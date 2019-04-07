#!/usr/bin/env python2.7
from app import db_populate

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add or remove recipes from the database. Set the number of recipes to add/remove from the database')
    parser.add_argument('--numrecipes', default=10, type=int,
                        help='Num recipes to add or remove. Default is 10')
    parser.add_argument('--action', default='add', type=str,
                        help='--action add or remove. Set numrecipes to 0 to remove all recipes.')
    args = parser.parse_args()
    if args.numrecipes < 0:
        raise(Exception("[Error] Must enter a positive number of recipes"))
    if args.action == 'add':
        db_populate.add_recipes_to_db(args.numrecipes)
    elif args.action == 'remove':
        if args.numrecipes == 0:
            db_populate.clear_db()
        else:
            db_populate.clear_db(args.numrecipes)