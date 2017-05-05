curl -XPUT http://127.0.0.1:9200/vizdata/_mapping/map_happiness?pretty -d @json/addMapHappiness.json > results/addMapHappiness.json &&
cat results/addMapHappiness.json
