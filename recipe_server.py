from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from recipe_db_setup import Base, User, Category, Recipe, Ingredient

app = Flask(__name__)

engine = create_engine('sqlite:///recipes.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/categories/')
def showCategories():
    categories = session.query(Category).all()
    return render_template('categories.html', categories=categories)

@app.route('/categories/new/', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')

@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            return redirect(url_for('showCategories'))
    else:
        return render_template('editCategory.html', category=editedCategory)

@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('deleteCategory.html', category=categoryToDelete)


@app.route('/categories/<int:category_id>/recipes/')
def showRecipes(category_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    recipes = session.query(Recipe).filter_by(category_id=category_id).all()
    return render_template('recipes.html', categories=categories, recipes=recipes, category=category)

@app.route('/categories/<int:category_id>/recipes/new', methods=['GET', 'POST'])
def newRecipe(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        newRecipe = Recipe(category_id=category_id, name=request.form['name'])
        session.add(newRecipe)
        session.commit()
        return redirect(url_for('showIngredients', recipe_id=newRecipe.id, category_id=category_id))
    else:
        return render_template('newRecipe.html', category=category)

@app.route('/categories/<int:category_id>/recipes/<int:recipe_id>/edit/', methods=['GET', 'POST'])
def editRecipe(category_id, recipe_id):
    editedRecipe = session.query(Recipe).filter_by(id=recipe_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRecipe.name = request.form['name']
            return redirect(url_for('showRecipes', category_id=category_id))
    else:
        return render_template('editRecipe.html', recipe=editedRecipe)

@app.route('/categories/<int:category_id>/recipes/<int:recipe_id>/delete/', methods=['GET', 'POST'])
def deleteRecipe(category_id, recipe_id):
    recipeToDelete = session.query(Recipe).filter_by(id=recipe_id).one()
    if request.method == 'POST':
        session.delete(recipeToDelete)
        session.commit()
        return redirect(url_for('showRecipes', category_id=category_id))
    else:
        return render_template('deleteRecipe.html', recipe=recipeToDelete)



@app.route('/categories/<int:category_id>/recipes/<int:recipe_id>/ingredients', methods=['GET'])
def showIngredients(category_id, recipe_id):
    category = session.query(Category).filter_by(id=category_id).one()
    recipes = session.query(Recipe).filter_by(category_id=category_id).all()
    recipe = session.query(Recipe).filter_by(id=recipe_id).one()
    ingredients = session.query(Ingredient).filter_by(recipe_id=recipe_id).all()
    return render_template('ingredients.html', category=category, recipes=recipes, recipe=recipe, ingredients=ingredients)

@app.route('/categories/<int:category_id>/recipes/<int:recipe_id>/ingredients/new', methods=['POST'])
def newIngredient(category_id, recipe_id):
    ingredients = session.query(Ingredient).filter_by(recipe_id=recipe_id).all()
    if request.method == 'POST':
        newIngredient = Ingredient(name=request.form['name'], recipe_id=recipe_id)
        session.add(newIngredient)
        session.commit()
    return redirect(url_for('showIngredients', category_id=category_id, recipe_id=recipe_id))

@app.route('/categories/<int:category_id>/recipes/<int:recipe_id>/ingredients/edit/<int:ingredient_id>', methods=['POST'])
def editIngredient(category_id, recipe_id, ingredient_id):
    editedIngredient = session.query(Ingredient).filter_by(id=ingredient_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedIngredient.name = request.form['name']
    return redirect(url_for('showIngredients', category_id=category_id, recipe_id=recipe_id))

@app.route('/categories/<int:category_id>/recipes/<int:recipe_id>/ingredients/delete/<int:ingredient_id>', methods=['POST'])
def deleteIngredient(category_id, recipe_id, ingredient_id):
    ingredientToDelete = session.query(Ingredient).filter_by(id=ingredient_id).one()
    if request.method == 'POST':
        session.delete(ingredientToDelete)
        session.commit()
    return redirect(url_for('showIngredients', category_id=category_id, recipe_id=recipe_id))

# Prevent Caching during development
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
