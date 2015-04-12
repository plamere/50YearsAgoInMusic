import sys
import tweepy
import simplejson as json
import cPickle as pickle
import datetime
import spotipy
import spotipy.util as util
import pprint
import os
import collections

user = 'plamere'
scope = 'playlist-modify-public'

debug = False
tweet_debug = False

consumer_key = os.environ['twitter_consumer_key']
consumer_secret = os.environ['twitter_consumer_secret']
access_token = os.environ['twitter_access_token']
access_token_secret = os.environ['twitter_access_token_secret']

feeds = {
    '5' : {
        'years': 5,
        'title': '5 Years Ago in Music',
        'playlist_uri':'spotify:user:plamere:playlist:7L7F0RmgNOZ5O8UJX7s4RR',
        'playlist_url':'https://open.spotify.com/user/plamere/playlist/7L7F0RmgNOZ5O8UJX7s4RR',
    },
    '10' : {
        'years': 10,
        'title': '10 Years Ago in Music',
        'playlist_uri':'spotify:user:plamere:playlist:4VNzdtsvmHz31W3H6eDSEF',
        'playlist_url':'https://open.spotify.com/user/plamere/playlist/4VNzdtsvmHz31W3H6eDSEF',
    },
    '20' : {
        'years': 20,
        'title': '20 Years Ago in Music',
        'playlist_uri':'spotify:user:plamere:playlist:1HnmSGLvzXQejvcsgob208',
        'playlist_url':'https://open.spotify.com/user/plamere/playlist/1HnmSGLvzXQejvcsgob208',
    },
    '30' : {
        'years': 30,
        'title': '30 Years Ago in Music',
        'playlist_uri':'spotify:user:plamere:playlist:7tsCIT87Be5AP0eaJe1lY7',
        'playlist_url':'https://open.spotify.com/user/plamere/playlist/7tsCIT87Be5AP0eaJe1lY7',
    },
    '40' : {
        'years': 40,
        'title': '40 Years Ago in Music',
        'playlist_uri':'spotify:user:plamere:playlist:3N26XDqRfWT1DpXFBT2MlE',
        'playlist_url':'https://open.spotify.com/user/plamere/playlist/3N26XDqRfWT1DpXFBT2MlE',
    },
    '50' : {
        'years': 50,
        'title': '50 Years Ago in Music',
        'playlist_uri':'spotify:user:plamere:playlist:20MRgCn9dwNPeGhNBGAlZZ',
        'playlist_url':'http://open.spotify.com/user/plamere/playlist/20MRgCn9dwNPeGhNBGAlZZ',
    }
}

def authenticate():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def twitter_post(text):
    if debug or tweet_debug:
        print text
    else:
        try:
            api.update_status(text)
        except tweepy.error.TweepError as e:
            print 'trouble tweeting ' + text + ' ' + str(e)

def load_js():
    f = open('chart_details.js')
    js = f.read()
    f.close()

    obj = json.loads(js)
    return obj

def save_pickle(charts):
    f = open('chart_details.pkl', 'w')
    pickle.dump(charts, f, -1)
    f.close()

def load_pickle():
    f = open('chart_details.pkl')
    chart = pickle.load(f)
    f.close()
    return chart

def convert_charts_to_pickle():
    data = load_js()
    save_pickle(data)

def parse_date(dstring):
    date = datetime.datetime.strptime(dstring, '%Y-%m-%d').date()
    return date

def show_songs(song_ids):
    for i, id in enumerate(song_ids):
        if id and str(id) in charts['songs']:
            song = charts['songs'][str(id)]
            print i, song['title'], song['artist']

def show_week(date):
    if date in charts['charts']:
        week = charts['charts'][date]
        show_songs(week)

def prep_charts(charts):
    scharts = []
    for date_string,sids in charts['charts'].items():
        date = parse_date(date_string)
        scharts.append( (date, sids) )
    scharts.sort()
    charts['scharts'] = scharts

def get_best_match_for_date(sdate):
    for i, (date, sids) in enumerate(charts['scharts'][:-1]):
        ndate, nsids = charts['scharts'][i + 1]
        if sdate >= date and sdate < ndate:
            return date, sids
    return sdate, None
        
def save_to_playlist(feed, sids):
    uris = []
    for i, id in enumerate(sids):
        if id and str(id) in charts['songs']:
            song = charts['songs'][str(id)]
            if 'uri' in song:
                uri = song['uri']
                uris.append(uri)

    return sp.user_playlist_replace_tracks(user, feed['playlist_uri'], uris)

def fix_name(name):
    if name.endswith(', The'):
        return 'The ' + name.replace(', The', '')
    else:
        return name

def get_date(years):
    today = datetime.datetime.now().date()
    try:
        sdate = datetime.date(today.year - years, today.month, today.day)
    except ValueError:
        # leap year w00t
        delta = int(years * .2425)
        sdate = today - datetime.timedelta(365 * years + delta)
    return sdate

def fmt_date(date):
    return date.strftime('%Y-%m-%d')

def update_feed(feed):
    sdate = get_date(feed['years'])
    date, sids = get_best_match_for_date(sdate)
    if sids:
        if not debug:
            response = save_to_playlist(feed, sids)
        else:
            show_songs(sids)

        twitter_post('The ' + feed['title']  + \
            ' playlist has been updated for the week of ' + fmt_date(date) + '. ' + feed['playlist_url'])
    else:
        print 'no chart found for ', sdate
    
if __name__ == '__main__':
    api = authenticate()
    token = util.prompt_for_user_token(user, scope)

    if api and token:
        sp = spotipy.Spotify(auth=token)
    else:
        print "can't authenticate for twitter/spotify" 
        sys.exit(0)

    charts = load_pickle()
    prep_charts(charts)

    if len(sys.argv) > 1:
        for name in sys.argv[1:]:
            if name in feeds:
                update_feed(feeds[name])
            else:
                print 'unknown feed', name
    else:
        for label, feed in feeds.items():
            update_feed(feed)

