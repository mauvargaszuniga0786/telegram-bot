from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    pair = data.get("asset")
    direction = data.get("direction")
    entry = data.get("entry_price")
    expiration = data.get("expiration")

    message = f"""
📊 Nueva Señal

Par: {pair}
Dirección: {direction}
Entrada: {entry}
Expiración: {expiration}
"""

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": message
    })

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
