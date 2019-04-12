import sys
import csv
import os
from utils import find_distance_between_ingredients, \
    filter_existing_ingredients, find_stats
from db_accessor import get_ingredients, get_kmeans_clusters
from kmeans import get_all_kmeans_cluster_distances

def test_pca(ingredients_list):
    '''

    :param ingredients_list:
    :return:
    '''
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

def kmeans_test():
    '''

    :return:
    '''

    clusters_request = get_kmeans_clusters()
    if clusters_request["error"] != None:
        raise(clusters_request["error"])
    clusters = clusters_request["data"]
    cluster_distances = get_all_kmeans_cluster_distances()
    cluster_lengths = [len(cluster.ingredients) for cluster in clusters]
    kmeans_stats = find_stats(cluster_lengths)
    with open(os.getcwd() + '/app/test/kmeans_clusters.txt', 'w') as textfile:
        textfile.write("Size stats\n")
        textfile.write("-------------------------\n")
        textfile.write("Mean: " + str(kmeans_stats["mean"]))
        textfile.write("\n")
        textfile.write("Median: " + str(kmeans_stats["median"]))
        textfile.write("\n")
        textfile.write("St Dev: " + str(kmeans_stats["stdev"]))
        textfile.write("\n")
        textfile.write("Quartile 1: " + str(kmeans_stats["qt1"]))
        textfile.write("\n")
        textfile.write("Quartile 2: " + str(kmeans_stats["qt2"]))
        textfile.write("\n")
        textfile.write("-------------------------\n")
        textfile.write("\n")
        for x, cluster in enumerate(clusters):
            textfile.write("Cluster " + str(x) + "\n")
            textfile.write("-------------------------\n")
            textfile.write("Cluster size: " + str(len(cluster.ingredients)) + "\n")
            textfile.write(",".join(cluster.get_ingredient_strings()) + "\n")
            textfile.write("-------------------------\n")
            textfile.write("\n")
        textfile.write("\n")
        for i, entry in enumerate(cluster_distances):
            textfile.write("Distances from Cluster " + str(i) + "\n")
            textfile.write("-------------------------\n")
            for j, dist in enumerate(entry):
                textfile.write("Cluster " + str(j) + ": " + str(dist) + "\n")
            textfile.write("-------------------------\n")
            textfile.write("\n")

def create_database_snapshot():
    '''

    :return:
    '''
    min_distance_ingredient1 = ''
    min_distance_ingredient2 = ''
    max_distance_ingredient1 = ''
    max_distance_ingredient2 = ''
    min_distance = sys.maxint
    max_distance = 0
    total_distance = 0
    counter = 0
    get_ingredients_request = get_ingredients()
    if get_ingredients_request["error"] != None:
        raise(get_ingredients_request["error"])
    ingredients = get_ingredients_request["data"]
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