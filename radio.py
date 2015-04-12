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
tweet_testing = True
cur_feed = None

feeds = {
    '5' : {
        'years': 5,
        'title': '5 Years Ago in Music',
        'playlist_uri':'spotify:user:plamere:playlist:4VNzdtsvmHz31W3H6eDSEF',
        'playlist_url':'https://open.spotify.com/user/plamere/playlist/4VNzdtsvmHz31W3H6eDSEF',
        'twitter_consumer_key':'0918eqwf81vmYWWhRguLIwiTC',
        'twitter_consumer_secret':'W1ZcAqZu0gNAFwN7YD3TtvnrKyGZva4WiAr1P3g3cXnu9WmMWi',
        'twitter_access_token':'3155979951-9bUjBJfXzKSVYzoM5kQ8OS4AeVEymsB5VyICL72',
        'twitter_access_token_secret':'Go1SMwNOMHALuENMQkgjmUjgVl0SBNvrAaGmDRS2mKT4D',
    },
    '10' : {
        'years': 10,
        'title': '10 Years Ago in Music',
        'playlist_uri':'spotify:user:plamere:playlist:4VNzdtsvmHz31W3H6eDSEF',
        'playlist_url':'https://open.spotify.com/user/plamere/playlist/4VNzdtsvmHz31W3H6eDSEF',
        'twitter_consumer_key':'0918eqwf81vmYWWhRguLIwiTC',
        'twitter_consumer_secret':'W1ZcAqZu0gNAFwN7YD3TtvnrKyGZva4WiAr1P3g3cXnu9WmMWi',
        'twitter_access_token':'3155979951-9bUjBJfXzKSVYzoM5kQ8OS4AeVEymsB5VyICL72',
        'twitter_access_token_secret':'Go1SMwNOMHALuENMQkgjmUjgVl0SBNvrAaGmDRS2mKT4D',
    },
    '20' : {
        'years': 20,
        'title': '20 Years Ago in Music',
        'playlist_uri':'spotify:user:plamere:playlist:1HnmSGLvzXQejvcsgob208',
        'playlist_url':'https://open.spotify.com/user/plamere/playlist/1HnmSGLvzXQejvcsgob208',
        'twitter_consumer_key':'0918eqwf81vmYWWhRguLIwiTC',
        'twitter_consumer_secret':'W1ZcAqZu0gNAFwN7YD3TtvnrKyGZva4WiAr1P3g3cXnu9WmMWi',
        'twitter_access_token':'3155979951-9bUjBJfXzKSVYzoM5kQ8OS4AeVEymsB5VyICL72',
        'twitter_access_token_secret':'Go1SMwNOMHALuENMQkgjmUjgVl0SBNvrAaGmDRS2mKT4D',
    },
    '30' : {
        'years': 30,
        'title': '30 Years Ago in Music',
        'playlist_uri':'spotify:user:plamere:playlist:7tsCIT87Be5AP0eaJe1lY7',
        'playlist_url':'https://open.spotify.com/user/plamere/playlist/7tsCIT87Be5AP0eaJe1lY7',
        'twitter_consumer_key':'0918eqwf81vmYWWhRguLIwiTC',
        'twitter_consumer_secret':'W1ZcAqZu0gNAFwN7YD3TtvnrKyGZva4WiAr1P3g3cXnu9WmMWi',
        'twitter_access_token':'3155979951-9bUjBJfXzKSVYzoM5kQ8OS4AeVEymsB5VyICL72',
        'twitter_access_token_secret':'Go1SMwNOMHALuENMQkgjmUjgVl0SBNvrAaGmDRS2mKT4D',
    },
    '40' : {
        'years': 40,
        'title': '40 Years Ago in Music',
        'playlist_uri':'spotify:user:plamere:playlist:3N26XDqRfWT1DpXFBT2MlE',
        'playlist_url':'https://open.spotify.com/user/plamere/playlist/3N26XDqRfWT1DpXFBT2MlE',
        'twitter_consumer_key':'0918eqwf81vmYWWhRguLIwiTC',
        'twitter_consumer_secret':'W1ZcAqZu0gNAFwN7YD3TtvnrKyGZva4WiAr1P3g3cXnu9WmMWi',
        'twitter_access_token':'3155979951-9bUjBJfXzKSVYzoM5kQ8OS4AeVEymsB5VyICL72',
        'twitter_access_token_secret':'Go1SMwNOMHALuENMQkgjmUjgVl0SBNvrAaGmDRS2mKT4D',
    },
    '50' : {
        'years': 50,
        'title': '50 Years Ago in Music',
        'playlist_uri':'spotify:user:plamere:playlist:20MRgCn9dwNPeGhNBGAlZZ',
        'playlist_url':'http://open.spotify.com/user/plamere/playlist/20MRgCn9dwNPeGhNBGAlZZ',
        'twitter_consumer_key':'0918eqwf81vmYWWhRguLIwiTC',
        'twitter_consumer_secret':'W1ZcAqZu0gNAFwN7YD3TtvnrKyGZva4WiAr1P3g3cXnu9WmMWi',
        'twitter_access_token':'3155979951-9bUjBJfXzKSVYzoM5kQ8OS4AeVEymsB5VyICL72',
        'twitter_access_token_secret':'Go1SMwNOMHALuENMQkgjmUjgVl0SBNvrAaGmDRS2mKT4D',
    },
}

def authenticate():
    consumer_key = cur_feed['twitter_consumer_key']
    consumer_secret = cur_feed['twitter_consumer_secret']
    access_token = cur_feed['twitter_access_token']
    access_token_secret = cur_feed['twitter_access_token_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def twitter_post(text):
    if tweet_testing:
        print text
    else:
        api.update_status(text)

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
        

def save_to_playlist(sids):
    uris = []
    for i, id in enumerate(sids):
        if id and str(id) in charts['songs']:
            song = charts['songs'][str(id)]
            if 'uri' in song:
                uri = song['uri']
                uris.append(uri)

    return sp.user_playlist_replace_tracks(user, cur_feed['playlist_uri'], uris)


def fun_facts(date, sids):
    sdate = date.strftime('%Y-%m-%d')
    facts = []
    artists = collections.Counter()
    shortest = None
    longest = None
    year = str(date.year)

    def add_fact(score, txt):
        facts.append( (score, txt) )

    def fn(song):
        return song['title'] + ' by ' + fix_name(song['artist'])

    def fp(p):
        return  "#" + str(p)

    def intro():
        return 'This week in ' + year + ' '
        #return 'On ' + sdate + ' '

    for i, id in enumerate(sids):
        if id and str(id) in charts['songs']:
            song = charts['songs'][str(id)]
            artist = fix_name(song['artist'])
            artists[artist] += 1
            if i == 0:
                add_fact(1, intro() + 'the #1 song was ' + fn(song))
            if song['peak_week'] == sdate:
                score = 6 - i / 100.0
                add_fact(score, intro() + fn(song) +' reached its peak at ' + fp(i + 1))
            if song['entered'] == sdate:
                score = 5 - i / 100.0
                add_fact(score, intro() + fn(song) +' entered the charts at ' + fp(i + 1))

            wc = song['weeks_charted']
            if shortest == None or wc < shortest['weeks_charted']:
                shortest = song
            if longest == None or wc > longest['weeks_charted']:
                longest = song

            if song['yearly_rank'] < 10:
                score = 2 - i / 100.
                add_fact(score, intro() + 'top 10 song of ' + year + ' ' \
                    + fn(song) + 'was at ' + fp(i + 1))

    for i, (a, c) in enumerate(artists.most_common(3)):
        score = 5 + c
        if c > 2:
            add_fact(score + c, intro()  + a + ' appears on the chart ' + str(c) + ' times.')

    add_fact(5, fn(shortest) + ' was only on the charts for ' + \
        str(shortest['weeks_charted']) + ' weeks.')
    add_fact(2, fn(longest) + ' was on the charts for ' + \
        str(longest['weeks_charted']) + ' weeks.')
    facts.sort(reverse=True)
    return facts


def show_fun_facts(facts):
    for score, txt in facts:
        print score, txt


def fix_name(name):
    if name.endswith(', The'):
        return 'The ' + name.replace(', The', '')
    else:
        return name


def create_tweet(txt):
    msg = txt + ' ' + cur_feed['playlist_url']
    twitter_post(msg)


def tweet_fun_fact(facts, which):
    if len(facts) > 0:
        idx = which % len(facts)
        score, tweet = facts[idx]
        create_tweet(tweet)


def get_tweet_count():
    tweets_per_day = 3
    today = datetime.datetime.now()
    day_of_week = today.weekday()
    hc = int(today.hour / (24. / tweets_per_day))
    tweet_count = day_of_week * tweets_per_day + hc
    return int(tweet_count)

    
if __name__ == '__main__':
    save = True
    just_tweet = False
    tweet_count = 0
    sdate = None

    which = sys.argv[1]
    if which in feeds:
        cur_feed = feeds[which]
        years = cur_feed['years']
    else:
        print 'unknown feed', which
        sys.exit(0)

    if len(sys.argv) > 2:
        if sys.argv[2] == '--tweet':
            just_tweet = True
            save = False
            if len(sys.argv) > 3:
                tweet_count = int(sys.argv[3])
            else:
                tweet_count = get_tweet_count()
        elif sys.argv[2] == '--date':
            sdate = parse_date(sys.argv[3])

    if sdate == None:
        today = datetime.datetime.now().date()
        try:
            sdate = datetime.date(today.year - years, today.month, today.day)
        except ValueError:
            # leap year w00t
            delta = int(years * .2425)
            sdate = today - datetime.timedelta(365 * years + delta)

    api = authenticate()
    token = util.prompt_for_user_token(user, scope)
    if token:
        sp = spotipy.Spotify(auth=token)
        charts = load_pickle()
        prep_charts(charts)
        date, sids = get_best_match_for_date(sdate)
        if sids:
            if save:
                response = save_to_playlist(sids)
                if not response:
                    create_tweet('The ' + cur_feed['title']  + ' playlist has just been updated.')
            else:
                facts = fun_facts(date, sids)
                tweet_fun_fact(facts, tweet_count)
        else:
            print 'no chart found for ', sdate
    else:
        print "can't connect to spotify"

