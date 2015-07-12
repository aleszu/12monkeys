curl -XDELETE "localhost:9200/articles*?pretty"
curl -XDELETE "localhost:9200/_template/articles?pretty"
curl -XPUT "localhost:9200/_template/twitter?pretty" -d "@articles_template.json"
python getfragments.py

 