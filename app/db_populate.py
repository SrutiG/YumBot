from spoonacular_api import find_random_recipes
from app import db, models
import unicodedata
from cooccur import add_recipe_ingredients_to_matrix, generate_new_matrix

def add_recipes_to_db(num_recipes):
    recipes = find_random_recipes(num_recipes, False)
    for r in recipes:
        if "title" not in r:
            continue
        try:
            has_recipe = models.Recipe.query.get(r["title"])
            if has_recipe:
                continue
            recipe = models.Recipe(name=r["title"])
            add_general(recipe, r)
            add_ingredients(r["title"], r["extendedIngredients"])
            add_steps(r["title"], r["analyzedInstructions"][0]["steps"])
            db.session.add(recipe)
            db.session.commit()
            add_recipe_ingredients_to_matrix(r["extendedIngredients"])
        except Exception as e:
            print(e)
            print("[Error] failed to add recipe " + r["title"])
            db.session.rollback()

def add_general(recipe_object, recipe_info):
    try:
        if "sourceName" in recipe_info:
            recipe_object.source = recipe_info["sourceName"]
        if "sourceUrl" in recipe_info:
            recipe_object.source_url = recipe_info["sourceUrl"]
        if "image" in recipe_info:
            recipe_object.image_url = recipe_info["image"]
        if "vegetarian" in recipe_info:
            recipe_object.vegetarian = recipe_info["vegetarian"]
        if "vegan" in recipe_info:
            recipe_object.vegan = recipe_info["vegan"]
        if "dairyFree" in recipe_info:
            recipe_object.dairy_free = recipe_info["dairyFree"]
        if "glutenFree" in recipe_info:
            recipe_object.gluten_free = recipe_info["glutenFree"]
        if "readyInMinutes" in recipe_info:
            recipe_object.prep_time = recipe_info["readyInMinutes"]
        if "servings" in recipe_info:
            recipe_object.servings = recipe_info["servings"]
    except Exception as e:
        raise(Exception(str(e) + " [Add General]"))

def add_ingredients(recipe_name, ingredients):
    try:
        for i in ingredients:
            has_ingredient = models.Ingredient.query.get(i["name"])
            if not has_ingredient:
                ingredient = models.Ingredient(name=i["name"])
                if "image" in i and i["image"] != None:
                    ingredient.image_url = "https://spoonacular.com/cdn/ingredients_100x100/" + i["image"]
                db.session.add(ingredient)
            has_recipe_ingredient = models.Recipe_Ingredient.query.get((recipe_name, i["name"]))
            if not has_recipe_ingredient:
                recipe_ingredient = models.Recipe_Ingredient(recipe_name=recipe_name, ingredient_name=i["name"])
                if "originalString" in i:
                    recipe_ingredient.original_string = i["originalString"]
                if "amount" in i:
                    recipe_ingredient.amount = i["amount"]
                if "unit" in i:
                    recipe_ingredient.unit = i["unit"]
                if "measures" in i:
                    if "us" in i["measures"]:
                        if "amount" in i["measures"]["us"]:
                            recipe_ingredient.us_amount = i["measures"]["us"]["amount"]
                        if "unitShort" in i["measures"]["us"]:
                            recipe_ingredient.us_unit = i["measures"]["us"]["unitShort"]
                    if "metric" in i["measures"]:
                        if "amount" in i["measures"]["metric"]:
                            recipe_ingredient.metric_amount = i["measures"]["metric"]["amount"]
                        if "unitShort" in i["measures"]["metric"]:
                            recipe_ingredient.metric_unit = i["measures"]["metric"]["unitShort"]
                # TODO calculate standard amount
                db.session.add(recipe_ingredient)
    except Exception as e:
        raise(Exception(str(e) + " [Add Ingredients]"))

def add_steps(recipe_name, steps):
    try:
        for s in steps:
            s["step"] = unicodedata.normalize('NFKD', s["step"]).encode('ascii','ignore')
            recipe_step = models.Recipe_Step(recipe_name=recipe_name, step=s["step"])
            recipe_step.step_number = s["number"]
            if "ingredients" in s:
                for i in s["ingredients"]:
                    recipe_step_ingredient = models.Recipe_Step_Ingredient(
                        recipe_name=recipe_name,
                        step=s["step"],
                        ingredient_name=i["name"]
                    )
                    db.session.add(recipe_step_ingredient)
            db.session.add(recipe_step)
    except Exception as e:
        raise(Exception(str(e) + " [Add Steps]"))

def clear_db(max_count=None, save_matrix=True):
    try:
        counter = 0
        recipes = models.Recipe.query.all()
        ingredients = models.Ingredient.query.all()
        for recipe in recipes:
            if max_count and counter > max_count:
                break
            counter += 1
            db.session.delete(recipe)
        for ingredient in ingredients:
            if len(ingredient.recipes) == 0:
                db.session.delete(ingredient)
        if not save_matrix:
            generate_new_matrix()
        db.session.commit()
    except Exception as e:
        print(e)
