from elasticsearch import Elasticsearch
from tweetscore import tweetScore
import json
import code

es = Elasticsearch()

batchSize = 100
scrollContext = '10m'

last_scroll_id = ''

def getIdBatch():
    global last_scroll_id
    
    j = es.scroll(
        scroll=scrollContext,
        scroll_id=last_scroll_id
    )
    last_scroll_id = j['_scroll_id']
    ids = [a['_id'] for a in j['hits']['hits']]
    return ids

def getFirstIdBatch():
    global last_scroll_id
    
    j = es.search(
        index='twdata',
        doc_type='tweet',
        body={
            'query': {
                "bool": {
                    "must_not": {
                        "exists" : { "field" : "happyScore" }
                        }
                    },
                "range": {
                    "time": {
                        "gte": 1488344400000,
                        "lte": 1493697600000,
                        "format": "epoch_millis"
                        }
                    }
                }
            },
        scroll=scrollContext,
        size=batchSize
    )
    last_scroll_id = j['_scroll_id']
    ids = [a['_id'] for a in j['hits']['hits']]
    return ids

def getTermedTweet(ids):
    j = es.mtermvectors(
        index='twdata',
        doc_type='tweet',
        ids=','.join(ids),
        fields='content',
        offsets=False,
        field_statistics=False,
        payloads=False,
        positions=False,
        realtime=False
    )
    return [(a['_id'], list(a['term_vectors']['content']['terms'].keys())) for a in j['docs'] if a['term_vectors'] != {}]

def scoreAndUpdateTweet(tweet):
    tid = tweet[0]
    score = tweetScore(tweet[1])
    es.update(
        index='twdata',
        doc_type='tweet',
        id=tid,
        body={
            'doc': {
                'happyScore': score
            }
        },
        retry_on_conflict=10
    )

def step():
    if last_scroll_id == '':
        ids = getFirstIdBatch()
    else:
        ids = getIdBatch()

    tweets = getTermedTweet(ids)

    for tweet in tweets:
        scoreAndUpdateTweet(tweet)


def run():
    i = 0
    while i < 24000000:
        step()
        i += batchSize
        print(i)

run()
