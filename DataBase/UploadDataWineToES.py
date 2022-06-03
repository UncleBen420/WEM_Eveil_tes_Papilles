#!/usr/bin/env python3

import json
from pprint import pprint
from elasticsearch import Elasticsearch
import argparse

# Schema for recipes
settings_recipe = {
    "settings": {
        "number_of_shards": 1
    },
    "mappings": {
            "properties": {
                "title": {
                    "type": "text"
                },
                "country": {
                    "type": "keyword"
                },
                "grape_variety": {
                    "type": "keyword"
                },
                "description": {
                    "type": "text"
                },
                "pairsWellWith": {
                    "type": "nested",
                    "properties": {
                        "terms": {
                            "type": "keyword"
                        }
                    }
                }
            }
        }
}

def create_index(es_object, index_name, settings):
    created = False
    # index setting
    try:
        if not es_object.indices.exists(index=index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(index=index_name, settings=settings_recipe["settings"], mappings=settings_recipe["mappings"])

            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def store_record(elastic_object, index_name, record):

    pairwells = []
    for pw in record["pairsWellWith"]:
        pairwells.append({"terms":pw})
    record["pairsWellWith"] = pairwells

    print(record)

    is_stored = True
    try:
        #outcome = elastic_object.bulk(index=index_name, body=bulk_data)
        outcome = elastic_object.index(index=index_name, document=record)
        print(outcome)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))
        is_stored = False
    finally:
        return is_stored


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Connected')
    else:
        print('Error')
    return _es

if __name__ == '__main__':

    es = connect_elasticsearch()

    parser = argparse.ArgumentParser(description='Can upload the recipes form a file.jl to ElasticSearch')
    parser.add_argument('--path', metavar='path', required=True, help='the path to the file to upload')
    args = parser.parse_args()

    with open(args.path) as f:
        documents = json.loads("[" + f.read().replace("}\n{", "},\n{") + "]")

        if es is not None:
            create_index(es, 'wines', settings_recipe)
            for doc in documents:
                out = store_record(es, 'wines', doc)
