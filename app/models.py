
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
    __tablename__ = 'recipe'
    name = db.Column(db.String(128), index=True, primary_key=True)
    source = db.Column(db.String(128))
    source_url = db.Column(db.String(256))
    image_url = db.Column(db.String(256), default="/static/images/stock_recipe_image.jpg")
    vegetarian = db.Column(db.Boolean)
    vegan = db.Column(db.Boolean)
    dairy_free = db.Column(db.Boolean)
    gluten_free = db.Column(db.Boolean)
    prep_time = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    ingredients = db.relationship("Recipe_Ingredient", cascade="all", backref="recipe", passive_updates=False)
    steps = db.relationship("Recipe_Step", cascade="all", backref="recipe", passive_updates=False)

class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    name = db.Column(db.String(128), index=True, primary_key=True)
    image_url = db.Column(db.String(256))
    recipes = db.relationship("Recipe_Ingredient", cascade="all", backref="ingredient", passive_updates=False)
    pca_coordinates = db.relationship("PCA_Coordinate", cascade="all", backref="ingredient", passive_updates=False)

class Recipe_Ingredient(db.Model):
    __tablename__ = 'recipe_ingredient'
    recipe_name = db.Column(db.String(128), db.ForeignKey('recipe.name'), primary_key=True)
    ingredient_name = db.Column(db.String(128), db.ForeignKey('ingredient.name'), primary_key=True)
    original_string = db.Column(db.String(128))
    amount = db.Column(db.Integer)
    unit = db.Column(db.Integer)
    us_amount = db.Column(db.Integer)
    us_unit = db.Column(db.String(64))
    metric_amount = db.Column(db.Integer)
    metric_unit = db.Column(db.String(64))
    standard_amount = db.Column(db.Integer)

class Recipe_Step(db.Model):
    __tablename__ = 'recipe_step'
    recipe_name = db.Column(db.String(128), db.ForeignKey('recipe.name'), primary_key=True)
    step = db.Column(db.String(2048), primary_key=True)
    step_number = db.Column(db.Integer)
    ingredients = db.relationship("Recipe_Step_Ingredient", cascade="all", backref="recipe_step", passive_updates=False)

class Recipe_Step_Ingredient(db.Model):
    __tablename__= 'recipe_step_ingredient'
    recipe_name = db.Column(db.String(128), primary_key=True)
    step = db.Column(db.String(2048), primary_key=True)
    ingredient_name = db.Column(db.String(128), db.ForeignKey("ingredient.name"), primary_key=True)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['recipe_name', 'step'],
            ['recipe_step.recipe_name', 'recipe_step.step'],
        ),
    )

'''
Co-occurrence matrix for ingredients
'''
class Co_Occur_Matrix(db.Model):
    __tablename__= 'co_occur_matrix'
    x_coord = db.Column(db.String(128), db.ForeignKey('ingredient.name'), primary_key=True)
    y_coord = db.Column(db.String(128), db.ForeignKey('ingredient.name'), primary_key=True)
    count = db.Column(db.Integer)

'''
PCA coordinates for an ingredient
'''
class PCA_Coordinate(db.Model):
    __tablename__ = 'pca_coordinate'
    ingredient_name = db.Column(db.String(128), db.ForeignKey('ingredient.name'), primary_key=True)
    column_name = db.Column(db.String(8), primary_key=True)
    value = db.Column(db.Float)



