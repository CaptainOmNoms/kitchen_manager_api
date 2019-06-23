from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_claims, get_jwt_identity,  fresh_jwt_required
from models.recipe import RecipeModel


class NewRecipe(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="It has to be named something"
                        )
    parser.add_argument('recipe_type',
                        type=str,
                        required=True,
                        help="If it doesnt fit into any, just pick one"
                        )
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="Just write a description!"
                        )
    parser.add_argument('steps',
                        type=str,
                        required=True,
                        help="How do you expect me to make this without steps?"
                        )
    parser.add_argument('servings',
                        type=int,
                        required=False,
                        default=1
                        )
    parser.add_argument('prep_min',
                        type=int,
                        required=True,
                        help="It takes no time to prep?"
                        )
    parser.add_argument('cook_min',
                        type=int,
                        required=True,
                        help="It takes no time to make?"
                        )

    @fresh_jwt_required
    def post(self):
        data = self.parser.parse_args()
        if RecipeModel.find_by_name(data['name']):
            return {'message': "A recipe with name '{}' already exists.".format(data['name'])}, 400

        recipe = RecipeModel(**data)
        try:
            recipe.save_to_db()
        except:
            return {"message": "An error occurred creating the recipe."}, 500

        return recipe.json(), 201


class Recipe(Resource):
    @fresh_jwt_required
    def get(self, recipe_id):
        recipe = RecipeModel.find_by_id(recipe_id)
        if recipe:
            return recipe.json()
        return {'message': 'Recipe not found'}, 404

    @fresh_jwt_required
    def delete(self, recipe_id):
        claims = get_jwt_claims()
        if not claims['admin']:
            return {'message': 'Admin privilege required.'}, 401

        recipe = RecipeModel.find_by_id(recipe_id)
        if recipe:
            recipe.delete_from_db()
            return {'message': 'Recipe deleted'}
        return {'message': 'Recipe not found'}, 404

    @fresh_jwt_required
    def put(self, recipe_id):
        data = NewRecipe.parser.parse_args()

        recipe = RecipeModel.find_by_id(recipe_id)

        if recipe:
            recipe.name = data['name']
            recipe.recipe_type = data['recipe_type']
            recipe.description = data['description']
            recipe.steps = data['steps']
            recipe.servings = data['servings']
            recipe.prep_min = data['prep_min']
            recipe.cook_min = data['cook_min']
        else:
            recipe = RecipeModel(**data)

        recipe.save_to_db()
        return recipe.json(), 201


class RecipeList(Resource):
    @fresh_jwt_required
    def get(self):
        return {'recipes': [recipe.json() for recipe in RecipeModel.find_all()]}
