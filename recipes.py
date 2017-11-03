from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from recipe_db_setup import Base, User, Category, Recipe, Ingredient

engine = create_engine('sqlite:///recipes.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

#Create Master User (Me)
user1 = User(email="osa10928@gmail.com")
session.add(user1)
session.commit()

#Create 1st category with user1 as reference
category1 = Category(name="BBQ", user=user1)
session.add(category1)
session.commit()

#Create 1st Recipe with category1 as reference
recipe1 = Recipe(name="Barbequed Ribs", category=category1)
session.add(recipe1)
session.commit()

#Create ingredients for recipe1
ingredient1 = Ingredient(name="4 pounds baby back pork ribs", recipe=recipe1)
session.add(ingredient1)
session.commit()

ingredient2 = Ingredient(name="4 cloves garlic, sliced", recipe=recipe1)
session.add(ingredient2)
session.commit()

ingredient3 = Ingredient(name="1 tablespoon white sugar", recipe=recipe1)
session.add(ingredient3)
session.commit()

ingredient4 = Ingredient(name="1 tablespoon paprika", recipe=recipe1)
session.add(ingredient4)
session.commit()

ingredient5 = Ingredient(name="2 teaspoons salt", recipe=recipe1)
session.add(ingredient5)
session.commit()

ingredient6 = Ingredient(name="2 teaspoons ground black pepper", recipe=recipe1)
session.add(ingredient6)
session.commit()

ingredient7 = Ingredient(name="2 teaspoons chili powder", recipe=recipe1)
session.add(ingredient7)
session.commit()

ingredient8 = Ingredient(name="2 teaspoons ground cumin", recipe=recipe1)
session.add(ingredient8)
session.commit()

ingredient9 = Ingredient(name="1/2 cup dark brown sugar", recipe=recipe1)
session.add(ingredient9)
session.commit()

ingredient10 = Ingredient(name="1/2 cider vinegar", recipe=recipe1)
session.add(ingredient10)
session.commit()

ingredient11 = Ingredient(name="1/2 cup ketchup", recipe=recipe1)
session.add(ingredient11)
session.commit()

ingredient12 = Ingredient(name="1/4 cup chili sauce", recipe=recipe1)
session.add(ingredient12)
session.commit()

ingredient13 = Ingredient(name="1/4 Worcestershire sauce", recipe=recipe1)
session.add(ingredient13)
session.commit()

ingredient14 = Ingredient(name="1 tablespoon lemon juice", recipe=recipe1)
session.add(ingredient14)
session.commit()

ingredient15 = Ingredient(name="2 tablespoons onion, chopped", recipe=recipe1)
session.add(ingredient15)
session.commit()

ingredient16 = Ingredient(name="1/2 teaspoons dry mustard", recipe=recipe1)
session.add(ingredient16)
session.commit()

ingredient17 = Ingredient(name="1 clove crushed garlic", recipe=recipe1)
session.add(ingredient17)
session.commit()


# create second recipe for category1
recipe2 = Recipe(name="Southern BBQ Chicken", category=category1)
session.add(recipe2)
session.commit()

# create ingredients for recipe2
ingredient1 = Ingredient(name="2 tablespoon brown sugar", recipe=recipe2)
session.add(ingredient1)
session.commit()

ingredient2 = Ingredient(name="2 large cloves garlic, chopped", recipe=recipe2)
session.add(ingredient2)
session.commit()

ingredient3 = Ingredient(name="2 tablesppons salt", recipe=recipe2)
session.add(ingredient3)
session.commit()

ingredient4 = Ingredient(name="1 teaspoons black pepper", recipe=recipe2)
session.add(ingredient4)
session.commit()

ingredient5 = Ingredient(name="10 chicken drumsticks", recipe=recipe2)
session.add(ingredient5)
session.commit()

ingredient6 = Ingredient(name="2 tablespoons vegetable oil", recipe=recipe2)
session.add(ingredient6)
session.commit()

ingredient7 = Ingredient(name="1/2 cup finely chopped onion", recipe=recipe2)
session.add(ingredient7)
session.commit()

ingredient8 = Ingredient(name="3/4 cup ketchup", recipe=recipe2)
session.add(ingredient8)
session.commit()

ingredient9 = Ingredient(name="2 tablespoons white wine vinegar", recipe=recipe2)
session.add(ingredient9)
session.commit()

ingredient10 = Ingredient(name="2 tablespoons Worcestershire sauce", recipe=recipe2)
session.add(ingredient10)
session.commit()

# Now Create a second category, its 2 recipes with their ingredients
category2 = Category(name="Vegetarian", user=user1)
session.add(category2)
session.commit()

recipe3 = Recipe(name="Vegetarian Korma", category=category2)
session.add(recipe3)
session.commit()

ingredient1 = Ingredient(name="1 1/2 tablespoons vegetable oil", recipe=recipe3)
session.add(ingredient1)
session.commit()

ingredient2 = Ingredient(name="1 small onion, diced", recipe=recipe3)
session.add(ingredient2)
session.commit()

ingredient3 = Ingredient(name="1 teaspoon minced fresh ginger root", recipe=recipe3)
session.add(ingredient3)
session.commit()

ingredient4 = Ingredient(name="4 cloves garlic, minced", recipe=recipe3)
session.add(ingredient4)
session.commit()

ingredient5 = Ingredient(name="2 potatoes, cubed", recipe=recipe3)
session.add(ingredient5)
session.commit()

ingredient6 = Ingredient(name="4 carrots, cubed", recipe=recipe3)
session.add(ingredient6)
session.commit()

ingredient7 = Ingredient(name="1 fresh jalapeno pepper, seeded and sliced", recipe=recipe3)
session.add(ingredient7)
session.commit()

ingredient8 = Ingredient(name="3 tablespoons ground unsalted cashews", recipe=recipe3)
session.add(ingredient8)
session.commit()

ingredient9 = Ingredient(name="1 (4 ounce) can tomato sauce", recipe=recipe3)
session.add(ingredient9)
session.commit()

ingredient10 = Ingredient(name="2 teaspoons salt", recipe=recipe3)
session.add(ingredient10)
session.commit()


recipe4 = Recipe(name="Spinach Quiche", category=category2)
session.add(recipe4)
session.commit()

ingredient1 = Ingredient(name="1 (10ounce) package frozen chopped spinach, thawed", recipe=recipe4)
session.add(ingredient1)
session.commit()

ingredient2 = Ingredient(name="1 bunch green onions, finely chopped (white parts only)", recipe=recipe4)
session.add(ingredient2)
session.commit()

ingredient3 = Ingredient(name="4 eggs, beaten", recipe=recipe4)
session.add(ingredient3)
session.commit()

ingredient4 = Ingredient(name="1 (16 ounce) package cottage cheese", recipe=recipe4)
session.add(ingredient4)
session.commit()

ingredient5 = Ingredient(name="2 cups shredded Cheddar cheese", recipe=recipe4)
session.add(ingredient5)
session.commit()

ingredient6 = Ingredient(name="1/4 cup crushed croutons", recipe=recipe4)
session.add(ingredient6)
session.commit()


# Add last category, its recipes and their ingredients
category3 = Category(name="Dessert", user=user1)
session.add(category3)
session.commit()

recipe5 = Recipe(name="Chef John's Pumpkin Pie", category=category3)
session.add(recipe5)
session.commit()

ingredient1 = Ingredient(name="1 (15 ounce) can pumpkin puree", recipe=recipe5)
session.add(ingredient1)
session.commit()

ingredient2 = Ingredient(name="3 egg yolks", recipe=recipe5)
session.add(ingredient2)
session.commit()

ingredient3 = Ingredient(name="1 large egg", recipe=recipe5)
session.add(ingredient3)
session.commit()

ingredient4 = Ingredient(name="1 (14ounce) can sweetened condensed milk", recipe=recipe5)
session.add(ingredient4)
session.commit()

ingredient5 = Ingredient(name="1 teaspoon ground cinnamon", recipe=recipe5)
session.add(ingredient5)
session.commit()

ingredient6 = Ingredient(name="1/2 teaspoon ground ginger", recipe=recipe5)
session.add(ingredient6)
session.commit()

ingredient7 = Ingredient(name="1/2 teaspoon fine salt", recipe=recipe5)
session.add(ingredient7)
session.commit()

ingredient8 = Ingredient(name="1/4 teaspoon freshly grated nutmeg", recipe=recipe5)
session.add(ingredient8)
session.commit()

ingredient9 = Ingredient(name="1/8 teaspoon Chines 5-spice poweder", recipe=recipe5)
session.add(ingredient9)
session.commit()

ingredient10 = Ingredient(name="1 9-inch unbaked pie crust", recipe=recipe5)
session.add(ingredient10)
session.commit()


recipe6 = Recipe(name="Maple Pecan Shortbread Squares", category=category3)
session.add(recipe6)
session.commit()

ingredient1 = Ingredient(name="1 cup all-purpose flour", recipe=recipe6)
session.add(ingredient1)
session.commit()

ingredient2 = Ingredient(name="1/2 cup softened butter", recipe=recipe6)
session.add(ingredient2)
session.commit()

ingredient3 = Ingredient(name="1 egg", recipe=recipe6)
session.add(ingredient3)
session.commit()

ingredient4 = Ingredient(name="1/3 cup packed brown sugar", recipe=recipe6)
session.add(ingredient4)
session.commit()

ingredient5 = Ingredient(name="3 tablespoons pure maple syrup", recipe=recipe6)
session.add(ingredient5)
session.commit()

ingredient6 = Ingredient(name="1/2 cup chopped pecans", recipe=recipe6)
session.add(ingredient6)
session.commit()
