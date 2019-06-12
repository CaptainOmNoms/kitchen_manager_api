from db import db

class UserModel(db.Model)
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(12))
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def json(self):
        return {
            'user_id': self.id,
            'username': self.username
        }
        
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()    