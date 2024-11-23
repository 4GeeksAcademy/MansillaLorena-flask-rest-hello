"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorites_characters, Favorites_planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def get_all_user():
    users = User.query.all()
    users_serialized = []
    for user in users :
       users_serialized.append (user.serialized())
       return jsonify({'msg': 'Ok', 'data' : 'users_serialized'}), 200


@app.route('/character', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    character_serialized = []
    for character in characters :
        character_serialized.append (character.serialized())
       
    return jsonify({'msg': 'Ok', 'data' : character_serialized}), 200
    

@app.route( '/planet', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    planet_serialized = []
    for planet in planets :
        planet_serialized.append (planet.serialized())
        
    return jsonify({'msg': 'Ok', 'data' : planet_serialized}), 200
    

@app.route('/character/<int:id>', methods=['GET'])
def get_characters(id):
    character = Character.query.get(id)
    character_serialized = character.serialized()
    return jsonify({
        'msg': 'ok',
        'data': character_serialized
        })
    

@app.route('/planet/<int:id>', methods=['GET'])
def get_planets(id):
    planet = Planet.query.get(id)
    planet_serialized = planet.serialized()
    return jsonify({
        'msg': 'ok',
        'data': planet_serialized
        })


@app.route('/favorites_planets/<int:user_id>', methods=['GET'])
def get_favorites_by_user(user_id):
    user = User.query.get(user_id)
    favorites_planets_serialized = []
    for fav_planet in user.planet_favorites:
        favorites_planets_serialized.append(fav_planet.planet_relationship.serialized())
    data = {
        'user_info': user.serialized(),
        'planets_favorites': favorites_planets_serialized
    }
    return jsonify({'msg':'ok', 'data': data})


@app.route('/favorites_characters/<int:user_id>', methods=['GET'])
def get_favorites_user(user_id):
    user = User.query.get(user_id)
    favorite_characters_serialized = []
    for fav_character in user.planet_favorites:
        favorite_characters_serialized.append(fav_character.character_relationship.serialized())
    data = {
        'user_info': user.serialized(),
        'planets_favorites': favorite_characters_serialized
    }
    return jsonify({'msg':'ok', 'data': data})


@app.route( '/favorite/planet/<int:planet_id>/<int:user_id>', methods=['POST'])
def add_favorite_planet(planet_id, user_id):
    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)
    if not user or not planet:
        return jsonify({'msg': 'User or Planet not found'}), 404

    new_favorite = Favorites_planets(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({'msg': 'Favorite Planet added successfully'}), 201


@app.route( '/favorite/character/<int:character_id>/<int:user_id>', methods=['POST'])
def add_favorite_character(character_id, user_id):
    user = User.query.get(user_id)
    character = Character.query.get(character_id)
    if not user or not character:
        return jsonify({'msg': 'User or Character not found'}), 404

    new_favorite = Favorites_characters(user_id=user_id, character_id=character_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({'msg': 'Favorite character added successfully'}), 201

@app.route( '/favorite/planet/<int:planet_id>/<int:user_id>', methods=['DELETE'])
def delete_fav_planet(planet_id,user_id):
    favorite_planet= Favorites_planets.query.filter_by(planet_id=planet_id,user_id=user_id).first()
    #print(favorite_planet)
    db.session.delete(favorite_planet)
    db.session.commit()
    
    return jsonify({'msg': 'Favorite planet is delete'}), 200


@app.route( '/favorite/character/<int:character_id>/<int:user_id>', methods=['DELETE'])
def delete_fav_character(character_id,user_id):
    favorite_character= Favorites_characters.query.filter_by(character_id=character_id,user_id=user_id).first()
  
    db.session.delete(favorite_character)
    db.session.commit()
    
    return jsonify({'msg': 'Favorite character is delete'}), 200


 #   [DELETE] /favorite/planet/<int:planet_id>/<int:user_id> Elimina un planet favorito.
   # [DELETE] /favorite/character/<int:character_id>/<int:user_id> Elimina un people favorito .



    
   



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
