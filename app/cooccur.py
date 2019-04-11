from app import db, models

def generate_new_matrix():
    entries = models.Co_Occur_Matrix.query.all()
    for entry in entries:
        db.session.delete(entry)
    db.session.commit()
    ingredients = models.Ingredient.query.all()
    recipes = models.Recipe.query.all()
    for i1 in ingredients:
        for i2 in ingredients:
            new_entry = models.Co_Occur_Matrix(x_coord = i1.name, y_coord = i2.name, count = 0)
            db.session.add(new_entry)
    for r in recipes:
        for x in r.ingredients:
            for y in r.ingredients:
                edit_entry = models.Co_Occur_Matrix.query.get((x.ingredient_name, y.ingredient_name))
                edit_entry.count = edit_entry.count + 1
                db.session.add(edit_entry)
    db.session.commit()

def add_ingredient_to_matrix(ingredient_name):
    try:
        has_ingredient = models.Co_Occur_Matrix.query.get((ingredient_name,ingredient_name))
        if not has_ingredient:
            ingredients = models.Ingredient.query.all()
            for i in ingredients:
                has_entry = models.Co_Occur_Matrix.query.get((i.name,ingredient_name))
                if not has_entry:
                    db.session.add(models.Co_Occur_Matrix(
                        x_coord=i.name,
                        y_coord=ingredient_name,
                        count=0
                    ))
                has_reversed_entry = models.Co_Occur_Matrix.query.get((ingredient_name, i.name))
                if i.name != ingredient_name and not has_reversed_entry:
                    db.session.add(models.Co_Occur_Matrix(
                        x_coord=ingredient_name,
                        y_coord=i.name,
                        count=0
                    ))
            db.session.commit()
    except Exception as e:
        print(e)
        print('[Error] error adding ingredient to matrix')
        db.session.rollback()

def add_recipe_ingredients_to_matrix(ingredients):
    try:
        for i in ingredients:
            add_ingredient_to_matrix(i["name"])
        for i1 in ingredients:
            for i2 in ingredients:
                entry = models.Co_Occur_Matrix.query.get((i1["name"],i2["name"]))
                entry.count = entry.count + 1
                db.session.add(entry)
        db.session.commit()
    except Exception as e:
        print(e)
        print('[Error] error adding recipe ingredients to matrix')
        db.session.rollback()

def create_matrix():
    keys = []
    matrix = []
    ingredients = models.Ingredient.query.all()
    for i in ingredients:
        # only add ingredients which occur in more than 1 recipe for co occurrence matrix
        num_occurrences = models.Recipe_Ingredient.query.filter_by(ingredient_name=i.name).all()
        # to avoid outliers skewing the data, only include ingredients
        # found in more than 1 recipe
        if len(num_occurrences) > 3:
            keys.append(i.name)
            matrix.append([0] * len(ingredients))
    for x,i1 in enumerate(keys):
        for y,i2 in enumerate(keys):
            entry = models.Co_Occur_Matrix.query.get((i1, i2))
            matrix[x][y] = entry.count
    return matrix,keys



