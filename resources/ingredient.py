from flask_restful import Resource, reqparse
from models.ingredient import IngredientModel


class NewIngredient(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('measurement',
                        type=str,
                        required=True,
                        help="Every igredient needs a measurement type."
                        )

    
    def post(self):
        data = self.parser.parse_args()

        if IngredientModel.find_by_name_measurement(data['name'], data['measurement']):
            return {'message': 'An ingredient with that name and measurement type already exists'}

        ingredient = IngredientModel(**data)

        try:
            ingredient.save_to_db()
        except:
            return {'message': 'An error occurred while inserting the ingredient'}, 500
        return ingredient.json(), 201


class Ingredient(Resource):
    def get(self, ingredient_id):
        ingredient = IngredientModel.find_by_id(ingredient_id)
        if ingredient:
            return ingredient.json()
        return {'message': 'Ingredient not found '}

    def delete(self, ingredient_id):
        ingredient = IngredientModel.find_by_id(ingredient_id)

        if ingredient:
            ingredient.delete_from_db()
            return {'message': 'Ingredient deleted.'}
        return {'message': 'Ingredient not found.'}, 404


class IngredientList(Resource):
    def get(self):
        ingredients = [x.json() for x in IngredientModel.find_all()]
        return {'ingredients': ingredients}, 200
