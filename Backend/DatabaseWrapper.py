from elasticsearch import Elasticsearch

class DatabaseWrapper:

    def __init__(self, address='localhost', port=9200, index_recipe="recipes", index_wine = "wines"):
        self.address = address
        self.port = port
        self.index_recipe = index_recipe
        self.index_wine = index_wine
        self.es = Elasticsearch([{'host': address, 'port': port}])

    def GetRecipeByName(self, searchTerm):
        query = {"bool":{
            "must":[ # doit matcher
                {"match": { "title": {"query" : searchTerm, "fuzziness": 2}}}
            ],
        "filter":[ # option secondaire
            {"bool":{
                "should":[ # ou must
                    {'range': {'score': {'gte': 3., 'boost': 4.0}}}
                ]
            }
        }]}}

        res = self.es.search(index=self.index_recipe, query=query)
        result = []
        nb_result = 3
        if len(res['hits']['hits']) < 3:
            nb_result = len(res['hits']['hits'])

        for i in range(nb_result):
            result.append({"score": res['hits']['hits'][i]["_score"],
                           "recipes":res['hits']['hits'][i]["_source"]})
        return result

    def GetRecipeByIngredientAndName(self, searchName, searchIngredient):
        query = {"bool":{
            "must":[ # doit matcher
                {"match": { "title": {"query" : searchName, "fuzziness": 2}}},
                {"nested": {
                "path": "ingredients",
                "query": {
                    "bool":{
                        "must": [{"match": {"ingredients.ingredient": {"query" : searchIngredient, "fuzziness": 2}}}]
                    }
                }}}
            ]}}

        res = self.es.search(index=self.index_recipe, query=query)
        result = []
        nb_result = 1
        if len(res['hits']['hits']) < 3:
            nb_result = len(res['hits']['hits'])

        for i in range(nb_result):
            result.append({"score": res['hits']['hits'][i]["_score"],
                           "recipes":res['hits']['hits'][i]["_source"]})
        return result


    def GetRecipeByIngredients(self, searchTerms, type):

        ingredientsToFind = []
        for terms in searchTerms:
            ingredientsToFind.append({"nested": {
            "path": "ingredients",
            "query": {
                "bool":{
                    "must": {"match":{"ingredients.ingredient":{"query" : terms, "fuzziness": 2}}}
            }}}})

        query = {
            "bool":{
                "must":ingredientsToFind,
                "filter":[
                    {"bool":{
                        "must":[{"match": { "type": type}}]
                    }}
                ]
            }
        }
        # is sort by the number of ingredient
        sort = [{ "ingredients_count" : "asc"},"_score"]

        res = self.es.search(index=self.index_recipe, query=query, sort=sort)
        result = []
        nb_result = 3
        if len(res['hits']['hits']) < 3:
            nb_result = len(res['hits']['hits'])

        for i in range(nb_result):
            result.append({"score": res['hits']['hits'][i]["_score"],
                           "recipes":res['hits']['hits'][i]["_source"]})
        return result

    def GetRecipeByParams(self, searchMaxTerms, searchMinTerms, type):
        filters =[]
        for key, val in searchMaxTerms.items():
            filters.append({'range': {key : {'lte': val}}})

        for key, val in searchMinTerms.items():
            filters.append({'range': {key : {'gte': val}}})

        filters.append({"match": { "type": type}})

        query = {"bool":{
            "must":filters
        }}

        res = self.es.search(index=self.index_recipe, query=query)
        result = []
        nb_result = 3
        if len(res['hits']['hits']) < 3:
            nb_result = len(res['hits']['hits'])

        for i in range(nb_result):
            result.append({"score": res['hits']['hits'][i]["_score"],
                           "recipes":res['hits']['hits'][i]["_source"]})
        return result

    def GetWineByName(self, searchTerms):

        query = {
            "bool":{
                "must":[ # doit matcher
                    {"match": { "title": {"query" : searchTerms, "fuzziness": 2}}}
                ]
            }
        }

        res = self.es.search(index=self.index_wine, query=query)
        result = []
        nb_result = 3
        if len(res['hits']['hits']) < 3:
            nb_result = len(res['hits']['hits'])

        for i in range(nb_result):
            result.append({"score": res['hits']['hits'][i]["_score"],
                           "wines":res['hits']['hits'][i]["_source"]})
        return result

#        script_fields = {
#            "count":{
#                "script" : {
#                "source": "params['_source']['ingredients'].size() > params['limit_ingred']",
#                "lang": "painless",
#                "params": {
#                  "limit_ingred": len(searchTerms)
#                }
#            }}
#        }
