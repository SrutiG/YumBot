'''
Title
-----
spoonacular_api.py

Description
-----------
Access methods for the Spoonacular API
'''
import requests
import os

api_url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
api_host = "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
api_key = os.environ["SPOONACULAR_API_KEY"]
require_instructions = "&instructionsRequired=1"
headers = {"X-RapidAPI-Host":api_host,"X-RapidAPI-key":api_key}

def find_random_recipes(numRecipes, formatted=True):
    '''
    Get random recipes
    :param numRecipes: number of random recipes to get
    :param formatted: format in application default recipe format
    :return: array of recipe objects
    '''
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
        print(e)
        print("[Error] error getting recipe data")
    return new_recipes

def search_recipes_by_ingredient(ingredient_list):
    '''
    find recipes containing certain ingredients
    :param ingredient_list: a list of ingredient names
    :return: list of recipe objects
    '''
    new_recipes = []
    num_recipes = "4"
    ingredients = ",".join(ingredient_list)
    url = api_url + "/recipes/findByIngredients?number=" \
          + num_recipes + "&ingredients=" + ingredients \
          + "&ranking=2&ignorePantry=false"
    try:
        response = requests.get(url, headers=headers)
        recipe_names = set()
        for recipe in response.json():
            if recipe["title"] in recipe_names:
                continue;
            recipe_information = get_recipe_information(recipe["id"])
            new_recipe = format_spoonacular_recipe(recipe_information)
            new_recipe["used_ingredient_count"] = recipe["usedIngredientCount"]
            new_recipe["missed_ingredient_count"] = recipe["missedIngredientCount"]
            new_recipes.append(new_recipe)
            recipe_names.add(new_recipe["name"])
    except Exception as e:
        print(e)
        print("[Error] error getting recipe data when searching by ingredient")
    return new_recipes

def get_recipe_information(id):
    '''
    get Spoonacular API recipe information by recipe ID
    :param id: the Spoonacular API recipe ID
    :return: recipe object
    '''
    url = api_url + "/recipes/" + str(id) + "/information"
    recipe = ""
    try:
        response = requests.get(url, headers=headers)
        recipe = response.json()
    except Exception as e:
        print(e)
        print("[Error] error getting recipe information")
    return recipe

def format_spoonacular_recipe(recipe):
    '''
    Spoonacular API recipe formatted in general recipe
    format used throughout application
    :param recipe: original recipe from API
    :return: recipe object (formatted)
    '''
    new_recipe = {"ingredients":[], "steps":[]}
    new_recipe["name"] = recipe["title"]
    new_recipe["id"] = recipe["id"]
    new_recipe["yumbot"] = False
    if "ready_in_minutes" in recipe:
        new_recipe["prep_time"] = recipe["ready_in_minutes"]
    if "servings" in recipe:
        new_recipe["servings"] = recipe["servings"]
    if "image" in recipe:
        new_recipe["image"] = recipe["image"]
    for ing in recipe["extendedIngredients"]:
        new_recipe["ingredients"].append(ing["originalString"])
    if "analyzedInstructions" in recipe:
        for step in recipe["analyzedInstructions"][0]["steps"]:
            new_recipe["steps"].append(step["step"])
    else:
        new_recipe["steps"] = recipe["instructions"].split("\n")
    return new_recipe



