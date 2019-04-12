from app import db, models

# ================== GETTERS ==================

def get_ingredients():
    try:
        return {"data":models.Ingredient.query.all(),
                "error":None,
                "message":"successfully got ingredients"}
    except Exception as e:
        print(e)
        print("[Error] Error getting ingredients")
        return {"error":e, "message":"[Error] error getting ingredients"}

def get_ingredient(ingredient_name):
    try:
        return {"data":models.Ingredient.query.get(ingredient_name),
                "error":None,
                "message":"successfully got ingredient"}
    except Exception as e:
        print(e)
        print("[Error] Error getting ingredient " + ingredient_name)
        return {"error":e, "message":"[Error] error getting ingredient"}

def get_kmeans_clusters():
    try:
        return {"data": models.Kmeans_Cluster.query.all(),
                "error":None,
                "message":"successfully got kmeans clusters"}
    except Exception as e:
        print(e)
        print("[Error] Error getting kmeans clusters")
        return {"error":e, "message": "[Error] error getting kmeans clusters"}

def get_kmeans_cluster(cluster_number):
    try:
        return {"data": models.Kmeans_Cluster.query.get(cluster_number),
                "error":None,
                "message":"successfully got kmeans cluster " + str(cluster_number)}
    except Exception as e:
        print(e)
        print("[Error] Error getting kmeans cluster")
        return {"error":e, "message": "[Error] error getting kmeans cluster"}

# ================== SETTERS ==================

def set_ingredient_cluster(ingredient_name, cluster):
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


