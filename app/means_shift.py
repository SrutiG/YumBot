from sklearn.cluster import MeanShift, estimate_bandwidth
from db_accessor import get_kmeans_clusters, get_ingredients
import numpy as np
import os

def create_mean_shift_clusters():
    clusters_request = get_kmeans_clusters()
    if clusters_request["error"]:
        return None
    clusters = clusters_request["data"]
    keys = []
    mean_shift_coordinates = []
    for cluster in clusters:
        mean_shift_coordinates.append(cluster.get_coordinates_list())
        keys.append(cluster.cluster_number)
    mean_shift_array = np.array(mean_shift_coordinates)
    bandwidth = estimate_bandwidth(mean_shift_array, quantile=0.1)
    clustering = MeanShift(bandwidth=bandwidth).fit(mean_shift_array)
    for i, key in enumerate(keys):
        print(str(key) + ": " + str(clustering.labels_[i]))

def mean_shift_test():
    get_ingredients_request = get_ingredients()
    if get_ingredients_request["error"] != None:
        raise(get_ingredients_request["error"])
    ingredients = get_ingredients_request["data"]
    # keys: the ingredients which have pca coordinates
    keys = []
    # coordinates: coordinates of each key corresponding to the index of the key
    coordinates = []
    for i in ingredients:
        if len(i.pca_coordinates) > 0:
            keys.append(i.name)
            coordinates.append(i.get_coordinates_list())
    if len(keys) == 0:
        print("[Info] No ingredients with pca coordinates, ending process")
        return
    np_array = np.array(coordinates)
    bandwidth = estimate_bandwidth(np_array, quantile=0.1)
    clustering = MeanShift(bandwidth=bandwidth).fit(np_array)
    cluster_values = [[] for _ in range(max(clustering.labels_) + 1)]
    for i, x in enumerate(keys):

        cluster_values[clustering.labels_[i]].append(x.encode('utf-8'))
    with open(os.getcwd() + '/app/test/means_shift_clusters.txt', 'w') as textfile:
        for i,j in enumerate(cluster_values):
            textfile.write("CLUSTER " + str(i) + "\n")
            textfile.write(",".join(j))
            textfile.write("\n")
