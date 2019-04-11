import sys
import csv
import os
from utils import find_distance_between_ingredients, filter_existing_ingredients
from db_accessor import get_ingredients

def test_pca(ingredients_list):
    ingredients_list = filter_existing_ingredients(ingredients_list)
    print(ingredients_list)
    if len(ingredients_list) > 1:
        for i1 in ingredients_list:
            for i2 in ingredients_list:
                if i1 != i2:
                    find_distance_between_ingredients(i1, i2)
    else:
        print("Sorry an ingredient isn't in the database")
    return []

def create_database_snapshot():
    min_distance_ingredient1 = ''
    min_distance_ingredient2 = ''
    max_distance_ingredient1 = ''
    max_distance_ingredient2 = ''
    min_distance = sys.maxint
    max_distance = 0
    total_distance = 0
    counter = 0
    ingredients = get_ingredients()
    if ingredients == None:
        return
    pca_matrix_keys = ['']
    for ingredient in ingredients:
        if len(ingredient.pca_coordinates) > 0:
            pca_matrix_keys.append(ingredient.name.encode('utf-8'))
    with open(os.getcwd() + '/app/test/pca_snapshot.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(pca_matrix_keys)
        for i1 in pca_matrix_keys[1:]:
            values = [i1]
            i1 = i1.decode("utf-8")
            for i2 in pca_matrix_keys[1:]:
                i2 = i2.decode("utf-8")

                distance = find_distance_between_ingredients(i1, i2)
                if distance < min_distance and distance > 0:
                    min_distance = distance
                    min_distance_ingredient1 = i1
                    min_distance_ingredient2 = i2
                if distance > max_distance:
                    max_distance = distance
                    max_distance_ingredient1 = i1
                    max_distance_ingredient2 = i2
                if distance > 0:
                    total_distance += distance
                    counter += 1
                values.append(distance)
            csvwriter.writerow(values)
    csvfile.close()
    with open(os.getcwd() + '/app/test/pca_stats.txt', 'w') as textfile:
        textfile.write("Minimum distance between ingredients: "
                       + str(min_distance) + " ("
                       + min_distance_ingredient1 + ", "
                       + min_distance_ingredient2 + ")\n")
        textfile.write("Maximum distance between ingredients: "
                       + str(max_distance) + " ("
                       + max_distance_ingredient1 + ", "
                       + max_distance_ingredient2 + ")\n")
        textfile.write("Avg distance between ingredients: "
                       + str(total_distance/counter) + "\n")
        textfile.write("Total number of ingredients: "
                       + str(len(ingredients)))