from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# Load OpenAI API Key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

knowledge_paragraph = """
Welcome to MBot! We are an AI-powered service helping small businesses.
We are located in the heart of Berlin near Kaisar DAM.
Our business hours are 9 AM to 5 PM, Monday through Friday.
We offer full refunds within 30 days of purchase, no questions asked.
For support, we are available 24/7 via email and WhatsApp. Do you want to place an order then we have variety of dishes and lunch breakfast. Contact us for full support.  
"""

def generate_ai_response(user_input):
    prompt = f"""
You are a helpful assistant. Use the information below to answer the user's question.
If the answer is not found, reply: "I'm sorry, I couldn't find an answer to that."

Information:
{knowledge_paragraph}

User question: {user_input}
"""

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()


@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    print("User said:", incoming_msg)

    reply = generate_ai_response(incoming_msg)

    resp = MessagingResponse()
    msg = resp.message()
    msg.body(reply)

    return str(resp), 200


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
