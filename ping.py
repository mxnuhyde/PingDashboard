import time
import requests
from ping3 import ping
from datetime import datetime
from flask import Flask, request

# Configurazione
IP_ADDRESS = "ip_to_monitor"
CHECK_INTERVAL = 60
TELEGRAM_TOKEN = "telegram_token"
CHAT_ID = "chat_id"
BOT_PORT = 5000

# Inizializza Flask per gestire i comandi Telegram
app = Flask(__name__)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except requests.exceptions.RequestException as e:
        print(f"Errore nell'invio del messaggio: {e}")

# Stato iniziale
response = ping(IP_ADDRESS)
is_online = response is not None
last_status = is_online
last_hourly_report = datetime.now().hour

# Invia un primo messaggio con lo stato iniziale
if is_online:
    send_telegram_message(f"✅ L'IP {IP_ADDRESS} è ONLINE all'avvio dello script")
else:
    send_telegram_message(f"❌ L'IP {IP_ADDRESS} è OFFLINE all'avvio dello script")

# Funzione per gestire i comandi Telegram
@app.route(f"/bot{TELEGRAM_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        message_text = data["message"]["text"].strip()
        
        if message_text == "/stato":
            status_message = f"✅ L'IP {IP_ADDRESS} è ONLINE" if is_online else f"❌ L'IP {IP_ADDRESS} è OFFLINE"
            send_telegram_message(status_message)
    return "", 200

# Rimuovi il controllo sugli orari, ora invia un aggiornamento ogni minuto
while True:
    response = ping(IP_ADDRESS)
    is_online = response is not None
    current_hour = datetime.now().hour
    current_minute = datetime.now().minute
    
    # Invia notifica se lo stato cambia
    if last_status != is_online:
        if is_online:
            send_telegram_message(f"✅ L'IP {IP_ADDRESS} è tornato ONLINE")
        else:
            send_telegram_message(f"❌ L'IP {IP_ADDRESS} è andato OFFLINE")
        last_status = is_online
    
    # Invia aggiornamento orario ogni minuto
    if current_minute == 0 and current_hour != last_hourly_report:
        if is_online:
            send_telegram_message(f"⏰ Aggiornamento orario: L'IP {IP_ADDRESS} è ONLINE")
        else:
            send_telegram_message(f"⏰ Aggiornamento orario: L'IP {IP_ADDRESS} è OFFLINE")
        last_hourly_report = current_hour

    time.sleep(CHECK_INTERVAL)
