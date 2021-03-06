import os
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import datetime
import json
import wikipedia
import random

app = Flask(__name__)

with open('observances_data.json') as json_file:
    data = json.load(json_file)

months = { 1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
           7: 'July', 8: 'August', 9:' September', 10: 'October', 11: 'November', 12: 'December'}

def getSpotifyTrack(playlist_id):
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    CLIENT_ID = os.environ['CLIENT_ID']
    CLIENT_SECRET = os.environ['CLIENT_SECRET']

    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    auth_response_data = auth_response.json()
    SPOTIFY_ACCESS_TOKEN = auth_response_data['access_token']

    headers = { 'Authorization': 'Bearer {token}'.format(token=SPOTIFY_ACCESS_TOKEN) }
    BASE_URL = 'https://api.spotify.com/v1/'
    r = requests.get(BASE_URL + 'playlists/' + playlist_id, headers=headers)
    r = r.json()

    spotify_song_message = 'Spotify Song Track: '
    artist_count = 0
    random_number = random.randint(0, len(r['tracks']['items']) - 1)
    song = r['tracks']['items'][random_number]
    spotify_song_message += song['track']['name'] + ' by '

    for artist in song['track']['artists']:
        if artist_count == len(song['track']['artists']) - 1 and len(song['track']['artists']) >=2:
            spotify_song_message += ' and '
        spotify_song_message += artist['name']
        if artist_count + 2 < len(song['track']['artists']):
            spotify_song_message += ', '
        artist_count += 1

    spotify_song_message += '\n' + song['track']['external_urls']['spotify'] + '\n'

    return spotify_song_message

def getBookInfo(author):
    url = "https://www.googleapis.com/books/v1/volumes?q=inauthor:" + author.lower().replace(' ', '-')
    response = requests.get(url)
    json_data = json.loads(response.text)
    if len(json_data['items']) > 0:
        if len(json_data['items']) > 3:  # look at most the top 3 results (higher relevance)
            max = 3
        else:
            max = len(json_data['items'])
        random_number = random.randint(0, max - 1)
        title = json_data['items'][random_number]['volumeInfo']['title']
        preview_link = json_data['items'][random_number]['volumeInfo']['previewLink']
        return '\nBook: {} by {}\n{}\n'.format(title, author, preview_link)
    return ''

@app.route('/', methods=['POST'])
def receive_sms():
    text = request.values.get('Body', None)
    text = text.strip()  # remove leading/trailing whitespaces
    today = datetime.datetime.now()
    month = months[today.month]  # convert from the int to word/string representation of a month

    message_string = ''

    if text.upper() == 'LEARN':

        if len(data[month]['observances']) == 0:  # if no observances found for the month
            message_string += 'Celebrate diversity and learn more by checking out https://www.doinggoodtogether.org/bhf/celebrate-diversity'
        else:
            month_observances = ''
            for i in range(len(data[month]['observances'])):
                if i == len(data[month]['observances']) - 1 and len(data[month]['observances']) >=2:
                    month_observances += ' and '
                month_observances += data[month]['observances'][i]
                if i + 2 < len(data[month]['observances']):
                    month_observances += ', '

            message_string += "\nThis month, {}, is {}!\nTo learn more and get awesome book, music, and podcast recommendations to celebrate, text back one of the following number(s): \n".format(month, month_observances)

            for i in range(len(data[month]['observances'])):  # print the month's observances
                message_string += str(i + 1) + ': ' + data[month]['observances'][i] + '\n'

    else:
        try:
            numeric_selection = int(text)  # try to convert string to int
            celebration = data[month]['observances'][numeric_selection-1]
            if numeric_selection <= len(data[month]['observances']):
                message_string += '\n**{}**\n\n'.format(celebration)
                message_string += wikipedia.summary(celebration)[0:300] + '...\n'
                message_string += '(Info retrieved from Wikipedia)\n\n'
            if len(data[month][celebration]['spotify_song_playlist_id']) > 0:
                message_string += getSpotifyTrack(data[month][celebration]['spotify_song_playlist_id'])
            if len(data[month][celebration]['spotify_podcast']['name']) > 0:
                message_string += '\nSpotify Podcast: ' + data[month][celebration]['spotify_podcast']['name'] + '\n'
                message_string += data[month][celebration]['spotify_podcast']['link'] + '\n'
            if len(data[month][celebration]['authors']) > 0:
                random_number = random.randint(0, len(data[month][celebration]['authors']) - 1)
                author = data[month][celebration]['authors'][random_number]
                message_string += getBookInfo(author)
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
