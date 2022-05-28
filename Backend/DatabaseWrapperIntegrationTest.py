#!/usr/bin/env python3
from DatabaseWrapper import DatabaseWrapper

dbw = DatabaseWrapper()

print("----------------------------------------------\nTest GET RECIPE BY NAME")
result_data = dbw.GetRecipeByName("Tarte au poire")
print(result_data)

print("\n----------------------------------------------\nTest GET RECIPE BY INGREDIENTS")
result_data = dbw.GetRecipeByIngredients(["sucre", "oeuf"], "dessert")
print(result_data)

#print("\n----------------------------------------------\nTest GET RECIPE BY PARAM")
#result_data = dbw.GetRecipeByParams({"duration":120,"nb_people":4, "score":5}, {"duration":30, "nb_people":1, "score":2}, "dessert")
#print(result_data)

#print("\n----------------------------------------------\nTest GET RECIPE BY NAME AND INGREDIENT")
#result_data = dbw.GetRecipeByIngredientAndName("tarte", "pomme")
#print(result_data)

#print("\n----------------------------------------------\nTest GET WINE BY NAME")
#result_data = dbw.GetWineByName("sauvignon blanc")
#print(result_data)
