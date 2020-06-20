import os
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import datetime
import json

app = Flask(__name__)

with open('observances_data.json') as json_file:
    data = json.load(json_file)

months = { 1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
           7: 'July', 8: 'August', 9:' September', 10: 'October', 11: 'November', 12: 'December'}

@app.route('/', methods=['POST'])
def receive_sms():
    body = request.values.get('Body', None)

    today = datetime.datetime.now()
    month = months[today.month]  # convert from the int to word/string representation of a month

    message_string = "The month is {}. Learn more by sending a number to the left of the following options: \n".format(month)

    for i in range(len(data[month]['observances'])):  # print the month's observances
        message_string += str(i + 1) + ': ' + data[month]['observances'][i] + '\n'

    if(len(data[month]['observances']) == 0):  # if no observances found for the month
        message_string += 'Learn more about...'

    resp = MessagingResponse()
    resp.message(message_string)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
