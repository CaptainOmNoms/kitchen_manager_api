from flask_restful import Resource, reqparse
from flask_jwt_extended import fresh_jwt_required
from models.ingredient import IngredientModel
from models.recipe_ingredient import RecipeIngredientModel


class RecipeIngredient(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('amount', type=float, required=True, help="This field cannot be left blank!")
    parser.add_argument('recipe_id', type=int, required=True, help="Need a recipe for which this ingredient belongs to!")
    parser.add_argument('ingredient_id', type=int, required=True, help="Need an ingredient to add to a recipe!")

    @fresh_jwt_required
    def post(self):
        data = RecipeIngredient.parser.parse_args()
        if IngredientModel.find_by_id(data['ingredient_id']):
            return {'message': "That ingredient does not exist"}, 404
        if RecipeModel.find_by_id(['recipe_id']):
            return {'message': "That recipe does not exist"}, 404

        ri = RecipeIngredientModel(**data)

        try:
            ri.save_to_db()
        except:
            return {"message": "An error occurred inserting the recipe ingredient."}, 500
        return ri.json(), 201

    @fresh_jwt_required
    def delte(self, recipe_id, ingredient_id):
        ri = RecipeIngredientModel.find_by_recipe_ingredient(recipe_id, ingredient_id)

        if ri:
            ri.delete_from_db()
            return {'message': 'Recipe ingredient deleted.'}
        return {'message': 'Recipe ingredient not found'}, 404

    @fresh_jwt_required
    def put(self, amount, recipe_id, ingredient_id):
        data = RecipeIngredient.parser.parse_args()

        ri = RecipeIngredientModel.find_by_recipe_ingredient(recipe_id, ingredient_id)
        if ri:
            ri.amount = data['amount']
        else:
            ri = RecipeIngredientModel(**data)

        ri.save_to_db()
        return ri.json()


class RecipeIngredientList(Resource):
    
    @fresh_jwt_required
    def get(self, recipe_id):
        return {'ingredients': [x.json() for x in self.find_by_recipe(recipe_id)]}