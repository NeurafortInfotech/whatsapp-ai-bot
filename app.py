from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').lower()
    print("Received:", incoming_msg)

    resp = MessagingResponse()
    msg = resp.message()

    if 'hi' in incoming_msg:
        msg.body("Hello from MBot on Render!")
    else:
        msg.body("Sorry, I didn't understand that.")

    return str(resp), 200  # Make sure to return status code 200


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Get Render-provided port
    app.run(host="0.0.0.0", port=port, debug=True)  # Bind to all interfaces
