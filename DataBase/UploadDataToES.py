#!/usr/bin/env python3

import json
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
                "image_link": {
                    "type": "keyword"
                },
                "link": {
                    "type": "keyword"
                },
                "duration": {
                    "type": "short"
                },
                "score": {
                    "type": "float"
                },
                "ingredients_count":{
                    "type": "short"
                },
                "ingredients": {
                    "type": "nested",
                    "properties": {
                        "ingredient": {
                            "type": "keyword"
                        },
                        "quantity": {
                            "type": "keyword"
                        },
                        "unit": {
                            "type": "keyword"
                        }
                    }
                },
                "type": {
                    "type": "keyword"
                },
                "steps": {
                    "type": "text"
                },
                "nb_people": {
                    "type": "short"
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
    is_stored = True

    duration = record["duration"]

    if duration is None:
        record["duration"]  = -1
    else:
        duration = duration.replace('h',' ')
        duration = duration.split(' ')
        if duration[1] != 'min':
            record["duration"] = int(duration[0]) * 60
            if duration[1].isnumeric():
                record["duration"] += int(duration[1])
        else:
            record["duration"] = int(duration[0])

        record["ingredients_count"] = len(record["ingredients"])
        print(len(record["ingredients"]))

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
            create_index(es, 'recipes', settings_recipe)
            for doc in documents:
                out = store_record(es, 'recipes', doc)
