import math
from db_accessor import get_ingredients, get_ingredient

def distance_between_coordinates(coord1, coord2):
    if len(coord1) != len(coord2):
        raise(Exception("coordinates should be same length"))
    accum = 0
    for x in range(len(coord1)):
        accum += (coord1[x] - coord2[x])**2
    distance = math.sqrt(accum)
    return distance

def find_distance_between_ingredients(ingredient_1, ingredient_2):
    i1_obj = get_ingredient(ingredient_1)
    i2_obj = get_ingredient(ingredient_2)
    coord1 = i1_obj.get_coordinates()
    coord2 = i2_obj.get_coordinates()
    distance = distance_between_coordinates(coord1, coord2)
    # print(ingredient_1 + "-" + ingredient_2 + " distance: " + str(distance))
    return distance

def filter_existing_ingredients(ingredients_list):
    new_ingredients_list = []
    for ingredient in ingredients_list:
        if get_ingredient(ingredient) != None \
                and len(get_ingredient(ingredient)
                                .pca_coordinate) \
                > 0:
            new_ingredients_list.append(ingredient)
    return new_ingredients_list

def create_distance_matrix(ingredients_list):
    ingredients_list = filter_existing_ingredients(ingredients_list)
    print(ingredients_list)
    if len(ingredients_list) > 1:
        find_distance_between_ingredients(ingredients_list[0], ingredients_list[1])
    return []

def get_alphabet_columns():
    return ['a','b','c','d','e','f',
     'g','h','i','j','k','l',
     'm','n','o','p','q','r',
     's','t','u','v','w','x',
     'y','z']