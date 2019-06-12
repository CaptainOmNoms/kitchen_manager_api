from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.recipe import RecipeModel

class Recipe(Resource):
    @jwt_required
    def get(self, _id):
        recipe = RecipeModel.find_by_id(_id)
        if recipe:
            return recipe.json()
        return {'message': 'Recipe not found'}, 404
    
    @jwt_required
    def post(self, _id, name):
        pass
       
    @jwt_required
    def delete(self, _id):
        pass   
    

class RecipeList(Resource):
    @jwt_required
    def get(self):
        return {'recipes' : [ recipe.json() for recipe in RecipeModel.find_all()]}
