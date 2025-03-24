import time
import threading
import requests
from ping3 import ping
from datetime import datetime
from flask import Flask, request, render_template

# Configurazione
IP_ADDRESS = "ip_to_monitor"
CHECK_INTERVAL = 60
TELEGRAM_TOKEN = "telegram_token"
CHAT_ID = "chat_id"
BOT_PORT = 5000

# Inizializza Flask
app = Flask(__name__)

# Variabili globali
is_online = False
status_history = []  # Storico degli stati


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except requests.exceptions.RequestException as e:
        print(f"Errore nell'invio del messaggio: {e}")


def monitor_ip():
    """Monitora l'IP e aggiorna lo stato in background."""
    global is_online, status_history
    last_status = None

    while True:
        response = ping(IP_ADDRESS)
        is_online = response is not None
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Se cambia stato, invia il messaggio e aggiorna la cronologia
        if last_status != is_online:
            message = f"✅ L'IP {IP_ADDRESS} è tornato ONLINE" if is_online else f"❌ L'IP {IP_ADDRESS} è andato OFFLINE"
            send_telegram_message(message)
            status_history.insert(0, (timestamp, is_online))  # Aggiunge nuovo stato
            if len(status_history) > 10:  # Mantiene solo gli ultimi 10 record
                status_history.pop()
            last_status = is_online

        time.sleep(CHECK_INTERVAL)


@app.route("/")
def index():
    """Mostra lo stato attuale e lo storico nella dashboard."""
    return render_template("index.html", ip=IP_ADDRESS, is_online=is_online, history=status_history)


@app.route("/stato")
def get_status():
    """Endpoint API per ottenere lo stato attuale in JSON."""
    return {"ip": IP_ADDRESS, "is_online": is_online}


# Avvia il monitoraggio in un thread separato
monitor_thread = threading.Thread(target=monitor_ip, daemon=True)
monitor_thread.start()

# Avvia Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=BOT_PORT, debug=True)
