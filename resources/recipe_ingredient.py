from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_claims, get_jwt_identity,  fresh_jwt_required
from models.ingredient import IngredientModel
from models.recipe import RecipeModel
from models.recipe_ingredient import RecipeIngredientModel


class RecipeIngredient(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('amount', type=float, required=True,
                        help="This field cannot be left blank!")

    def post(self, recipe_id, ingredient_id):
        data = RecipeIngredient.parser.parse_args()
        if not IngredientModel.find_by_id(ingredient_id):
            return {'message': "That ingredient does not exist"}, 404
        if not RecipeModel.find_by_id(recipe_id):
            return {'message': "That recipe does not exist"}, 404
        if RecipeIngredientModel.find_by_recipe_ingredient(recipe_id, ingredient_id):
            return {'message': "That recipe already contains that ingredient."}
        ri = RecipeIngredientModel(data['amount'], recipe_id, ingredient_id)
        print(ri.json())

        try:
            ri.save_to_db()
        except:
            return {"message": "An error occurred inserting the recipe ingredient."}, 500
        return ri.json(), 201

    def delete(self, recipe_id, ingredient_id):
        ri = RecipeIngredientModel.find_by_recipe_ingredient(
            recipe_id, ingredient_id)

        if ri:
            ri.delete_from_db()
            return {'message': 'Recipe ingredient deleted.'}
        return {'message': 'Recipe ingredient not found'}, 404

    def put(self, recipe_id, ingredient_id):
        data = RecipeIngredient.parser.parse_args()

        ri = RecipeIngredientModel.find_by_recipe_ingredient(
            recipe_id, ingredient_id)
        if ri:
            ri.amount = data['amount']
        else:
            ri = RecipeIngredientModel(
                data['amount'], recipe_id, ingredient_id)

        ri.save_to_db()
        return ri.json(), 201


class RecipeIngredientList(Resource):

    def get(self, recipe_id):
        return {'ingredients': [x.json() for x in RecipeIngredientModel.find_by_recipe(recipe_id)]}
