'''

'''
from db_accessor import get_ingredients, \
    get_ingredient, set_ingredient_cluster, \
    delete_kmeans_clusters, add_kmeans_cluster,\
    add_kmeans_cluster_coordinate, get_kmeans_clusters,\
    get_kmeans_cluster
from sklearn.cluster import KMeans
import numpy as np
from utils import *
import os
import sys

def get_all_kmeans_cluster_distances():
    '''

    :return:
    '''
    kmeans_clusters_request = get_kmeans_clusters()
    if kmeans_clusters_request["error"]:
        print(kmeans_clusters_request["error"])
        return None
    kmeans_clusters = kmeans_clusters_request["data"]
    cluster_distances = [None] * len(kmeans_clusters)
    for c1 in kmeans_clusters:
        distances = [None] * len(kmeans_clusters)
        for c2 in kmeans_clusters:
            distances[c2.cluster_number] = distance_between_coordinates(
                c1.get_coordinates(), c2.get_coordinates()
            )
        cluster_distances[c1.cluster_number] = distances
    return cluster_distances

def find_closest_cluster(cluster_number):
    '''

    :param cluster_number:
    :return:
    '''
    cluster_request = get_kmeans_cluster(cluster_number)
    clusters_request = get_kmeans_clusters()
    closest_cluster = cluster_number
    min_distance = sys.maxint
    if cluster_request["error"]:
        print(cluster_request["error"])
        return closest_cluster
    if clusters_request["error"]:
        print(clusters_request["error"])
        return closest_cluster
    cluster = cluster_request["data"]
    clusters = clusters_request["data"]
    cluster_coordinates = cluster.get_coordinates()
    if not cluster:
        return closest_cluster
    for c in clusters:
        if cluster.cluster_number != c.cluster_number:
            distance = distance_between_coordinates(
                cluster_coordinates, c.get_coordinates()
            )
            if distance < min_distance:
                min_distance = distance
                closest_cluster = c.cluster_number
    return closest_cluster

def smallest_cluster_size():
    '''

    :return:
    '''
    clusters_request = get_kmeans_clusters()
    min_size = sys.maxint
    if clusters_request["error"]:
        print(clusters_request["error"])
        return min_size
    clusters = clusters_request["data"]
    for cluster in clusters:
        if len(cluster.ingredients) < min_size:
            min_size = len(cluster.ingredients)
    return min_size

def largest_cluster_size():
    '''

    :return:
    '''
    clusters_request = get_kmeans_clusters()
    max_size = 0
    if clusters_request["error"]:
        print(clusters_request["error"])
        return max_size
    clusters = clusters_request["data"]
    for cluster in clusters:
        if len(cluster.ingredients) < max_size:
            max_size = len(cluster.ingredients)
    return max_size

def cluster_size_upper_threshold():
    '''

    :return:
    '''
    clusters_request = get_kmeans_clusters()
    if clusters_request["error"]:
        print(clusters_request["error"])
        return 0
    clusters = clusters_request["data"]
    cluster_lengths = [len(cluster.ingredients) for cluster in clusters]
    kmeans_stats = find_stats(cluster_lengths)
    return kmeans_stats["mean"]


def create_kmeans_clusters(clusters=10):
    '''

    :param clusters:
    :return:
    '''
    try:
        # ingredients: all ingredients in the database
        get_ingredients_request = get_ingredients()
        if get_ingredients_request["error"] != None:
            raise(get_ingredients_request["error"])
        ingredients = get_ingredients_request["data"]
        # keys: the ingredients which have pca coordinates
        keys = []
        # coordinates: coordinates of each key corresponding to the index of the key
        coordinates = []
        columns = get_alphabet_columns()
        delete_request = delete_kmeans_clusters()
        if delete_request["error"] != None:
            raise(delete_request["error"])
        for i in ingredients:
            if len(i.pca_coordinates) > 0:
                keys.append(i.name)
                coordinates.append(i.get_coordinates_list())
        if len(keys) == 0:
            print("[Info] No ingredients with pca coordinates, ending process")
            return
        np_array = np.array(coordinates)
        kmeans = KMeans(n_clusters=clusters, random_state=0).fit(np_array)
        kmeans_arr = kmeans.predict(np_array)
        for i, cluster in enumerate(kmeans.cluster_centers_):
            add_cluster_request = add_kmeans_cluster(i)
            if add_cluster_request["error"] != None:
                raise(add_cluster_request["error"])
            for j, value in enumerate(cluster):
                add_coordinate_request = add_kmeans_cluster_coordinate(i, columns[j], value)
                if add_coordinate_request["error"] != None:
                    raise(add_coordinate_request["error"])
        for x in range(len(keys)):
            set_ingredient_request = set_ingredient_cluster(keys[x], kmeans_arr[x])
            if set_ingredient_request["error"] != None:
                raise(set_ingredient_request["error"])
        print("[Info] Successfully calculated kmeans clusters")
    except Exception as e:
        print(e)
        print("[Error] Error calculating kmeans clusters")
        delete_request = delete_kmeans_clusters()
        if delete_request["error"] != None:
            print(delete_request["error"])
            print(delete_request["message"])


