50Year Radio
============
This is the source for 50 Year Radio, a python app that updates a set of Spotify playlists with the top tracks from the past.  

The script is intended to be run once a week (crontab for the win). It currently updates the following playlists:

   + 50 Years Ago in Music
   + 40 Years Ago in Music
   + 30 Years Ago in Music
   + 20 Years Ago in Music
   + 10 Years Ago in Music
   + 5 Years Ago in Music
   
It also tweets info about the updated playlists to a twitter account.

The chart data is derived from [The Whitburn Project](http://waxy.org/2008/05/the_whitburn_project/).

The app uses the Spotify API to create the playlists and the Twitter API to tweet the tweets.

Usage
====

    % python update_radio.py [year]
    
 or more typically as a crontab entry:
 
    0 9 * * 1  /path/to/app/go

 to run the script a 9AM every monday
 
Dependencies
------------
The script uses *spotipy* and *tweepy*

The script looks for credentials in environment variables (which are not maintained in the repo for obvious reasons). The following ENV variables should be set:

 - export SPOTIPY_CLIENT_ID='xxx'
 - export SPOTIPY_CLIENT_SECRET='xxx'
 - export SPOTIPY_REDIRECT_URI='https://xxx/yyy'
 - export twitter_consumer_key='xxx'
 - export twitter_consumer_secret='xxx'
 - export twitter_access_token='xxx'
 - export twitter_access_token_secret='xxx'
