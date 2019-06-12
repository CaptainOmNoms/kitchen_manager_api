from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from resources.user import User, UserLogin, UserLogout
from resources.ingredient import Ingredient, IngredientList
from resources.recipe import Recipe, RecipeList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api.Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

# TODO: Add claims loader
# TODO: Add jwt token refreshing and reloading


# TODO: uncomment endpoints as resources/models are created

# api.add_resource('Recipe', '/recipe/<int:recipe_id>')
# api.add_resource('RecipeList', '/recipes')
# api.add_resource('Ingredient', '/ingredient/<int:ingredient_id>')
# api.add_resource('IngredientList', '/ingredients/')
# api.add_resource('User', '/user/<int:user_id>')
# api.add_resource('UserLogin', '/login')
# api.add_resource('UserLogout', '/logout')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
