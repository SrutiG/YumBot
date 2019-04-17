'''

'''
import random
from db_accessor import get_kmeans_clusters, get_ingredient
from utils import get_recipe_format, filter_existing_ingredients,\
    get_random_string
from kmeans import cluster_size_upper_threshold, find_closest_cluster,\
    find_closest_clusters_under_threshold

class YumBot:

    def __init__(self):
        get_cluster_request = get_kmeans_clusters()
        if get_cluster_request["error"] != None:
            print(get_cluster_request["error"])
            print(get_cluster_request["message"])
            self.clusters = None
        else:
            self.clusters = get_cluster_request["data"]
            self.closest_clusters = [None] * len(self.clusters)
            for c in self.clusters:
                self.closest_clusters[c.cluster_number] = \
                    find_closest_clusters_under_threshold(c.cluster_number)


    def find_random_valid_cluster_ingredients(self):
        '''

        :return:
        '''
        clusters = self.clusters
        count = 0
        ingredients = []
        cluster = random.randint(0, len(clusters) - 1)
        while len(ingredients) < 4 and count < len(self.clusters):
            ingredients += self.clusters[cluster].ingredients
            count += 1
            cluster = find_closest_cluster(cluster)
        return clusters[cluster].ingredients


    def get_random_recipe(self):
        '''

        :return:
        '''
        recipe = get_recipe_format()
        recipe_name = []
        try:
            ingredients = self.find_random_valid_cluster_ingredients()
            num_ingredients = random.randint(2, min(len(ingredients), 15))
            used_ingredients = set()
            for x in range(num_ingredients):
                found_ingredient = False
                while found_ingredient == False:
                    ingredient = ingredients[random.randint(0, len(ingredients) - 1)]
                    if ingredient.name in used_ingredients:
                        continue
                    found_ingredient = True
                    used_ingredients.add(ingredient.name)
                    recipe_name.append(ingredient.name)
                    amount = ingredient.recipes[random.randint(
                        0, len(ingredient.recipes) - 1
                    )].original_string
                    recipe["ingredients"].append(amount)
            recipe["name"] = ", ".join(recipe_name)
            recipe["image"] = "/static/images/stock_recipe_image.jpg"
            recipe["id"] = get_random_string()
            return recipe
        except Exception as e:
            print(e)
            return None

    def get_ingredient_throw_error(self, ingredient_name):
        '''

        :param ingredient_name:
        :return:
        '''
        ingredient_request = get_ingredient(ingredient_name)
        if ingredient_request["error"]:
            raise(ingredient_request["error"])
        return ingredient_request["data"]

    def are_ingredients_compatible(self, ingredient_name, ingredient_list):
        '''

        :param ingredient_name:
        :param ingredient_list:
        :return:
        '''
        try:
            ingredient = self.get_ingredient_throw_error(ingredient_name)
            threshold = cluster_size_upper_threshold()
            for i2 in ingredient_list:
                if i2 == ingredient_name:
                    return False
                compare_ing = self.get_ingredient_throw_error(i2)
                if ingredient.cluster_number != compare_ing.cluster_number:
                    size_cluster_1 = len(ingredient.kmeans_cluster.ingredients)
                    size_cluster_2 = len(compare_ing.kmeans_cluster.ingredients)
                    if size_cluster_1 > threshold and size_cluster_2 > threshold:
                        return False
                    elif size_cluster_1 > threshold and size_cluster_2 < threshold:
                        if ingredient.cluster_number not in self.closest_clusters[compare_ing.cluster_number]:
                            return False
                    elif size_cluster_1 < threshold and size_cluster_2 > threshold:
                        if compare_ing.cluster_number not in self.closest_clusters[ingredient.cluster_number]:
                            return False
                    else:
                        if compare_ing.cluster_number not in self.closest_clusters[ingredient.cluster_number]:
                            return False
            return True
        except Exception as e:
            print("[Error] Error checking if ingredients are compatible")
            raise(e)

    def create_recipes_from_ingredients(self, ingredients_list):
        '''

        :param ingredients_list:
        :return:
        '''
        try:
            ingredients_list = filter_existing_ingredients(ingredients_list)
            if len(ingredients_list) < 2:
                return None
            recipes = []
            existing_recipes = set()
            for i in ingredients_list:
                compatible_check = []
                for j in ingredients_list:
                    compatible_check.append(j)
                    if self.are_ingredients_compatible(i, compatible_check):
                        if self.hash_recipe_name(compatible_check + [i]) not in existing_recipes:
                            recipes.append(
                                self.create_recipe_from_ingredients(compatible_check + [i])
                            )
                            existing_recipes.add(self.hash_recipe_name(compatible_check + [i]))
                    else:
                        compatible_check.remove(j)
            return recipes
        except Exception as e:
            print(e)
            print("[Error] Error creating recipes from ingredients list")
            return []

    def hash_recipe_name(self, ingredients_list):
        '''

        :param ingredients_list:
        :return:
        '''
        hash_value = 0
        for i in ingredients_list:
            hash_value += 1000
            for c in i:
                hash_value += ord(c)**3
        return hash_value

    def get_ingredient_amount(self, ingredient_name, other_ingredients=[]):
        '''
        Return the amount of the ingredient to put in the recipe
        TODO: implement this properly instead of just returning a random amount
        :param ingredient_name:
        :return: the amount of the ingredient as a string
        '''
        try:
            ingredient = self.get_ingredient_throw_error(ingredient_name)
            return ingredient.recipes[random.randint(
                0, len(ingredient.recipes) - 1
            )].original_string
        except Exception as e:
            print(e)
            print("[Error] error getting ingredient amount")
            return None

    def create_recipe_from_ingredients(self, compatible_ingredients_list):
        '''

        :param compatible_ingredients_list:
        :return:
        '''
        recipe = get_recipe_format()
        for ingredient in compatible_ingredients_list:
            recipe["ingredients"].append(self.get_ingredient_amount(ingredient))
        recipe["name"] = ", ".join(compatible_ingredients_list)
        recipe["image"] = "/static/images/stock_recipe_image.jpg"
        recipe["id"] = get_random_string()
        return recipe
