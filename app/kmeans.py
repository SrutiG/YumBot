'''

'''
from db_accessor import get_ingredients, \
    get_ingredient, set_ingredient_cluster, \
    delete_kmeans_clusters, add_kmeans_cluster,\
    add_kmeans_cluster_coordinate
from sklearn.cluster import KMeans
import numpy as np
from utils import *
import os

def get_kmeans_cluster_distances(kmeans_clusters):
    '''

    :param kmeans_clusters:
    :return:
    '''
    cluster_distances = {}
    for i1, c1 in enumerate(kmeans_clusters):
        for i2, c2 in enumerate(kmeans_clusters):
            if (i1,i2) not in cluster_distances \
                    and (i2, i1) not in cluster_distances \
                    and i1 != i2:
                cluster_distances[(i1,i2)] = distance_between_coordinates(c1, c2)
    return cluster_distances

def kmeans_test(clusters=15):
    '''

    :param clusters:
    :return:
    '''
    # ingredients: all ingredients in the database
    ingredients = get_ingredients()
    # keys: the ingredients which have pca coordinates
    keys = []
    # coordinates: coordinates of each key corresponding to the index of the key
    coordinates = []
    # cluster_values: indices correspond to cluster number (e.g. index 0 has cluster 0)
    # contains ingredients at each cluster (e.g. if index 0 has ['bread', 'butter']
    # that means that bread and butter are in cluster 0
    cluster_values = []

    columns = get_alphabet_columns()
    delete_kmeans_clusters()
    for _ in range(clusters):
        cluster_values.append([])
    for i in ingredients:
        if len(i.pca_coordinates) > 0:
            keys.append(i.name)
            coordinates.append(i.get_coordinates_list())
    if len(keys) == 0:
        return
    np_array = np.array(coordinates)
    kmeans = KMeans(n_clusters=clusters, random_state=0).fit(np_array)
    kmeans_arr = kmeans.predict(np_array)
    cluster_distances = get_kmeans_cluster_distances(kmeans.cluster_centers_)
    for i, cluster in enumerate(kmeans.cluster_centers_):
        add_kmeans_cluster(i)
        for j, value in enumerate(cluster):
            add_kmeans_cluster_coordinate(i, columns[j], value)
    for x in range(len(keys)):
        set_ingredient_cluster(keys[x], kmeans_arr[x])
        cluster_values[kmeans_arr[x]].append(keys[x])
    with open(os.getcwd() + '/app/test/kmeans_clusters.txt', 'w') as textfile:
        for row in range(len(cluster_values)):
            textfile.write("cluster " + str(row) + ": ")
            textfile.write(",".join(cluster_values[row]))
            textfile.write("\n")
        for key in cluster_distances:
            textfile.write("Cluster distance "
                           + str(key) + ": "
                           + str(cluster_distances[key])
                           + "\n")