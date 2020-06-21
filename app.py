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

def getSpotifyTrack():
    pass

@app.route('/', methods=['POST'])
def receive_sms():
    text = request.values.get('Body', None)
    text = text.strip()  # remove leading/trailing whitespaces
    today = datetime.datetime.now()
    month = months[today.month]  # convert from the int to word/string representation of a month

    message_string = ''

    if text.upper() == 'LEARN':

        if len(data[month]['observances']) == 0:  # if no observances found for the month
            message_string += 'Learn more about...'
        else:
            month_observances = ''
            for i in range(len(data[month]['observances'])):
                if i == len(data[month]['observances']) - 1 and len(data[month]['observances']) >=2:
                    month_observances += ' and '
                month_observances += data[month]['observances'][i]
                if i + 2 < len(data[month]['observances']):
                    month_observances += ', '

            message_string += "This month, {}, is {}!\nTo learn more and get awesome book, music, podcast, and article recommendations to celebrate, text back one of the following number(s): \n".format(month, month_observances)

            for i in range(len(data[month]['observances'])):  # print the month's observances
                message_string += str(i + 1) + ': ' + data[month]['observances'][i] + '\n'

    else:
        try:
            numeric_selection = int(text)  # try to convert string to int
            celebration = data[month]['observances'][numeric_selection-1]
            if numeric_selection <= len(data[month]['observances']):
                message_string += '**{}**\n'.format(celebration)
                message_string += wikipedia.summary(celebration) + '\n'
                message_string += '(Info retrieved from Wikipedia)'
        except ValueError:
            pass

    if(len(message_string) == 0):
        message_string = "Learn more by texting LEARN"

    resp = MessagingResponse()
    resp.message(message_string)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
