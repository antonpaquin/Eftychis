from elasticsearch import Elasticsearch
from tweetscore import tweetScore
import json
import code

es = Elasticsearch()

last_scroll_id = ''

def getIdBatch():
    j = search(
        index='twdata',
        doc_type='tweet',
        body=getNextScroll(),
        scroll="1m",
        size=10
    )
    return j

def getNextScroll():
    return {
        "size": 100,
        "query": {
            "match_all" : {}
        },
        "scroll_id": last_scroll_id
    }

'''
POST /twdata/tweet/_mtermvectors
{
    "ids" : ["1", "2"],
    "parameters": {
        "fields": [
                "content"
        ]
    }
}
'''
code.interact(local=locals())
