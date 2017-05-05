from elasticsearch import Elasticsearch
from scipy import stats
import code

es = Elasticsearch()

def getAll():
    j = es.search(
        index='vizdata',
        doc_type='map_happiness',
        body={
            'query': {
                'bool': {
                    'must': {
                        'exists': {'field': 'rank'},
                    }
                }
            },
            "script_fields" : {
                "florida_distance" : {
                    "script" : {
                        "lang": "painless",
                        "inline": "doc['location'].arcDistance(27, -88)"
                    }
                },
            },
            "docvalue_fields": [ "rank" ]
        },
        size=1200
    )

    dists = [a['fields']['florida_distance'][0] for a in j['hits']['hits']]
    ranks = [a['fields']['rank'][0] for a in j['hits']['hits']]

    return dists, ranks

code.interact(local=locals())
