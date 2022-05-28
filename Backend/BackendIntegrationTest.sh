#!/bin/bash

echo "------------------------------------------------------------------------------"
echo "recipeByIngredients"
curl "http://localhost:8080/Recipes/ByIngredients/?type=dessert&ingredients=whisky,farine"
echo "------------------------------------------------------------------------------"

echo "------------------------------------------------------------------------------"
echo "recipeByParam"
curl "http://localhost:8080/Recipes/ByParam/?type=dessert&duration=30,120&nb_people=2,6&score=2,4"
echo "------------------------------------------------------------------------------"

echo "------------------------------------------------------------------------------"
echo "recipeSuggestion"
curl "http://localhost:8080/Recipes/Suggestion/?recipe=tarte_au_pomme"
echo "------------------------------------------------------------------------------"

echo "------------------------------------------------------------------------------"
echo "recipeReplacement"
curl "http://localhost:8080/Recipes/Replacement/?recipe=flan_au_chocolat&ingredient=chocolat"
echo "------------------------------------------------------------------------------"

echo "------------------------------------------------------------------------------"
echo "recipeToPredictWine"
curl "http://localhost:8080/Wines/Pairing/?recipe=flan_au_chocolat"
echo "------------------------------------------------------------------------------"

echo "------------------------------------------------------------------------------"
echo "WineToPredictRecipe"
curl "http://localhost:8080/Recipes/Pairing/?wine=lavaux"
echo "------------------------------------------------------------------------------"
