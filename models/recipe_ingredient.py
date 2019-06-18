from db import db

class RecipeIngredientModel(db.Model):
    __tablename__ = 'recipe_ingredients'
    
    recipe_ingredient_id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'))
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.ingredient_id'))
    amount = db.Column(db.Float(precision=2))
    recipe = db.relationship('RecipeModel')
    ingredient = db.relationship('IngredientModel')
    
    def __init__(self, amount, recipe_id, ingredient_id):
        self.recipe_id = recipe_id
        self.ingredient = ingredient_id
        self.amount = amount
        
    def json(self):
        return {'amount': self.amount, 'ingredient': self.Ingredient.name}
        
    @classmethod
    def find_by_recipe(cls, recipe_id):
        return cls.query.filter_by(recipe_id=recipe_id)
    
    @classmethod
    def find_by_recipe_ingredient(cls,recipe_id, ingredient_id):
        return cls.query.filter_by(recipe_id=recipe_id).filter(ingredient_id=ingredient_id)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()