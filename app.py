import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import json
from flask_cors import CORS

from models import db_drop_and_create_all, setup_db, Actor, Movie
from auth.auth import AuthError, requires_auth



# def create_app(test_config=None):
# create and configure the app
def create_app(test_config=None):
  # create and configure the app

  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  # db_drop_and_create_all()


  @app.route('/')
  def index():
    return 'Hello'

  '''
  Movies endpoint 
  '''

  @app.route('/movies')
  @requires_auth('get:movies')
  def get_movies(payload):
    
    movies = Movie.query.order_by(Movie.title).all()
    # for drink in drinks:
    #   print(drink.title)
    data = [movie.format() for movie in movies]

    if len(data) == 0 :
      abort(404)

    return jsonify({
      'success': True,
      'movies': data
    }), 200

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def post_movies(payload):

    title = request.json.get('title', None)
    release_date = request.json.get('release_date', None)

      # recipe = json.dumps(request.json.get('recipe', None))
    
    if title is None or release_date is None:
      abort(422) 

    try:
      movie = Movie(
      title = title,
      release_date = release_date
      )
    
      movie.insert()

      return jsonify({
        'success': True,
        'movie': movie.format()
      }), 200

    except:
      abort(422)

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_drinks(payload,movie_id):
      
    title = request.json.get('title', None)
    release_date = request.json.get('release_date', None)

    if title is None or release_date is None:
        abort(422)     


    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    
    
    if movie is None:
        abort(404)

    try:
        movie.title = title
        movie.release_date = release_date
        movie.update()

        data = []
        data.extend((movie.title, movie.release_date))

        return jsonify({
          'success': True,
          'movies':data
        }), 200

    except:
      abort(422)

  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload,movie_id):
    try:
      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

      if movie is None:
        abort(404)

      movie.delete()

      return jsonify({
        'success':True,
        'deleted':movie_id
      }),200
    except:
      abort(422)

  # '''
  # Actor endpoint
  # '''

  @app.route('/actors')
  @requires_auth('get:actors')
  def get_actors(payload):
    
    actors = Actor.query.order_by(Actor.id).all()
    # for drink in drinks:
    #   print(drink.title)
    data = [actor.format() for actor in actors]

    if len(data) == 0 :
      abort(404)

    return jsonify({
      'success': True,
      'actors': data
    }), 200

  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def post_actors(payload):

    name = request.json.get('name', None)
    age = request.json.get('age', None)
    gender = request.json.get('gender', None)
    # movie_id = request.json.get('movie_id', None)

      # recipe = json.dumps(request.json.get('recipe', None))
    
    if name is None or age is None or gender is None:
      abort(422) 

    try:

      actor = Actor(
      name = name,
      age = age,
      gender = gender
      )
    
      actor.insert()

      return jsonify({
        'success': True,
        'actors': actor.format()
      }), 200

    except:
      abort(422)

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actors(payload,actor_id):
      
    name = request.json.get('name', None)
    age = request.json.get('age', None)
    gender = request.json.get('gender', None)
    # movie_id = request.json.get('movie_id', None)


      # recipe = json.dumps(request.json.get('recipe', None))
    
    if name is None or age is None or gender is None:
      abort(422)    


    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    
    
    if actor is None:
        abort(404)

    try:
        actor.name = name
        actor.age = age
        actor.gender = gender
        # actor.movie_id = movie_id

        actor.update()

        data = []
        data.extend((actor.name, actor.age, actor.gender))

        return jsonify({
          'success': True,
          'actors':data
        }), 200

    except:
      abort(422)

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actors(payload,actor_id):
    try:
      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

      if actor is None:
        abort(404)

      actor.delete()

      return jsonify({
        'success':True,
        'deleted':actor_id
      }),200
    except:
      abort(422)
  # APP = create_app()


  ## Error Handling

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
                      "success": False, 
                      "error": 422,
                      "message": "unprocessable"
                      }), 422

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success":False,
        "error":404,
        "message":"resource not found"
    }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
        "success":False,
        "error":405,
        "message":"methode not allowed"
    }), 405

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
    "success":False,
    "error":400,
    "message":"bad request"
    }), 400

  @app.errorhandler(401)
  def Unauthorized(error):
    return jsonify({
    "success":False,
    "error":401,
    "message": "Unauthorized"
    }), 401

  @app.errorhandler(403)
  def Forbidden(error):
    return jsonify({
    "success":False,
    "error":403,
    "message": "Forbidden"
    }), 403


  @app.errorhandler(AuthError)
  def auth_error(e):
      return jsonify(e.error), e.status_code

  # if __name__ == '__main__':
  #     app.run()

  return app

app = create_app()

if __name__ == '__main__':
  app.run()