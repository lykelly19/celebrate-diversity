# Celebrating Diversity Through Tech

### About
This project was created for MLH Hack Girl Summer 2020 Hackathon. You can check out the Devpost Submission to learn more about the background of our project [here](https://devpost.com/software/celebrating-diversity-through-tech).   

### Description  
*Celebrating Diversity* is an accessible way to learn about diverse cultures and identities. Text to receive recommendations for books, podcasts, and music that represent and celebrate these communities. 

### Getting Started  
Activate the virtual environment: ```source ./env/scripts/activate```   
Install dependencies: ```pip install -r requirements.txt```

### How deploy your app with Heroku
Ensure that you have the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed

To be able to use the [Spotify API](https://developer.spotify.com/), you will need to create a Spotify Developers Account. You will need to add CLIENT_ID and CLIENT_SECRET from the Spotify API to the configuration variables on Heroku for authentication.

To use the [Twilio API](https://twilio.com/), you will also need to create an account. You can configure your phone number on the [console](https://www.twilio.com/console/phone-numbers/incoming). On the Messaging section, configure by selecting "Webhooks" and paste in your Heroku app's URL.

The other API you will be using is the [Google Books API](https://developers.google.com/books), which does not require authentication in this project for requesting book information.

```git init```   
```git add .```    
```git commit -m "initial code"```   
```heroku create```   
```heroku apps:rename custom_project_name```   
```git push heroku master```   
