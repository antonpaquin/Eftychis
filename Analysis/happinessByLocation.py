from elasticsearch import Elasticsearch
import matplotlib
import code

es = Elasticsearch()

geocodesFile = 'params/geocodes.txt'

with open(geocodesFile) as geocodes_f:
    geocodes = [[float(g) for g in line.strip().split(',')] for line in geocodes_f.readlines()]

def getAvgPositivity(location):
    j = es.search(
        index='twdata',
        doc_type='tweet',
        body={
            "query": {
                "bool": {
                    "filter" : {
                        "geo_bounding_box" : {
                            "pin.location" : {
                                "top_left" : {
                                    "lat" : location[0] + 0.1,
                                    "lon" : location[1] - 0.1
                                },
                                "bottom_right" : {
                                    "lat" : location[0] - 0.1,
                                    "lon" : location[1] + 0.1
                                }
                            }
                        }
                    }
                }
            },
            "aggs": {
                "avg_happy": {
                    "avg": { "field": "happyScore" }
                }
            }
        },
        size=0
    )

    return j

code.interact(local=locals())
