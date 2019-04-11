from app import db, models

# ================== GETTERS ==================

def get_ingredients():
    try:
        return models.Ingredient.query.all()
    except Exception as e:
        print(e)
        print("[Error] Error getting ingredients")
        return None

def get_ingredient(ingredient_name):
    try:
        return models.Ingredient.query.get(ingredient_name)
    except Exception as e:
        print(e)
        print("[Error] Error getting ingredient " + ingredient_name)
        return None

# ================== SETTERS ==================

def set_ingredient_cluster(ingredient_name, cluster):
    try:
        ingredient = get_ingredient(ingredient_name)
        if ingredient != None:
            ingredient.cluster_number = cluster
            db.session.add(ingredient)
            db.session.commit()
    except Exception as e:
        print(e)
        print("[Error] Error adding cluster for ingredient")
        db.session.rollback()

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
    except Exception as e:
        print(e)
        print("[Error] error adding pca coordinate")
        db.session.rollback()

def add_kmeans_cluster(number):
    try:
        new_cluster = models.Kmeans_Cluster(cluster_number=number)
        db.session.add(new_cluster)
        db.session.commit()
    except Exception as e:
        print(e)
        print("[Error] error adding kmeans cluster")
        db.session.rollback()

def add_kmeans_cluster_coordinate(cluster_number, column_name, value):
    try:
        new_cluster_coord = models.Kmeans_Cluster_Coordinate(
            cluster_number=cluster_number,
            column_name=column_name,
            value=value
        )
        db.session.add(new_cluster_coord)
        db.session.commit()
    except Exception as e:
        print(e)
        print("[Error] error adding kmeans cluster coordinate")
        db.session.rollback()

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



