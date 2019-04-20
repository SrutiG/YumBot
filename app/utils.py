'''
Title
-----
utils.py

Description
-----------
Helper functions and universal data
'''
import math
from db_accessor import get_ingredients, get_ingredient
import statistics as stat
import random

def find_stats(lst):
    '''
    find important statistical data
    for a set of numbers
    :param lst: an array of floats or integers
    :return: a dictionary containing mean, median,
    stdev, first, and second quartile.
    '''
    lst.sort()
    return {
        "mean": stat.mean(lst),
        "median": stat.median(lst),
        "stdev": stat.stdev(lst),
        "qt1": stat.median(lst[0:len(lst)//2]),
        "qt2": stat.median(lst[len(lst)//2: len(lst)])
    }

def distance_between_coordinates(coord1, coord2):
    '''
    find the difference between two coordinates
    in any dimension
    :param coord1: the first coordinate as either a tuple or list
    of floats or integers
    :param coord2: the second coordinate as either a tuple or list
    of floats or integers
    :return: distance a float
    '''
    if len(coord1) != len(coord2):
        raise(Exception("coordinates should be same length"))
    accum = 0
    for x in range(len(coord1)):
        accum += (coord1[x] - coord2[x])**2
    distance = math.sqrt(accum)
    return distance

def find_distance_between_ingredients(ingredient_1, ingredient_2, print_values=False):
    '''
    find the distance between two ingredients
    :param ingredient_1: the first ingredient name
    :param ingredient_2: the second ingredient name
    :param print_values: whether or not to print the distance
    between the ingredients
    :return: distance between ingredients as a float
    '''
    get_ingredient1_request = get_ingredient(ingredient_1)
    if get_ingredient1_request["error"] != None:
        raise(get_ingredient1_request["error"])
    i1_obj = get_ingredient1_request["data"]
    get_ingredient2_request = get_ingredient(ingredient_2)
    if get_ingredient2_request["error"] != None:
        raise(get_ingredient2_request["error"])
    i2_obj = get_ingredient2_request["data"]
    coord1 = i1_obj.get_coordinates()
    coord2 = i2_obj.get_coordinates()
    distance = distance_between_coordinates(coord1, coord2)
    if print_values:
        print(ingredient_1 + "-" + ingredient_2 + " distance: " + str(distance))
    return distance

def filter_existing_ingredients(ingredients_list):
    '''
    from a list of ingredient names, filter out the ones
    which either don't exist in the database at all, or
    don't have PCA coordinates.
    :param ingredients_list: a list of ingredient names
    :return: a new list of filtered ingredient names
    '''
    new_ingredients_list = []
    for ingredient in ingredients_list:
        get_ingredient_request = get_ingredient(ingredient)
        if get_ingredient_request["error"] != None:
            print(get_ingredient_request["error"])
            continue
        i_obj = get_ingredient_request["data"]
        if i_obj != None \
            and len(i_obj.pca_coordinates) > 0:
            new_ingredients_list.append(ingredient)
    return new_ingredients_list

def get_alphabet_columns():
    '''
    Get every letter of the alphabet in a list
    to be used as columns for coordinates
    :return: lowercase alphabet as list
    '''
    return ['a','b','c','d','e','f',
     'g','h','i','j','k','l',
     'm','n','o','p','q','r',
     's','t','u','v','w','x',
     'y','z']

def get_recipe_format():
    '''
    Get the general recipe format for all recipes
    :return: a dictionary recipe object
    '''
    # NOTE: optional columns: prep_time, servings, image, ingredients, images
    return {
        "name":"",
        "id":"",
        "yumbot":True,
        "image":"",
        "ingredients":[],
        "steps":[]
    }

def get_random_string():
    '''
    generate a random string from lowercase alphabet
     of length 20
    :return: random string
    '''
    values = get_alphabet_columns()
    random_string = ""
    for _ in range(20):
        random_string += values[random.randint(0, 25)]
    return random_string
