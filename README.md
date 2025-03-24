# IP Monitoring Script with Telegram Notifications

This script monitors the status of a specified IP address and sends real-time notifications to a **Telegram** chat whenever the IP goes online or offline. It also sends periodic hourly updates.

## 🚀 Features

- **Ping Monitoring**: The script pings the given IP address at regular intervals (default: every 60 seconds).
- **Telegram Integration**: Sends notifications to a Telegram chat when the IP is online or offline.
- **Hourly Updates**: Provides a status update at the start of each new hour.
- **Command Handling**: You can query the current status of the IP by sending a `/stato` command via Telegram.

## 🛠️ Requirements

- **Python 3.x**
- **Flask**: Web framework to handle Telegram commands.
- **ping3**: Python library to ping an IP address.
- **requests**: For sending HTTP requests to the Telegram API.

You can install the required libraries using pip:

```bash
pip install flask ping3 requests
```

## ⚙️ Configuration
Before running the script, modify the following variables in the code:

IP_ADDRESS The IP address you want to monitor.
CHECK_INTERVAL The number of seconds between each ping check (default is 60 seconds).
TELEGRAM_TOKEN The token for your Telegram bot.
CHAT_ID The Telegram chat ID where the notifications will be sent.
BOT_PORT The port on which the bot will receive commands (default is 5000).


## 📜 How it works
**Initial Status**: On startup, the script checks the initial status of the specified IP address and sends a message to Telegram indicating whether it is online or offline.
**Real-time Monitoring**: The script pings the IP at regular intervals and sends a message to the Telegram chat whenever the status changes (IP goes online or offline).
**Hourly Updates**: Every hour, the script sends a status update indicating whether the IP is online or offline.
**Telegram Commands**: The bot listens for the /stato command and replies with the current status of the IP.


## 🛠️ Running the Script
Clone the repository to your local machine:
```bash
git clone https://github.com/yourusername/ip-monitor-telegram.git
cd ip-monitor-telegram
```

Run the script:
```bash
python ip_monitor.py
```
Ensure that Flask and the other dependencies are installed.


## ⚠️ Notes
Make sure your **Telegram bot** is created and the **bot token** is correctly set.
The script runs indefinitely and will keep monitoring the IP address. You can stop it manually by pressing Ctrl + C.
This script requires an active internet connection to send notifications via Telegram.


## 🤝 Contributions
Feel free to fork the repository and submit pull requests. Contributions are welcome!


## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

```bash
This **README.md** file provides a clear description of the script, its functionality, and the necessary setup instructions. It also includes sections on how to use and configure the script, making it easy for others to understand and contribute. Let me know if you'd like any changes or additions!
```
