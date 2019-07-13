from flask_restful import Resource, reqparse
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
    parser.add_argument('chef_name',
                        type=str,
                        required=True,
                        help="Someone came up with this"
                        )
    parser.add_argument('chef_id',
                        type=int,
                        required=True,
                        help="We need your id pls"
                        )

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
    def get(self, recipe_id):
        recipe = RecipeModel.find_by_id(recipe_id)
        if recipe:
            return recipe.json()
        return {'message': 'Recipe not found'}, 404

    def delete(self, recipe_id):
        data = NewRecipe.parser.parse_args()


        recipe = RecipeModel.find_by_id(recipe_id)
        if recipe:
            if recipe.chef_id == data['chef_id']:
                recipe.delete_from_db()
                return {'message': 'Recipe deleted'}
            else:
                return {'message': 'You can not delete this recipe as you are not the chef.'}, 401
        return {'message': 'Recipe not found'}, 404

    def put(self, recipe_id):
        data = NewRecipe.parser.parse_args()

        recipe = RecipeModel.find_by_id(recipe_id)

        if recipe:
            if recipe.chef_id == data['chef_id']:
                recipe.name = data['name']
                recipe.recipe_type = data['recipe_type']
                recipe.description = data['description']
                recipe.steps = data['steps']
                recipe.servings = data['servings']
                recipe.prep_min = data['prep_min']
                recipe.cook_min = data['cook_min']
            else:
                return {'message': 'You can not change this recipe as you are not the chef.'}, 401
        else:
            recipe = RecipeModel(**data)

        recipe.save_to_db()
        return recipe.json(), 201


class RecipeListAll(Resource):
    def get(self):
        return {'recipes': [recipe.json() for recipe in RecipeModel.find_all()]}

class RecipeListType(Resource):
    def get(self, type):
        return {'recipes': [recipe.json() for recipe in RecipeModel.find_by_type(type)]}

class RecipeListChef(Resource):
    def get(self, chef_id):
        return {'recipes': [recipe.json() for recipe in RecipeModel.find_by_chef_id(chef_id)]}
