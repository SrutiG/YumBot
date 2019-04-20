'''
Title
-----
models.py

Description
-----------
Database schema
'''
from app import db

'''
Recipe class contains basic recipe information
'''
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

'''
Ingredient class contains basic ingredient information
'''
class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    name = db.Column(db.String(128), index=True, primary_key=True)
    image_url = db.Column(db.String(256))
    cluster_number = db.Column(db.Integer, db.ForeignKey('kmeans_cluster.cluster_number'))
    recipes = db.relationship("Recipe_Ingredient", cascade="all", backref="ingredient", passive_updates=False)
    pca_coordinates = db.relationship("PCA_Coordinate", cascade="all", backref="ingredient", passive_updates=False)

    def __str__(self):
        '''
        get the utf-8 encoding of the recipe name
        :return: recipe name in utf-8 encoding
        '''
        return self.name.encode('utf-8')

    def get_coordinates(self):
        '''
        get a tuple containing the pca coordinate
        for this ingredient
        :return: tuple pca coordinate
        '''
        return tuple(self.get_coordinates_list())

    def get_coordinates_list(self):
        '''
        get a list containing the pca coordinate
        for this ingredient
        :return: list pca coordinate
        '''
        coordinates_list = [None] * len(self.pca_coordinates)
        for coordinate in self.pca_coordinates:
            coordinates_list[ord(coordinate.column_name) - 97] = coordinate.value
        return coordinates_list


'''
Relationship table for recipes and ingredients
n-n because a recipe can have multiple ingredients
and an ingredient can exist in multiple recipes

contains amount info for the ingredient in the recipe
'''
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
    standard_amount_string = db.Column(db.String(128))
    standard_amount = db.Column(db.Integer)
    standard_unit = db.Column(db.String(64))

'''
Step for a specific recipe
1-n because a recipe has multiple steps but
each step belongs to just one recipe
'''
class Recipe_Step(db.Model):
    __tablename__ = 'recipe_step'
    recipe_name = db.Column(db.String(128), db.ForeignKey('recipe.name'), primary_key=True)
    step = db.Column(db.String(2048), primary_key=True)
    step_number = db.Column(db.Integer)
    ingredients = db.relationship("Recipe_Step_Ingredient", cascade="all", backref="recipe_step", passive_updates=False)

'''
Ingredients used in recipe step
n-n because an many ingredients can be
used in a recipe step and one ingredient
can be in many recipe steps
'''
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
contains the two ingredients and the count
which is the number of recipes in which
the ingredients are found together
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

'''
A Kmeans cluster containing a set of ingredients
which go well together
'''
class Kmeans_Cluster(db.Model):
    __tablename__ = 'kmeans_cluster'
    cluster_number = db.Column(db.Integer, primary_key=True)
    ingredients = db.relationship("Ingredient", cascade="none", backref="kmeans_cluster", passive_updates=True)
    coordinates = db.relationship("Kmeans_Cluster_Coordinate", cascade="all", backref="kmeans_cluster", passive_updates=False)

    def get_coordinates(self):
        '''
        get cluster center coordinate as a tuple
        :return: tuple cluster coordinate
        '''
        return tuple(self.get_coordinates_list())

    def get_coordinates_list(self):
        '''
        get cluster center coordinate as a list
        :return: list cluster coordinate
        '''
        coordinates = [None] * len(self.coordinates)
        for coord in self.coordinates:
            coordinates[ord(coord.column_name) - 97] = coord.value
        return coordinates

    def get_ingredient_strings(self):
        '''
        get all ingredients contained in the cluster
        as strings
        :return: list of ingredient strings
        '''
        ingredients_str = []
        for ingredient in self.ingredients:
            ingredients_str.append(str(ingredient))
        return ingredients_str

    def get_size(self):
        '''
        get the number of ingredients in the cluster
        which is the size of the cluster
        :return: cluster size
        '''
        return len(self.ingredients)

    def as_dict(self):
        '''
        return a dictionary representation of the cluster
        # TODO: include ingredient strings
        :return: dictionary representation of cluster
        '''
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


'''
A coordinate for the center of the Kmeans cluster
'''
class Kmeans_Cluster_Coordinate(db.Model):
    __tablename__ = 'kmeans_cluster_coordinate'
    cluster_number = db.Column(db.Integer, db.ForeignKey("kmeans_cluster.cluster_number"), primary_key=True)
    column_name = db.Column(db.String(8), primary_key=True)
    value = db.Column(db.Float)



