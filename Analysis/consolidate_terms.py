import json
import code

with open('results/count_terms.json') as json_f:
    results_s = json_f.read()

results = json.loads(results_s)

wordlist = results['aggregations']['top_count']['buckets']

with open('results/consolidate_terms.txt', 'w') as out_f:
    for word in wordlist:
        gram = word['key'].encode('utf-8')
        out_f.write(gram + '\n')
