'''
Title
-----
kmeans.py

Description
-----------
K-Means clustering calculations
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
    get the distances from each k-means cluster to the other
    :return: list of cluster distances with indices
    corresponding to cluster number
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

def get_sorted_distances_from_cluster(cluster_number):
    '''
    get clusters in order of least-greatest distance from
    a certain cluster
    :param cluster_number: the reference cluster
    :return: list of clusters ordered by distance
    '''
    kmeans_clusters_request = get_kmeans_clusters()
    if kmeans_clusters_request["error"]:
        print(kmeans_clusters_request["error"])
        return None
    kmeans_clusters = kmeans_clusters_request["data"]
    cluster = None
    distances = {}
    sorted_distances = []
    for c in kmeans_clusters:
        if c.cluster_number == cluster_number:
            cluster = c
    if cluster == None:
        return {}
    for other_cluster in kmeans_clusters:
        if other_cluster.cluster_number != cluster.cluster_number:
            distances[other_cluster.cluster_number] = distance_between_coordinates(
                cluster.get_coordinates(), other_cluster.get_coordinates()
            )
    for key, value in sorted(distances.items(), key=lambda item: item[1]):
        sorted_distances.append(key)
    return sorted_distances


def get_all_kmeans_cluster_distances_dictionary():
    '''
    A dictionary representation of all cluster distances
    :return: dictionary distances from each cluster to another
    '''
    cluster_distances_list = get_all_kmeans_cluster_distances()
    cluster_distances_dict = []
    for c in cluster_distances_list:
        distance_dict = dict((i,k) for i,k in enumerate(c))
        cluster_distances_dict.append(distance_dict)
    return cluster_distances_dict

def find_closest_cluster(cluster_number):
    '''
    Find the closest cluster to a specific cluster
    :param cluster_number: reference cluster
    :return: number of closest cluster
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

def find_closest_clusters_under_threshold(cluster_number):
    '''
    TODO: rename to find_compatible_clusters_under_threshold
    Find the set of clusters compatible to the specific cluster
    :param cluster_number: the reference cluster
    :return: set of compatible clusters
    '''
    closest_clusters = set()
    sorted_distances = get_sorted_distances_from_cluster(cluster_number)
    threshold = cluster_size_upper_threshold()
    if get_cluster_size(cluster_number) > threshold:
        return sorted_distances
    for x in sorted_distances:
        closest_clusters.add(x)
        if get_cluster_size(x) > threshold:
            break
    return closest_clusters

def smallest_cluster_size():
    '''
    Find the size of the smallest cluster
    :return: size of smallest cluster
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

def get_cluster_size(cluster_number):
    '''
    Get the size of a specific cluster
    :param cluster_number: cluster number
    :return: size of cluster
    '''
    cluster_request = get_kmeans_cluster(cluster_number)
    if cluster_request["error"]:
        print(cluster_request["error"])
        return sys.maxint
    return cluster_request["data"].get_size()

def largest_cluster_size():
    '''
    Get the largest cluster size
    :return: size of largest cluster
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
    get the size threshold for compatible clusters
    calculations
    :return: size threshold
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
    Create kmeans clusters from PCA coordinates
    and add them to the database
    :param clusters: number of clusters
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


