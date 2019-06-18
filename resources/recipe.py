from flask_restful import Resource, reqparse
from flask_jwt_extended import fresh_jwt_required
from models.recipe import RecipeModel

class Recipe(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type='string',
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @fresh_jwt_required
    def get(self, _id):
        recipe = RecipeModel.find_by_id(_id)
        if recipe:
            return recipe.json()
        return {'message': 'Recipe not found'}, 404

    @fresh_jwt_required
    def post(self, _id):
        if RecipeModel.find_by_name(name):
            return {'message': "A recipe with name '{}' already exists.".format(name)}, 400

        recipe = RecipeModel(**data)
        try:
            recipe.save_to_db()
        except:
            return {"message": "An error occurred creating the recipe."}, 500

        return recipe.json(), 201

    @fresh_jwt_required
    def delete(self, _id):
        recipe = RecipeModel.find_by_id(_id)
        if recipe:
            recipe.delete_from_db()
            return {'message': 'Recipe deleted'}
        return {'message': 'Recipe not found'}, 404

class RecipeList(Resource):
    @fresh_jwt_required
    def get(self):
        return {'recipes' : [ recipe.json() for recipe in RecipeModel.find_all()]}
