from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False,unique=True)
    firstname= db.Column(db.String(30))
    email= db.Column(db.String(40),nullable=False,unique=True)
    password=db.Column(db.String(12),nullable=False)
    
    favorites_planets= db.relationship('Favorites_planets',back_populates='user')
    favorites_characters= db.relationship('Favorites_characters',back_populates='user')

    def __repr__(self):
        return  f'Usuario {self.email} {self.id}'

    def serialized(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "firstname": self.firstname
            # do not serialize the password, its a security breach
        }


class Favorites_planets(db.Model):
    __tablename__ = 'favorites_planets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer,db.ForeignKey('planet.id'))
    planet= db.Column(db.Integer,db.ForeignKey('planet.id'))
    
    user = db.relationship('User',back_populates='favorites_planets')
    planet = db.relationship('Planet',back_populates='favorites_planets')

    def __repr__(self):
        return  f'Planet {self.id} {self.user_id}{self.planet_id}{self.planet}'

    def serialized(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id" : self.planet_id,
            "planet" : self.planet
        }

      
class Favorites_characters(db.Model):
    __tablename__='favorites_characters'
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    character_id=db.Column(db.Integer,db.ForeignKey('character.id'))
    character= db.Column(db.Integer,db.ForeignKey('character.id'))
    
    user = db.relationship('User',back_populates='favorites_characters')
    character= db.relationship('Character',back_populates='favorites_characters')

    def __repr__(self):
        return  f'Planet {self.id} {self.user_id}{self.character_id}{self.character}'

    def serialized(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id" : self.character_id,
            "character" : self.character
        }


class Planet(db.Model):
    __tablename__='planet'
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),nullable = False, unique = True)

    favorites_planets= db.relationship('Favorites_planets',back_populates='planet')

    def __repr__(self):
        return  f'Planet {self.id} {self.name}'

    def serialized(self):
        return {
            "id": self.id,
            "name": self.name
        }
    
class Character(db.Model):
    __tablename__='character'
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),nullable=False,unique=True)

    favorites_characters= db.relationship('Favorites_characters',back_populates='character')

    def __repr__(self):
        return  f'Planet {self.id} {self.name}'

    def serialized(self):
        return {
            "id": self.id,
            "name": self.name
        }


    
    def to_dict(self):
        return {}
