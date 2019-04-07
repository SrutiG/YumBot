
'''
Title
-----
models.py
Description
-----------
Database schema
'''
from app import db

class Recipe(db.Model):
    name = db.Column(db.String(128), index=True, primary_key=True)
    source = db.Column(db.String(128))
    source_url = db.Column(db.String(256))
    image_url = db.Column(db.String(256))
    vegetarian = db.Column(db.Boolean)
    vegan = db.Column(db.Boolean)
    dairy_free = db.Column(db.Boolean)
    gluten_free = db.Column(db.Boolean)
    prep_time = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    ingredients = db.relationship("Recipe_Ingredient", cascade="all", backref="recipe", passive_updates=False)
    steps = db.relationship("Recipe_Step", cascade="all", backref="recipe", passive_updates=False)

class Ingredient(db.Model):
    name = db.Column(db.String(128), index=True, primary_key=True)
    image_url = db.Column(db.String(256), default="/static/images/stock_recipe_image.jpg")
    recipes = db.relationship("Recipe_Ingredient", cascade="all", backref="ingredient", passive_updates=False)

class Recipe_Ingredient(db.Model):
    __tablename__ = 'recipe_ingredient'
    recipe_name = db.Column(db.String(128), db.ForeignKey('recipe.name'), primary_key=True)
    ingredient_name = db.Column(db.String(128), db.ForeignKey('ingredient.name'), primary_key=True)

class Recipe_Step(db.Model):
    __tablename__ = 'recipe_step'
    recipe_name = db.Column(db.String(128), db.ForeignKey('recipe.name'), primary_key=True)
    step = db.Column(db.String(2048), primary_key=True)
    step_number = db.Column(db.Integer)
    ingredients = db.relationship("Recipe_Step_Ingredient", cascade="all", backref="recipe_step", passive_updates=False)

class Recipe_Step_Ingredient(db.Model):
    recipe_name = db.Column(db.String(128), db.ForeignKey('recipe_step.recipe_name'), primary_key=True)
    step = db.Column(db.String(2048), db.ForeignKey('recipe_step.step'), primary_key=True)
    ingredient_name = db.Column(db.String(128), db.ForeignKey('ingredient.name'), primary_key=True)



