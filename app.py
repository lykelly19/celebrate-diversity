import os
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import datetime

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_sms():
    body = request.values.get('Body', None)

    months = { 1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
               7: 'July', 8: 'August', 9:' September', 10: 'October', 11: 'November', 12: 'December'}
    today = datetime.datetime.now()   
    message_string = "The month is {}".format(months[today.month])

    resp = MessagingResponse()
    resp.message(message_string)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
