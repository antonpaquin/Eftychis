curl -XPUT 'http://127.0.0.1:9200/twdata/_mapping/content?pretty' -d @json/enable_fielddata.json > results/enable_fielddata.json &&
cat results/enable_fielddata.json
