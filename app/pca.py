'''
Title
-----
pca.py

Description
-----------
Principal Component Analysis calculations
'''
from cooccur import create_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd
from utils import *
from db_accessor import delete_pca_data, add_pca_coordinate


def implement_pca_on_matrix(components=4):
    '''
    Run PCA algorithm on the co-occurrence matrix
    to get coordinates for each ingredient
    :param components: number of PCA components
    :return: the array of PCA coordinates
    '''
    if components > 25:
        raise(Exception('[Error] must reduce to less than 25 components'))
    columns = get_alphabet_columns()[:components]
    initial_matrix, keys = create_matrix()
    if initial_matrix == []:
        return []
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
    '''
    Add PCA coordinates to the database
    :param components: number of PCA components
    '''
    try:
        delete_pca_data()
        columns = get_alphabet_columns()[:components]
        pca_matrix = implement_pca_on_matrix(components)
        if pca_matrix == []:
            return
        for entry in pca_matrix:
            ingredient = entry[components]
            for x in range(components):
                add_pca_coordinate(ingredient, columns[x], entry[x])
        # TODO add error handling
        print("[Info] Successfully added pca coordinates to db")
    except Exception as e:
        print(e)
        print("[Error] Error adding pca coordinates to db")







