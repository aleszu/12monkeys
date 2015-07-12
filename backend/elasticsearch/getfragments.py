from datetime import datetime
from elasticsearch import Elasticsearch
import json
import uuid
import random

es = Elasticsearch()

def es_compare(obj, url):
    paragraphs=5
    termscount=40
    session = uuid.uuid4().urn[9:]
    for o in obj:
        o["session"]=session
        es.index(index="articles", doc_type="article", body=o)
    es.indices.refresh(index="articles")
    res = es.search(index="articles", doc_type="article", body={
        "size": 0,
        "query": {
            "constant_score": {
                "filter": {
                    "bool": {
                        "must": {
                            "term": {
                                "session": session
                            }
                        },
                        "must_not": {
                            "term" : {
                                "url" : url
                            }
                        }
                    }
                }
            }
        },
        "aggregations": {
            "top_terms": {
                "terms": {
                    "field": "paragraphs.ngram",
                    "size": termscount
                }
            },
            "significant_terms": {
                "significant_terms": {
                    "field": "paragraphs.ngram",
                    "size": termscount,
                    "background_filter": {
                        "term": {
                            "session": session
                        }
                    }
                }
            }
        }
    })
    terms = []
    for term in res["aggregations"]["significant_terms"]["buckets"]:
        terms.append(term["key"])
    commonterms = []
    for term in res["aggregations"]["top_terms"]["buckets"]:
        commonterms.append(term["key"])
    terms = list(set(terms) - set(commonterms))
    # print("Searching for the terms " + str(terms));
    if not terms:
        # the remove of article doesn't affect significant scores
        return []
    res = es.search(index="articles", doc_type="article", body={
        "fields":["url", "img_src"],
        "query": {
            "filtered": {
                "query": {
                    "terms": {
                        "paragraphs.ngram": terms
                    }
                }, 
                "filter": {
                    "not": {
                        "term" : {
                            "url" : url
                        }
                    }
                }
            }
        },
        "highlight" : {
            "pre_tags" : [""],
            "post_tags" : [""],
            "fields" : {
                "paragraphs" : {"fragment_size" : 1000, "number_of_fragments" : 4}
            }
        }
    })
    result = []
    saw = {}
    for art in res["hits"]["hits"]:
        for par in art["highlight"]["paragraphs"]:
            if not par in saw:
                result.append({
                    'text': par,
                    'url': art['fields']['url'][0],
                    'img': art['fields']['img_src'][0]
                    })
                saw[par] = 1
    return result

##########################################
# Test portion 

f = open("articles.json")
jsonobj = json.load(f)
f.close()
num=random.randint(0, len(jsonobj)-1)
url = jsonobj[num]["url"]
res=es_compare(jsonobj, url)

orig=es.search(index="articles", doc_type="article", body={
    "size": 1,
    "fields": "paragraphs",
    "query": {
        "constant_score": {
            "filter": {
                "term" : {
                    "url" : url
                }
            }
        }
    }
})
print("\nOriginal article:\n")
print("---------------------------------------------------------------------------\n")
if "fields" in orig["hits"]["hits"][0]:
    for par in orig["hits"]["hits"][0]["fields"]["paragraphs"]:
        print(par)
else:
    print("<<<<< EMPTY ARTICLE AT " + url + ">>>>>")
print("---------------------------------------------------------------------------\n")
print("\nRelated Paragraphs\n")
for par in res:
    print('url: ' + str(par['url']) + ' ' + 'img:' + str(par['img']) )
    print(par['text'] + '\n')
