from elasticsearch import Elasticsearch
from tweetscore import tweetScore
import datetime
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
    t0, t1 = getStartTime()
    j = es.search(
        index='twdata',
        doc_type='tweet',
        body={
            'query': {
                "bool": {
                    "must_not": {
                        "exists" : { "field" : "happyScore" }
                        },
                    "must": {  
                        "range": {
                            "time": {
                                "gte": str(int(t0)),
                                "lt": str(int(t1)),
                                "format": "epoch_millis"
                                }
                            }
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
        retry_on_conflict=1
    )

def getStartTime():
    with open('params/multithread_time.txt', 'r') as time_f:
        indx = int(time_f.readline().strip())

    with open('params/multithread_time.txt', 'w') as time_f:
        time_f.write(str(indx + 1))
        time_f.write('\n')

    startTime = unix_time_millis(datetime.datetime(2017, 4, 24, 0, 0))
    interval = 12 * 60 * 60 * 1000
    startTime += indx * interval
    return startTime, startTime + interval

epoch = datetime.datetime.utcfromtimestamp(0)
def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

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
