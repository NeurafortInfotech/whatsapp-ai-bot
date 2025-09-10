from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Webhook verification
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return 'Verification failed', 403

    elif request.method == 'POST':
        data = request.get_json()
        print("Incoming:", data)

        try:
            message = data['entry'][0]['changes'][0]['value']['messages'][0]
            from_number = message['from']
            user_message = message['text']['body'].lower()

            reply = "How can I help you today? Do you want to place an order?"

            # Send WhatsApp reply
            url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
            headers = {
                "Authorization": f"Bearer {WHATSAPP_TOKEN}",
                "Content-Type": "application/json"
            }
            payload = {
                "messaging_product": "whatsapp",
                "to": from_number,
                "type": "text",
                "text": {"body": reply}
            }

            requests.post(url, headers=headers, json=payload)

        except Exception as e:
            print("Error:", e)

        return "ok", 200

@app.route('/')
def home():
    return "WhatsApp chatbot webhook is running!"


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
