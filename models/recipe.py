from db import db

class RecipeModel(db.Model):
    __tablename__ = 'recipes'

    recipe_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    recipe_type = db.Column(db.String(15))
    description = db.Column(db.Text)
    steps = db.Column(db.Text)
    servings = db.Column(db.Integer)
    prep_min = db.Column(db.Integer)
    cook_min = db.Column(db.Integer)

    def __init__(self, name, recipe_type, description, steps, servings, prep_min, cook_min):
        self.name = name
        self.recipe_type = recipe_type
        self.description = description
        self.steps = steps
        self.servings = servings
        self.prep_min = prep_min
        self.cook_min = cook_min

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

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
