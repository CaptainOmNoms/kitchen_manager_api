import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from blacklist import BLACKLIST
from resources.recipe import NewRecipe, Recipe, RecipeList
from resources.ingredient import NewIngredient, Ingredient, IngredientList
from resources.recipe_ingredient import RecipeIngredient, RecipeIngredientList
from resources.user import User, UserRegister, UserLogin, UserLogout, TokenRefresh


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:  # eventually this needs to be changed to be controlled by a enviornment variable or a db lookup
        return {'admin': True}
    return {'admin': False}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
# we have to keep the argument here, since it's passed in by the caller internally
def invalid_token_callback(error):
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(NewRecipe, '/recipe')
api.add_resource(Recipe, '/recipe/<int:recipe_id>')
api.add_resource(RecipeList, '/recipes')

api.add_resource(NewIngredient, '/ingredient')
api.add_resource(Ingredient, '/ingredient/<int:ingredient_id>')
api.add_resource(IngredientList, '/ingredients/')

api.add_resource(RecipeIngredient,
                 '/recipe_ingredient/<int:recipe_id>/<int:ingredient_id>')
api.add_resource(RecipeIngredientList, '/recipe_ingredients/<int:recipe_id>')

api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
db.init_app(app)

if __name__ == '__main__':

    app.run(port=5000, debug=True)
