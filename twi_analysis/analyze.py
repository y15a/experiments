# coding=utf-8
"""
analyze.py

USAGE: $ python analyze.py twitter_name_01 twitter_name_02

Scans through Twitter screen names as provided from the command line.
Aggregated statistics are then output to a file, with a default name of 'result.csv'

"""

import time, os
from twitter import Api


def get_stats(status):
    """
    Takes twitter.status.Status object.
    """
    return dict(
        num_fav = status.favorite_count,
        num_rt = status.retweet_count,
        fav2rt = status.favorite_count / status.retweet_count if status.retweet_count else None,
        status = status,
        julian_date   = status.created_at_in_seconds
    )


def aggregate_stats(stats, num_followers):
    num_tweets = len(stats)
    num_favs = sum([d['num_fav'] for d in stats])
    num_rt   = sum([d['num_rt'] for d in stats])
    ave_favs = 1.0 * num_favs / num_tweets
    ave_rt = 1.0 * num_rt / num_tweets
    times = sorted([d['julian_date'] for d in stats])
    tweets_per_day = 1.0 * num_tweets / (times[-1]-times[0]) * 86400
    engagement = ( ave_favs + ave_rt ) / num_followers * 10000
    return dict(
        num_tweets      = num_tweets,
        num_favs        = num_favs,
        num_rt          = num_rt,
        ave_favs        = ave_favs,
        ave_rt          = ave_rt,
        tweets_per_day  = tweets_per_day,
        engagement      = engagement
    )


def get_line(stat):
    """Formatting for CSV output.
    """
    s = stat['stats']
    return ','.join([ str(item) for item in [
        stat['screen_name'],
        stat['num_followers'],
        s['num_tweets'],
        s['num_favs'],
        s['num_rt'],
        s['ave_favs'],
        s['ave_rt'],
        s['tweets_per_day'],
        s['engagement']
    ]]) + '\n'


# Initialize Twitter API.

api = Api(base_url="https://api.twitter.com/1.1",
    consumer_key=os.getenv('TWITTER_C_KEY'),
    consumer_secret=os.getenv('TWITTER_C_SECRET'),
    access_token_key=os.getenv('TWITTER_T_KEY'),
    access_token_secret=os.getenv('TWITTER_T_SECRET')
)

# Initialize parameters.

NAMES = os.sys.argv[1:]
FILENAME = 'result.csv'
for n in NAMES:
    if 'filename=' in n:
        NAMES.remove(n)
        FILENAME = n.split('filename=')[1]
NUM_TWEETS = 100
aggregated = []

# Start Twitter query.

for screen_name in NAMES:
    print('Starting scran for %s...' % screen_name)
    tweets = []
    stats = []
    max_id = None
    num_followers = None

    while len(tweets) < NUM_TWEETS:
        print('Querying Twitter server. Current number of tweets = %i' % len(tweets))
        twts = api.GetUserTimeline(screen_name=screen_name, count=100, max_id=max_id)
        for t in twts:
            if t.user.screen_name != screen_name:
                continue
            if num_followers is None:
                num_followers = t.user.followers_count
            tweets.append(t)
            stats.append(get_stats(t))
            max_id = t.id if t.id > max_id else max_id
        time.sleep(1.0)

    ag = aggregate_stats(stats, num_followers)
    aggregated.append(dict(
        screen_name = screen_name,
        num_followers = num_followers,
        stats = ag
    ))



f = open(FILENAME, 'w')

f.write('screen_name,num_followers,num_tweets,num_favs,num_rt,ave_favs,ave_rt,tweets_per_day,engagement\n')
for stat in aggregated:
    f.write(get_line(stat))
f.close()

