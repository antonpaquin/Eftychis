from elasticsearch import Elasticsearch
import statistics
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
                            "location" : {
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

    return j['aggregations']['avg_happy']['value']


def getPositivities():
    return [getAvgPositivity(g) for g in geocodes]


def transformPositivities(avgs):
    mMean = statistics.mean(avgs)
    mStdev = statistics.stdev(avgs)
    zscores = [(a - mMean) / mStdev for a in avgs]
    return zscores


def putValues(scores, ranks):
    data = []
    for geo, score, rank in zip(geocodes, scores, ranks):
        es.index(
            index='vizdata',
            doc_type='map_happiness',
            body={
                'location': str(geo[0]) + ',' + str(geo[1]),
                'zscore': score,
                'rank': rank
            }
        )

def run():
    positivity = getPositivities()
    posranks = [(p, x) for p, x in zip(positivity, range(len(positivity)))]
    posranks = [a[1] for a in sorted(posranks)]
    z = transformPositivities(positivity)
    putValues(z, posranks)


code.interact(local=locals())
