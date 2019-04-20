'''
Title
-----
db_accessor.py

Description
-----------
Interact with the database
'''
from app import db, models

# ================== GET ==================

def get_ingredients():
    '''
    get all ingredients in the database
    :return: object containing ingredient list if successful
    or error if not successful
    '''
    try:
        return {"data":models.Ingredient.query.all(),
                "error":None,
                "message":"successfully got ingredients"}
    except Exception as e:
        print(e)
        print("[Error] Error getting ingredients")
        return {"error":e, "message":"[Error] error getting ingredients"}

def get_ingredient(ingredient_name):
    '''
    get a specific ingredient object by name
    :param ingredient_name: name of ingredient
    :return: object containing ingredient data if successful
    or error if not successful
    '''
    try:
        return {"data":models.Ingredient.query.get(ingredient_name),
                "error":None,
                "message":"successfully got ingredient"}
    except Exception as e:
        print(e)
        print("[Error] Error getting ingredient " + ingredient_name)
        return {"error":e, "message":"[Error] error getting ingredient"}

def get_kmeans_clusters():
    '''
    Get all kmeans clusters in database
    :return: object containing kmeans clusters if successful
    or error if not successful
    '''
    try:
        return {"data": models.Kmeans_Cluster.query.all(),
                "error":None,
                "message":"successfully got kmeans clusters"}
    except Exception as e:
        print(e)
        print("[Error] Error getting kmeans clusters")
        return {"error":e, "message": "[Error] error getting kmeans clusters"}

def get_kmeans_cluster(cluster_number):
    '''
    Get a kmeans cluster by the cluster number
    :param cluster_number: kmeans cluster number
    :return: object containing kmeans cluster if successful
    or error if not successful
    '''
    try:
        return {"data": models.Kmeans_Cluster.query.get(cluster_number),
                "error":None,
                "message":"successfully got kmeans cluster " + str(cluster_number)}
    except Exception as e:
        print(e)
        print("[Error] Error getting kmeans cluster")
        return {"error":e, "message": "[Error] error getting kmeans cluster"}

# ================== UPDATE ==================

def set_ingredient_cluster(ingredient_name, cluster):
    '''
    Set the cluster number for a particular ingredient
    :param ingredient_name: ingredient name
    :param cluster: kmeans cluster number
    :return: object containing error if not successful
    '''
    try:
        ingredient = get_ingredient(ingredient_name)
        if ingredient["error"] != None:
            raise(ingredient["error"])
        ingredient = ingredient["data"]
        if ingredient != None:
            ingredient.cluster_number = int(cluster)
            db.session.add(ingredient)
            db.session.commit()
        return {"error":None, "message":"successfully set ingredient cluster"}
    except Exception as e:
        print(e)
        print("[Error] Error adding cluster for ingredient")
        db.session.rollback()
        return {"error":e, "message":"[Error] error setting ingredient cluster"}

# ================== ADD ==================

def add_pca_coordinate(ingredient_name, column_name, value):
    '''
    Add a pca coordinate for an ingredient
    :param ingredient_name: ingredient name
    :param column_name: column name [a-z]
    :param value: coordinate value
    :return: object containing error if not successful
    '''
    try:
        new_coordinate = models.PCA_Coordinate(
            ingredient_name=ingredient_name,
            column_name=column_name,
            value=value
        )
        db.session.add(new_coordinate)
        db.session.commit()
        return {"error":None, "message":"successfully added pca coordinate"}
    except Exception as e:
        print(e)
        print("[Error] error adding pca coordinate")
        db.session.rollback()
        return {"error":e,
                "message": "error adding pca coordinate"}

def add_kmeans_cluster(number):
    '''
    Add a new kmeans cluster
    :param number: cluster number
    :return: object containing error if not successful
    '''
    try:
        new_cluster = models.Kmeans_Cluster(cluster_number=number)
        db.session.add(new_cluster)
        db.session.commit()
        return {"error":None, "message":"successfully added kmeans cluster"}
    except Exception as e:
        print(e)
        print("[Error] error adding kmeans cluster")
        db.session.rollback()
        return {"error":e,
                "message": "error adding kmeans cluster"}

def add_kmeans_cluster_coordinate(cluster_number, column_name, value):
    '''
    Add a coordinate for a kmeans cluster
    :param cluster_number: kmeans cluster number
    :param column_name: column name [a-z]
    :param value: coordinate value
    :return: object containing error if not successful
    '''
    try:
        new_cluster_coord = models.Kmeans_Cluster_Coordinate(
            cluster_number=cluster_number,
            column_name=column_name,
            value=value
        )
        db.session.add(new_cluster_coord)
        db.session.commit()
        return {"error":None, "message":"successfully set kmeans cluster coordinate"}
    except Exception as e:
        print(e)
        print("[Error] error adding kmeans cluster coordinate")
        db.session.rollback()
        return {"error":e,
                "message":"[Error] setting kmeans cluster coordinate"}

# ================== DELETE ==================

def delete_pca_data():
    '''
    Delete all PCA data from database
    :return: object containing error if not successful
    '''
    try:
        pca_coord = models.PCA_Coordinate.query.all()
        for coord in pca_coord:
            db.session.delete(coord)
        db.session.commit()
        return {"error":None, "message":"successfully removed pca data"}
    except Exception as e:
        print(e)
        print("[Error] error wiping pca data")
        db.session.rollback()
        return {"error":e,
                "message":"There was an error while wiping pca data"}

def delete_kmeans_clusters():
    '''
    Delete all kmeans clusters from database
    :return: object containing error if not successful
    '''
    try:
        kmeans_clusters = models.Kmeans_Cluster.query.all()
        for cluster in kmeans_clusters:
            db.session.delete(cluster)
        db.session.commit()
        return {"error":None,
                       "message":"successfully wiped kmeans data"}
    except Exception as e:
        print(e)
        print("[Error] error deleting kmeans data")
        db.session.rollback()
        return {"error":e,
                "message":"There was an error while wiping kmeans data"}



