from db import db


class IngredientModel(db.Model):
    __tablename__ = 'ingredients'

    ingredient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    measurement = db.Column(db.String(10))

    def __init__(self, name, measurement):
        self.name = name
        self.measurement = measurement

    def json(self):
        return {
            'id': self.ingredient_id,
            'name': self.name,
            'measurement': self.measurement
        }

    @classmethod
    def find_by_name_measurement(cls, name, measurement):
        return cls.query.filter_by(name=name).filter_by(measurement=measurement).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
