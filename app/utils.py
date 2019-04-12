'''

'''
import math
from db_accessor import get_ingredients, get_ingredient
import statistics as stat
import random

def find_stats(lst):
    '''

    :param lst:
    :return:
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

    :param coord1:
    :param coord2:
    :return:
    '''
    if len(coord1) != len(coord2):
        raise(Exception("coordinates should be same length"))
    accum = 0
    for x in range(len(coord1)):
        accum += (coord1[x] - coord2[x])**2
    distance = math.sqrt(accum)
    return distance

def find_distance_between_ingredients(ingredient_1, ingredient_2):
    '''

    :param ingredient_1:
    :param ingredient_2:
    :return:
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
    # print(ingredient_1 + "-" + ingredient_2 + " distance: " + str(distance))
    return distance

def filter_existing_ingredients(ingredients_list):
    '''

    :param ingredients_list:
    :return:
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

def create_distance_matrix(ingredients_list):
    '''

    :param ingredients_list:
    :return:
    '''
    ingredients_list = filter_existing_ingredients(ingredients_list)
    print(ingredients_list)
    if len(ingredients_list) > 1:
        find_distance_between_ingredients(ingredients_list[0], ingredients_list[1])
    return []

def get_alphabet_columns():
    '''

    :return:
    '''
    return ['a','b','c','d','e','f',
     'g','h','i','j','k','l',
     'm','n','o','p','q','r',
     's','t','u','v','w','x',
     'y','z']

def get_recipe_format():
    '''

    :return:
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

    :return:
    '''
    values = get_alphabet_columns()
    random_string = ""
    for _ in range(20):
        random_string += values[random.randint(0, 25)]
    return random_string