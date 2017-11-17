# Item Catalogue Project

This project features a content managemnent system. it is written and python and uses the Flask framework. It features a Recipe Website which allows users to view recipes and their ingredients sorted by different categories. Upon authentication, users can use the other CRUD operations, namely creating, editing, and deleting, categories, recipes and recipe ingredients. The project also contains authorization logic to prevent one user from using CRUD operations on another users content. Finally, the website also features JSON endpoints to allow users to obtain recipe information in a JSON object.

Getting started is as easy as setting up the environment and running the code.

## Running Demo
This project utylizes a VirtualBox/Vagrant setup which makes running the demo quick and seemless. It features tools and frameworks such as:
* python (python 3.5.2)
* Flask
* Sqlalchemy

These tools/fraeworks are automatically added to your envionment by the Vagrant file contained in this repository when you launch your vagrant machine.

The steps for launching the demo are as follows:
1. Download VirtualBox and Vagrant.
2. Download/Clone repositiory
3. Navigate to this repository directory using a CL tool
4. Launch your vagrant virtual machine by typing `vagrant up`
5. Log in to your vagrant machine by typing `vagrant ssh`. (Note: Windows users may consider using puTTy, a free ssh client, in order to exchange their ssh keys).
6. Navigate to the project directory and run the recipes.py by typing `python3 recipes.py`. This will generate a starter database of categories, recipes, and ingredients that I've created.
7. Launch website by running `python3 recipe_server.py`
8. Open your browser and navigate to website located at localhost:5000

## Usage
This website features all the usages of a content manager by providing the user all the CRUD operations needed for a recipe website. More importantly, it restricts users to using these operations in the correct context

### CRUD
* Create: Users may only create content if they are logged in. Once logged in a user may create a category or a recipe, but may only create/add an ingredient to a recipe that they have created.
* Read: Users may read any and all content at any time (without being logged in).
* Update: Users may only update categories, recipes, and ingredients if they area logged in and created the category or recipe.
* Destroy: Users may only destoroy categories, recipes, and ingredients if they area logged in and created the category or recipe. (A special stipulation exist where a user may not destroy a category if another user has created a recipe in that category as this would result in one user destroying another users recipe content).

### Login
This website uses googles oauth authentication system. Thus it reqires any user who wants to log in or create an account to have a google account.

### JSON Endpoints
This websites contains several JSON endpoints to allow users to obtain any information that can be read through HTML as a JSON object. JSON endpoints are located on the following paths:
* '/categories/JSON/': Lists all the recipe categories.
* '/category/JSON/<int>/': List the category with the id of the same value as int.
* '/allrecipes/JSON/': List all the recipes contained on the website
*  '/categories/<int>/recipes/JSON/': List all recipes within the category which has an id equal to int.
*  '/recipes/<int>/ingredients/JSON/': List all the ingredients of the recipe with an id equal to int.

(JSON endpoint substitute <int> with appropriate id. Ex: '/recipes/2/ingredients/JSON/' will display all the ingredients for the recipe with the id of '2'.

## Contribution
I would like to thank Udacity for providing the Vagrant file needed to set up the environment. I would also like to thank you for taking the time to look over the project.
