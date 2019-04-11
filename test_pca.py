#!/usr/bin/env python2.7
from app import kmeans
from app import test

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add or remove recipes from the database. Set the number of recipes to add/remove from the database')
    parser.add_argument('--action', default='distance', type=str,
                        help='action can be distance,test,or kmeans. Distance allows you to add a set of ingredients broken up by a comma. Test saves the distance between all ingredients and stats. Kmeans creates kmeans clusters.')
    parser.add_argument('--ingredients', default='garlic,thyme', type=str,
                        help='Ingredients separated by a comma')
    parser.add_argument('--clusters', default=10, type=int,
                        help='Number of k-means clusters')

    args = parser.parse_args()
    if args.action == 'distance':
        ingredients = args.ingredients.split(",")
        test.test_pca(ingredients)
    elif args.action == 'test':
        test.create_database_snapshot()
    elif args.action == 'kmeans':
        kmeans.kmeans_test(args.clusters)