import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from cooccur import create_matrix
from app import db, models


def implement_pca_on_matrix(components=4):
    if components > 25:
        raise(Exception('[Error] must reduce to less than 25 components'))
    columns = ['a','b','c','d','e','f',
               'g','h','i','j','k','l',
               'm','n','o','p','q','r',
               's','t','u','v','w','x',
               'y','z'][:components]
    initial_matrix, keys = create_matrix()
    new_matrix = StandardScaler().fit_transform(initial_matrix)
    pca = PCA(n_components = components)
    keys_dataframe = pd.DataFrame(keys)
    principalComponents = pca.fit_transform(new_matrix)
    principalDf = pd.DataFrame(data = principalComponents
                               , columns = columns)
    concat_arr = []
    for column in columns:
        concat_arr.append(principalDf[column])
    concat_arr.append(keys_dataframe[0])
    finalDf = pd.concat(concat_arr, axis = 1)
    finalDfArr = finalDf.loc[:,columns + [0]].values.tolist()
    return finalDfArr

def add_pca_coordinates_to_db(components=4):
    try:
        old_entries = models.PCA_Coordinate.query.all()
        for old_entry in old_entries:
            db.session.delete(old_entry)
        columns = ['a','b','c','d','e','f',
                   'g','h','i','j','k','l',
                   'm','n','o','p','q','r',
                   's','t','u','v','w','x',
                   'y','z'][:components]
        pca_matrix = implement_pca_on_matrix(components)
        for entry in pca_matrix:
            ingredient = entry[components]
            for x in range(components):
                new_coordinate = models.PCA_Coordinate(
                    ingredient_name=ingredient,
                    column_name=columns[x],
                    value=entry[x]
                )
                db.session.add(new_coordinate)
        db.session.commit()
    except Exception as e:
        print(e)
        print("[Error] Error adding pca coordinates to db")
        db.session.rollback()



def find_farthest_ingredients():
    finalDfArr = implement_pca_on_matrix()
    max_dist = 0
