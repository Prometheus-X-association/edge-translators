#!/bin/bash

echo -e "\n"
echo " [Mindmatcher] local Docker Elasticsearch clean index data"
echo " ========================================================="
echo -e "\n"

clear_line() {
  echo -ne "\r\033[K"
}

# Declare per-index import types
declare -A index_types
index_types["edge_matchings"]="data"
index_types["edge_rules"]="data"

echo -e "\n👉 Clean elasticsearch data"
for index in "${!index_types[@]}"; do
    echo -e "   └─${index}"
    curl -X POST "http://localhost:9200/${index}/_delete_by_query" -H 'Content-Type: application/json' -d '{"query":{"match_all":{}}}'
done
echo -e "   └─🎉 Clean succeeded"
exit 0