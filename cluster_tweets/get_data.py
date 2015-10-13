# coding=utf-8

import json
from twitter import Api

def get_setup():
    return json.load(open('setup.json', 'r'))

if __name__ == '__main__':
    setup = get_setup()
    api = Api(base_url="https://api.twitter.com/1.1",
        consumer_key=setup.get("consumer_key", ""),
        consumer_secret=setup.get("consumer_secret", ""),
        access_token_key=setup.get("access_token_key", ""),
        access_token_secret=setup.get("access_token_secret", "")
    )

    tweets = []
    max_id = None

    while len(tweets) < 5000:
        found = api.GetSearch(term=u'ダルビッシュ', count=100,
            result_type='recent', max_id=max_id)
        tweets += [f.text.encode('utf-8') for f in found]
        max_id = found[-1].id

    obj = [dict(text=t) for t in tweets]
    f = open('data.txt', 'w')
    f.write(json.dumps(obj))
    f.close()
