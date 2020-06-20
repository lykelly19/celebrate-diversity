import os
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import datetime
import json
import wikipedia

app = Flask(__name__)

with open('observances_data.json') as json_file:
    data = json.load(json_file)

months = { 1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
           7: 'July', 8: 'August', 9:' September', 10: 'October', 11: 'November', 12: 'December'}

@app.route('/', methods=['POST'])
def receive_sms():
    text = request.values.get('Body', None)
    text = text.strip()  # remove leading/trailing whitespaces
    today = datetime.datetime.now()
    month = months[today.month]  # convert from the int to word/string representation of a month

    message_string = ''

    if text.upper() == 'INFO':
        message_string += '\nThe month is {}. Learn more by sending the number to the left of the following options: \n'.format(month)

        for i in range(len(data[month]['observances'])):  # print the month's observances
            message_string += str(i + 1) + ': ' + data[month]['observances'][i] + '\n'

        if(len(data[month]['observances']) == 0):  # if no observances found for the month
            message_string += 'Learn more about...'

    else:
        try:
            numeric_selection = int(text)
            if numeric_selection <= len(data[month]['observances']):
                message_string += '**{}**\n'.format(data[month]['observances'][numeric_selection-1])
                message_string += wikipedia.summary(data[month]['observances'][numeric_selection-1])
        except ValueError:
            pass

    if(len(message_string) == 0):
        message_string = "Learn more by texting INFO"

    resp = MessagingResponse()
    resp.message(message_string)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
