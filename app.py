import os
from flask import Flask, jsonify
from flask_restful import Api

from db import db
from resources.recipe import NewRecipe, Recipe, RecipeListAll, RecipeListType, RecipeListChef
from resources.ingredient import NewIngredient, Ingredient, IngredientList
from resources.recipe_ingredient import RecipeIngredient, RecipeIngredientList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(NewRecipe, '/recipe')
api.add_resource(Recipe, '/recipe/<int:recipe_id>')
api.add_resource(RecipeListAll, '/recipes')
api.add_resource(RecipeListType, '/recipes/<string:type>')
api.add_resource(RecipeListChef, '/my_recipes/<int:chef_id>')

api.add_resource(NewIngredient, '/ingredient')
api.add_resource(Ingredient, '/ingredient/<int:ingredient_id>')
api.add_resource(IngredientList, '/ingredients/')

api.add_resource(RecipeIngredient,
                 '/recipe_ingredient/<int:recipe_id>/<int:ingredient_id>')
api.add_resource(RecipeIngredientList, '/recipe_ingredients/<int:recipe_id>')

db.init_app(app)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
