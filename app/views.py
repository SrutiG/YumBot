'''

'''
from app import app
from flask import render_template, redirect, session, request, jsonify, url_for
from spoonacular_api import *
from pca import create_distance_matrix
from yumbot import YumBot

global yb

@app.before_request
def before_request():
    global yb
    yb = YumBot()

@app.route('/')
def index():
    '''

    :return:
    '''
    global yb
    if not session.get("search"):
        session["search"] = []
    if not session.get("recipes"):
        yumbot_recipe = yb.get_random_recipe()
        if yumbot_recipe != None:
            recipes = find_random_recipes(3)
            recipes.insert(0, yb.get_random_recipe())
        else:
            recipes = find_random_recipes(4)
        session["recipes"] = recipes
        session["random_search"] = True
    return render_template('index.html',
                           recipes=session.get("recipes"),
                           search=session.get("search"),
                           random_search=session.get("random_search"))

@app.route('/search/<search_value>')
def search(search_value=None):
    '''

    :param search_value:
    :return:
    '''
    global yb
    search = session.get("search")
    if search_value not in search:
        search.append(search_value)
    session["search"] = search
    recipes = yb.create_recipes_from_ingredients(search) or []
    recipes += search_recipes_by_ingredient(search)
    session["recipes"] = recipes
    if len(recipes) > 0:
        session["random_search"] = False
    return redirect(url_for("index"))

@app.route('/remove_search/<search_value>')
def remove_search(search_value):
    '''

    :param search_value:
    :return:
    '''
    global yb
    search = session.get("search")
    if search_value in search:
        search.remove(search_value)
    session["search"] = search
    recipes = yb.create_recipes_from_ingredients(search) or []
    recipes += search_recipes_by_ingredient(search)
    session["recipes"] = recipes
    if len(recipes) > 0:
        session["random_search"] = False
    return redirect(url_for("index"))

@app.route('/clear_search')
def clear_search():
    '''

    :return:
    '''
    session["search"] = []
    session["recipes"] = []
    return redirect(url_for("index"))

