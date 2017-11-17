import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serializable(self):
        return {
            'name': self.name,
            'id': self.id,
        }


class Recipe(Base):
    __tablename__ = 'recipe'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serializable(self):
        return {
            'name': self.name,
            'id': self.id,
            'category_id': self.category_id,
        }


class Ingredient(Base):
    __tablename__ = 'ingredient'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    recipe = relationship(Recipe)

    @property
    def serializable(self):
        return {
            'name': self.name,
            'id': self.id,
            'recipe_id': self.recipe_id,
        }


engine = create_engine('sqlite:///recipes.db')


Base.metadata.create_all(engine)
