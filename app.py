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

@app.route('/', methods=['POST'])
def telegram_webhook():
    data = request.json
    if data and "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]
        # Responder al chat con lo que reciba
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                     params={"chat_id": chat_id, "text": f"Recibido: {text}"})
    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


