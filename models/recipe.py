from db import db
import enum

class RecipeTypes(enum.Enum):
    appitizer = 0
    breakfast = 1
    lunch = 2
    dinner = 3
    dessert = 4
    drink = 5

class RecipeModel(db.Model):
    __tablename__ = 'recipes'

    recipe_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    type = db.Column(db.Enum(RecipeTypes))
    description = db.Column(db.Text)
    steps = db.Column(db.Text)
    servings = db.Column(db.int)
    prep_min = db.Column(db.int)
    cook_min = db.Column(db.int)
    ingredients = db.relationship('RecipeIngredientsModel', lazy='dynamic')
    
    
    def __init__(self, name):
        self.name = name
        
    def json(self):
        return {
            'id': self.recipe_id,
            'name': self.name,
            'type': self.type,
            'description': self.description,
            'servings': self.servings,
            'prep_min': self.prep_min,
            'cook_min': self.cook_min,
            'steps': [x.ingredient.json() for x in self.ingredients.all()]
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
          
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
