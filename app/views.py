from app import app
from flask import render_template, redirect, session, request, jsonify, url_for
from spoonacular_api import *



'''
Default route
'''
@app.route('/')
def index():
    if not session.get("search"):
        session["search"] = []
    if not session.get("recipes"):
        session["recipes"] = find_random_recipes(4)
        session["random_search"] = True
    return render_template('index.html',
                           recipes=session.get("recipes"),
                           search=session.get("search"),
                           random_search=session.get("random_search"))

@app.route('/search/<search_value>')
def search(search_value=None):
    search = session.get("search")
    if search_value not in search:
        search.append(search_value)
    session["search"] = search
    recipes = search_recipes_by_ingredient(search)
    session["recipes"] = recipes
    if len(recipes) > 0:
        session["random_search"] = False
    return redirect(url_for("index"))

@app.route('/remove_search/<search_value>')
def remove_search(search_value):
    search = session.get("search")
    if search_value in search:
        search.remove(search_value)
    session["search"] = search
    recipes = search_recipes_by_ingredient(search)
    session["recipes"] = recipes
    if len(recipes) > 0:
        session["random_search"] = False
    return redirect(url_for("index"))

