from elasticsearch import Elasticsearch
import code

es = Elasticsearch()
lastResult = ''


def check(word):
    global lastResult

    j = es.search(
        index='twdata',
        doc_type='tweet',
        body={
            'query': {
                'bool': {
                    'must': [
                        { 'term': {'content': word} },
                        { 'exists': {'field': 'happyScore'} }
                    ]
                }
            },
            'aggs': {
                'avg_score': {
                    'avg': { 'field': 'happyScore' }
                }
            }
        },
        size=0
    )

    count = str(j['hits']['total'])
    value = str(j['aggregations']['avg_score']['value'])

    print('')
    print('Count: ' + count)
    print('Value: ' + value)
    print('')

    lastResult = word + ',' + count + ',' + value

    return j

def take():
    global lastResult
    with open('results/interestingWords.txt', 'a') as words_f:
        words_f.write(lastResult + '\n')

code.interact(local=locals())
