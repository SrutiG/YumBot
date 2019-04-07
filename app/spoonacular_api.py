import requests
import os

api_url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
api_host = "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
api_key = os.environ["SPOONACULAR_API_KEY"]
require_instructions = "&instructionsRequired=1"
headers = {"X-RapidAPI-Host":api_host,"X-RapidAPI-key":api_key}

def find_random_recipes(numRecipes, formatted=True):
    new_recipes = []
    url = api_url + "/recipes/random?number=" + str(numRecipes) + require_instructions
    try:
        response = requests.get(url, headers=headers)
        for recipe in response.json()["recipes"]:
            if formatted:
                new_recipes.append(format_spoonacular_recipe(recipe))
            else:
                new_recipes.append(recipe)
    except Exception as e:
        print e
        print "[Error] error getting recipe data"
    return new_recipes

def search_recipes_by_ingredient(ingredient_list):
    new_recipes = []
    num_recipes = "8"
    ingredients = ",".join(ingredient_list)
    url = api_url + "/recipes/findByIngredients?number=" \
          + num_recipes + "&ingredients=" + ingredients
    try:
        response = requests.get(url, headers=headers)
        for recipe in response.json():
            recipe_information = get_recipe_information(recipe["id"])
            new_recipe = format_spoonacular_recipe(recipe_information)
            new_recipe["used_ingredient_count"] = recipe["usedIngredientCount"]
            new_recipes.append(new_recipe)
    except Exception as e:
        print e
        print "[Error] error getting recipe data when searching by ingredient"
    return new_recipes

def get_recipe_information(id):
    url = api_url + "/recipes/" + str(id) + "/information"
    recipe = ""
    try:
        response = requests.get(url, headers=headers)
        recipe = response.json()
    except Exception as e:
        print e
        print "[Error] error getting recipe information"
    return recipe

def format_spoonacular_recipe(recipe):
    new_recipe = {"ingredients":[], "steps":[]}
    new_recipe["name"] = recipe["title"]
    new_recipe["id"] = recipe["id"]
    if "ready_in_minutes" in recipe:
        new_recipe["prep_time"] = recipe["ready_in_minutes"]
    if "image" in recipe:
        new_recipe["image"] = recipe["image"]
    for ing in recipe["extendedIngredients"]:
        new_recipe["ingredients"].append(ing["originalString"])
    if "analyzedInstructions" in recipe:
        for step in recipe["analyzedInstructions"][0]["steps"]:
            new_recipe["steps"].append(step["step"])
    else:
        new_recipe["steps"] = recipe["instructions"].split("\n")
    print new_recipe
    return new_recipe



