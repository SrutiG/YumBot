#!/usr/bin/env python2.7
from app import db_populate

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Set the number of recipes to add to the database')
    parser.add_argument('--numrecipes', default='10', type=int,
                        help='numrecipes')
    args = parser.parse_args()
    db_populate.add_recipes_to_db(args.numrecipes)