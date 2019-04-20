'''
Title
-----
views.py

Description
-----------
handling requests to server
'''

from app import app
from flask import render_template, redirect, session, request, jsonify, url_for
from spoonacular_api import *
from yumbot import YumBot

global yb

@app.before_request
def before_request():
    '''
    TODO: after serializing YumBot clusters,
    TODO: modify this method to before_first_request

    create a global YumBot object
    :return:
    '''
    global yb
    # global recipes
    yb = YumBot()
    # search = session.get("search")
    # if len(search) > 0:
    #     recipes = yb.create_recipes_from_ingredients(search) or []
    #     recipes += search_recipes_by_ingredient(search)

@app.route('/')
def index():
    '''
    return the index.html template
    with search and recipes object based
    on what is stored in the session
    TODO: figure out how to bypass session storage
    TODO: since many recipes are long
    :return: index.html rendered template
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
    search for a specific ingredient
    and update the search list in the session.
    find recipes matching the search
    :param search_value: string ingredient name
    :return: redirect to index
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
    remove a specific ingredient
    from the search if it is contained
    in the search list. Update the recipes
    based on the new search
    :param search_value: string ingredient name
    :return: redirect to index
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
    clear all values from the search and
    reset the recipes list
    :return: redirect to index
    '''
    session["search"] = []
    session["recipes"] = []
    return redirect(url_for("index"))

