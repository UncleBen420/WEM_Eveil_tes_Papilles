#!/usr/bin/env python3

## @package Backend
#  This is the implementation of the backend for the projet "Eveil tes papilles" it's communicate with a machine learning model and an elastic search database
#

from flask import Flask, jsonify, request
from waitress import serve
from DatabaseWrapper import DatabaseWrapper
from Model.EveilleTesPapilles import EveilleTesPapilles

# Other used objects
app = Flask("Eveil_Tes_Papilles")

recipeFilesName = ['Model/entree.jl','Model/plat.jl','Model/dessert.jl','Model/red_wines.jl','Model/white_wines.jl']

model = EveilleTesPapilles("Model/EveilleTesPapilles.word2vec.wordvectors", recipeFilesName)
databaseWrapper = DatabaseWrapper()

## function describing the comportement of the REST Api called on the index
@app.route('/')
def index():
    return jsonify({'Something is happening!?!?!': 'I AM ALIVE BITCH!!!!'})

## function describing the comportement of the REST Api called /Recipes/ByIngredients/
#  @param type used while calling the Api expect a string for exemple: "dessert"
#  @param ingredients used while calling the Api expect an array of string for exemple: ["farine", "sucre"]
#  It allow the user to get 3 recipes from a list of ingredients. the results are sorted by number of ingredients (asc)
@app.route('/Recipes/ByIngredients/', methods=['GET'])
def recipeByIngredients():
    args = request.args.to_dict()
    ingredients = args["ingredients"].split(',')
    type_of = args["type"]

    recipes = databaseWrapper.GetRecipeByIngredients(ingredients, type_of)
    return jsonify(recipes)

## function describing the comportement of the REST Api called /Recipes/ByParam/
#  @param type used while calling the Api expect a string for exemple: "dessert"
#  @param duration used while calling the Api expect an array of 2 value for exemple: "1,2" where the first is the min value and the second the max value
#  @param nb_people used while calling the Api expect an array of 2 value for exemple: "1,2" where the first is the min value and the second the max value
#  @param score used while calling the Api expect an array of 2 value for exemple: "1,2" where the first is the min value and the second the max value
#  It allow the user to get 3 recipes that match a list of parameters for exemple the duration of the recipe,...
@app.route('/Recipes/ByParam/', methods=['GET'])
def recipeByParam():
    args = request.args.to_dict()
    min_values = {}
    max_values = {}
    for key in args:
        if key == "type":
            continue
        values = args[key].split(',')
        min_values[key] = values[0]
        max_values[key] = values[1]

    type_of = args["type"]
    recipes = databaseWrapper.GetRecipeByParams(max_values, min_values, type_of)
    return jsonify(recipes)

## function describing the comportement of the REST Api called /Recipes/Suggestion/
#  @param recipe used while calling the Api expect a string formed in this way word_word_word
#  It allow the user to get a suggestion of ingredient that can possibily goes well with a recipe
@app.route('/Recipes/Suggestion/', methods=['GET'])
def recipeSuggestion():
    args = request.args.to_dict()
    recipe = " ".join(args["recipe"].split("_"))
    result = databaseWrapper.GetRecipeByName(recipe)
    # if there is no recipe matching
    if len(result) > 0:
        ingredients = result[0]["recipes"]["ingredients"]
        list_ingredient = []
        for ingr in ingredients:
            for s in ingr["ingredient"].split():
                list_ingredient.append(s)

        print(list_ingredient)
        # TODO
        pred = model.predictSuggestion(list_ingredient)
        #model (predict suggestion)
    return jsonify({'ingredients': pred})

## function describing the comportement of the REST Api called /Recipes/Replacement/
#  @param recipe used while calling the Api expect a string formed in this way word_word_word
#  @param ingredient used while calling the Api expect a string formed in this way word_word_word
#  It allow the user to get a suggestion of ingredient that can replace an ingredient in a recipe
@app.route('/Recipes/Replacement/', methods=['GET'])
def recipeReplacement():
    args = request.args.to_dict()
    recipe = " ".join(args["recipe"].split("_"))
    ingredient = " ".join(args["ingredient"].split("_"))
    result = databaseWrapper.GetRecipeByIngredientAndName(recipe, ingredient)
    # if there is no recipe matching
    if len(result) > 0:
        steps = result[0]["recipes"]["steps"]
        print(steps)
        # TODO
        pred = model.predictIngredient(steps,ingredient)
        # model (predict ingredient)
    return jsonify({'ingredient': pred})

## function describing the comportement of the REST Api called /Wines/Pairing/
#  @param recipe used while calling the Api expect a string formed in this way word_word_word
#  It allow the user to get a suggestion of a wine that can pair well with a recipe
@app.route('/Wines/Pairing/', methods=['GET'])
def recipeToPredictWine():
    args = request.args.to_dict()
    recipe = " ".join(args["recipe"].split("_"))
    result = databaseWrapper.GetRecipeByName(recipe)
    # if there is no recipe matching
    if len(result) > 0:
        ingredients = result[0]["recipes"]["ingredients"]
        steps = result[0]["recipes"]["steps"]
        print(ingredients)
        print(steps)
        # TODO
        # model (predict wine pairing wine)
    return jsonify({'wine': 'not implemented yet'})

## function describing the comportement of the REST Api called /Recipes/Pairing/
#  @param wine used while calling the Api expect a string formed in this way word_word_word
#  It allow the user to get a suggestion of a recipe that can pair well with a wine
@app.route('/Recipes/Pairing/', methods=['GET'])
def WineToPredictRecipe():
    args = request.args.to_dict()
    wine = " ".join(args["wine"].split("_"))
    result = databaseWrapper.GetWineByName(wine)
    # if there is no recipe matching
    if len(result) > 0:
        pairsWellWith = result[0]["wines"]["pairsWellWith"]
        print(pairsWellWith)
        # TODO
        # model (predict wine pairing recipe)
    return jsonify({'recipe': 'not implemented yet'})

if __name__ == "__main__":
    host = "localhost"
    port = 8080

    serve(app, host=host, port=port)
