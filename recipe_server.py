from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy import exists
from sqlalchemy.orm import sessionmaker
from recipe_db_setup import Base, User, Category, Recipe, Ingredient

from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
SUPER_SECRET_KEY = json.loads(
    open('client_secrets.json', 'r').read())['web']['super_secret_key']

engine = create_engine('sqlite:///recipes.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
# Store it in the session for later valdation
@app.route('/login')
def showLogin():
    email = login_session.get('email')
    state = "".join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state, CLIENT_ID=CLIENT_ID, email=email, username=login_session['username'])

@app.route('/gconnect', methods=['POST'])
def gconnect():

    # Validate state token
    # If token isn't same as initial state then it malicious
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code from request
    code = request.data
    print("hey")
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        print("what")
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads((h.request(url, 'GET')[1]).decode("utf-8"))
    # If there is and error with the access token info, abort!

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(jsone.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client does not match app's"), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the login_session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfor_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfor_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Save user_id to session log. If no user_id create User
    existingUser = session.query(exists().where(User.email==login_session['email'])).scalar()
    if existingUser:
        login_session['user_id'] = session.query(User).filter_by(email=login_session['email']).one().id
    else:
        newUser = User(email=login_session['email'])
        session.add(newUser)
        session.commit()
        login_session['user_id'] = session.query(User).filter_by(email=login_session['email']).one().id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    '''if result['status'] == '200':'''
    del login_session['access_token']
    del login_session['gplus_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    flash("Succeffully Logged Out!")
    return redirect(url_for('showCategories'))
    '''else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response'''


# JSON endpoints
@app.route('/categories/JSON/')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serializable for r in categories])

@app.route('/category/JSON/<int:category_id>/')
def categoryJSON(category_id):
    isCategory = session.query(exists().where(Category.id==category_id)).scalar()
    if isCategory:
        category = session.query(Category).filter_by(id=category_id).one()
        return jsonify(category=category.serializable)
    return jsonify(category="No category with %s for an id" % category_id)

@app.route('/allrecipes/JSON/')
def allRecipesJSON():
    recipes = session.query(Recipe).all()
    return jsonify(recipes=[r.serializable for r in recipes])

@app.route('/categories/<int:category_id>/recipes/JSON')
def categoryRecipesJSON(category_id):
    isRecipes = session.query(exists().where(Recipe.category_id==category_id)).scalar()
    if isRecipes:
        recipes = session.query(Recipe).filter_by(category_id=category_id)
        return jsonify(recipes=[r.serializable for r in recipes])
    return jsonify(recipes="No recipes in category with %s for an id" % category_id)

@app.route('/recipes/<int:recipe_id>/ingredients/JSON/')
def recipeIngredientsJSON(recipe_id):
    isIngredients = session.query(exists().where(Ingredient.recipe_id==recipe_id)).scalar()
    if isIngredients:
        ingredients = session.query(Ingredient).filter_by(recipe_id=recipe_id)
        return jsonify(ingredients=[r.serializable for r in ingredients])
    return jsonify(ingredients="No ingredients in recipe with %s for an id" % recipe_id)


@app.route('/')
@app.route('/categories/')
def showCategories():
    email = login_session.get('email')
    username = login_session.get('username')
    categories = session.query(Category).all()
    return render_template('categories.html', categories=categories, email=email, username=username)

@app.route('/categories/new/', methods=['GET', 'POST'])
def newCategory():
    email = login_session.get('email')
    username = login_session.get('username')
    if 'email' not in login_session:
        flash("You must me be logged in to create a new Category")
        return redirect('/login')
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'], user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        flash('Successfully Created the Category %s' % newCategory.name)
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html', email=email, username=username)

@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    email = login_session.get('email')
    username = login_session.get('username')
    if 'email' not in login_session:
        return redirect('/login')
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if editedCategory.user_id != login_session['user_id']:
            flash("You may only edit Categories you've created")
            return redirect(url_for('showCategories'))
        if request.form['name']:
            editedCategory.name = request.form['name']
            return redirect(url_for('showCategories'))
    else:
        print([editedCategory.user_id, login_session['user_id']])
        return render_template('editCategory.html', category=editedCategory, email=email, username=username)

@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    email = login_session.get('email')
    username = login_session.get('username')
    if 'email' not in login_session:
        return redirect('/login')
    categoryToDelete = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if categoryToDelete.user_id != login_session['user_id']:
            flash("You may ony delete Categories you created")
            redirect(url_for('showCategories'))
        for recipe in session.query(Recipe).filter_by(category_id=categoryToDelete.id):
            if recipe.user_id != login_session['user_id']:
                flash("This Category contains Recipes that do not belong to the logged in User. Only and admin may delete this Category")
                return redirect(url_for('showCategories'))
        session.delete(categoryToDelete)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('deleteCategory.html', category=categoryToDelete, email=email, username=username)


@app.route('/categories/<int:category_id>/recipes/')
def showRecipes(category_id):
    email = login_session.get('email')
    username = login_session.get('username')
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    recipes = session.query(Recipe).filter_by(category_id=category_id).all()
    return render_template('recipes.html', categories=categories, recipes=recipes, category=category, email=email, username=username)

@app.route('/categories/<int:category_id>/recipes/new', methods=['GET', 'POST'])
def newRecipe(category_id):
    email = login_session.get('email')
    username = login_session.get('username')
    if 'email' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        newRecipe = Recipe(category_id=category_id, name=request.form['name'], user_id=login_session['user_id'])
        session.add(newRecipe)
        session.commit()
        return redirect(url_for('showIngredients', recipe_id=newRecipe.id, category_id=category_id))
    else:
        return render_template('newRecipe.html', category=category, email=email, username=username)

@app.route('/categories/<int:category_id>/recipes/<int:recipe_id>/edit/', methods=['GET', 'POST'])
def editRecipe(category_id, recipe_id):
    email = login_session.get('email')
    username = login_session.get('username')
    if 'email' not in login_session:
        return redirect('/login')
    editedRecipe = session.query(Recipe).filter_by(id=recipe_id).one()
    if request.method == 'POST':
        if editedRecipe.user_id != login_session['user_id']:
            flash('You may only edit a Recipe you created')
            return redirect(url_for('showRecipes', category_id=category_id))
        if request.form['name']:
            editedRecipe.name = request.form['name']
            return redirect(url_for('showRecipes', category_id=category_id))
    else:
        return render_template('editRecipe.html', recipe=editedRecipe, email=email, username=username)

@app.route('/categories/<int:category_id>/recipes/<int:recipe_id>/delete/', methods=['GET', 'POST'])
def deleteRecipe(category_id, recipe_id):
    email = login_session.get('email')
    username = login_session.get('username')
    if 'email' not in login_session:
        return redirect('/login')
    recipeToDelete = session.query(Recipe).filter_by(id=recipe_id).one()
    if request.method == 'POST':
        if recipeToDelete.user_id != login_session['user_id']:
            flash("You may only delete a recipe you created")
            return redirect(url_for('showRecipes', category_id=category_id))
        session.delete(recipeToDelete)
        session.commit()
        return redirect(url_for('showRecipes', category_id=category_id))
    else:
        return render_template('deleteRecipe.html', recipe=recipeToDelete, email=email, username=username)



@app.route('/categories/<int:category_id>/recipes/<int:recipe_id>/ingredients', methods=['GET'])
def showIngredients(category_id, recipe_id):
    email = login_session.get('email')
    username = login_session.get('username')
    category = session.query(Category).filter_by(id=category_id).one()
    recipes = session.query(Recipe).filter_by(category_id=category_id).all()
    recipe = session.query(Recipe).filter_by(id=recipe_id).one()
    ingredients = session.query(Ingredient).filter_by(recipe_id=recipe_id).all()
    return render_template('ingredients.html', category=category, recipes=recipes, recipe=recipe, ingredients=ingredients, email=email, username=username)

@app.route('/categories/<int:category_id>/recipes/<int:recipe_id>/ingredients/new', methods=['POST'])
def newIngredient(category_id, recipe_id):
    if 'email' not in login_session:
        return redirect('/login')
    recipe = session.query(Recipe).filter_by(id=recipe_id).one()
    if recipe.user_id != login_session['user_id']:
        flash("You may only add new Ingredient to a Recipe you created")
        return redirect(url_for('showIngredients', category_id=category_id, recipe_id=recipe_id))
    ingredients = session.query(Ingredient).filter_by(recipe_id=recipe_id).all()
    if request.method == 'POST':
        newIngredient = Ingredient(name=request.form['name'], recipe_id=recipe_id)
        session.add(newIngredient)
        session.commit()
    return redirect(url_for('showIngredients', category_id=category_id, recipe_id=recipe_id))

@app.route('/categories/<int:category_id>/recipes/<int:recipe_id>/ingredients/edit/<int:ingredient_id>', methods=['POST'])
def editIngredient(category_id, recipe_id, ingredient_id):
    if 'email' not in login_session:
        return redirect('/login')
    recipe = session.query(Recipe).filter_by(id=recipe_id).one()
    if recipe.user_id != login_session['user_id']:
        flash("You may only edit an Ingredient on a Recipe you created")
        return redirect(url_for('showIngredients', category_id=category_id, recipe_id=recipe_id))
    editedIngredient = session.query(Ingredient).filter_by(id=ingredient_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedIngredient.name = request.form['name']
    return redirect(url_for('showIngredients', category_id=category_id, recipe_id=recipe_id))

@app.route('/categories/<int:category_id>/recipes/<int:recipe_id>/ingredients/delete/<int:ingredient_id>', methods=['POST'])
def deleteIngredient(category_id, recipe_id, ingredient_id):
    if 'email' not in login_session:
        return redirect('/login')
    recipe = session.query(Recipe).filter_by(id=recipe_id).one()
    if recipe.user_id != login_session['user_id']:
        flash("You may only delete an Ingredient on a Recipe you created")
        return redirect(url_for('showIngredients', category_id=category_id, recipe_id=recipe_id))
    ingredientToDelete = session.query(Ingredient).filter_by(id=ingredient_id).one()
    if request.method == 'POST':
        session.delete(ingredientToDelete)
        session.commit()
    return redirect(url_for('showIngredients', category_id=category_id, recipe_id=recipe_id))

# Prevent Caching during development
@app.after_request
def add_header(r):
    '''
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    '''
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':
    app.secret_key = SUPER_SECRET_KEY
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
