curl -XGET 'http://127.0.0.1:9200/twdata/tweet/_search?pretty' -d @json/count_terms.json > results/count_terms.json &&
cat results/count_terms.json
