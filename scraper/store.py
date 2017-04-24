import elasticsearch

es = elasticsearch.Elasticsearch()

def putMany(li, geo):
    for tweet in li:
        putTweet(tweet, geo)

exceptionCount = 0
def putTweet(t, geo):
    global exceptionCount

    neatText = t.text.replace('"', '\\"').replace('\n', '\\n')

    data = '''{{
        "original": "{}",
        "content": "{}",
        "user_id": {},
        "location": "{},{}",
        "id": {},
        "time": {}000
    }}'''.format(neatText, neatText, t.user.id, geo[0], geo[1], t.id, t.created_at_in_seconds)

    try:
        es.index(
            index='twdata',
            doc_type='tweet',
            body=data
        )
    except Exception:
        exceptionCount += 1

def tweetCount():
    return es.count(index='twdata')
