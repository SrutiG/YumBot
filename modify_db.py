#!/usr/bin/env python2.7
'''

'''
from app import db_populate
from app import cooccur
from app import pca
from app import kmeans
import math

import argparse

def add_recipes_to_db_bulk(num_recipes):
    '''

    :param num_recipes:
    :return:
    '''
    loop_ind = int(math.ceil(num_recipes/100))
    recipes_to_add = num_recipes
    for _ in range(loop_ind):
        db_populate.add_recipes_to_db(min(100, recipes_to_add))
        recipes_to_add -= 100

if __name__ == "__main__":
    '''
    
    '''
    parser = argparse.ArgumentParser(description='Add or remove recipes from the database. Set the number of recipes to add/remove from the database')
    parser.add_argument('--numrecipes', default=10, type=int,
                        help='Num recipes to add or remove. Default is 10')
    parser.add_argument('--action', default='add', type=str,
                        help='--action add, remove, matrix, pca, kmeans, add_calc, remove_calc, and clear. '
                             'add: add recipes to the database. Use numrecipes flag to set number of recipes to add. Default is 10 \n'
                             'remove: remove recipes from the database. Use numrecipes flag to set number of recipes to remove. \n'
                             'matrix: recreate the co-occurrence matrix based on current recipes in the database. This is done automatically after adding recipes. \n'
                             'pca: calculate pca coordinates based on current co-occurrence matrix. \n'
                             'kmeans: calculate kmeans clusters based on pca coordinates. \n'
                             'add_calc: add recipes to database, calculate pca coordinates and kmeans coordinates. Use numrecipes to set number of recipes to add. \n'
                             'remove_calc: remove recipes from database. calculate pca coordinates and kmeans coordinates. Use numrecipes to set number of recipes to remove. \n'
                             'clear: wipe all data from the db including matrix, pca, kmeans, recipes, and ingredients. \n')
    parser.add_argument('--components', default=24, type=int, help='number of pca components. default is 10.')
    parser.add_argument('--clusters', default=35, type=int, help='number of kmeans clusters. default is 10.')
    args = parser.parse_args()
    if args.numrecipes < 0:
        raise(Exception("[Error] Must enter a positive number of recipes"))
    if args.action == 'add':
        add_recipes_to_db_bulk(args.numrecipes)
    elif args.action == 'remove':
        db_populate.clear_db(args.numrecipes)
    elif args.action == 'matrix':
        cooccur.generate_new_matrix()
    elif args.action == 'pca':
        pca.add_pca_coordinates_to_db(args.components)
    elif args.action == 'kmeans':
        kmeans.create_kmeans_clusters(args.clusters)
    elif args.action == 'add_calc':
        add_recipes_to_db_bulk(args.numrecipes)
        pca.add_pca_coordinates_to_db(args.components)
        kmeans.create_kmeans_clusters(args.clusters)
    elif args.action == 'remove_calc':
        db_populate.clear_db(args.numrecipes)
        pca.add_pca_coordinates_to_db(args.components)
        kmeans.create_kmeans_clusters(args.clusters)
    elif args.action == 'clear':
        db_populate.clear_db(None, False)


