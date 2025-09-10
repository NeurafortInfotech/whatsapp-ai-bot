from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

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

    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
