import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

ENV = 'prod'

if ENV == 'dev':
  # app.debug = True
  database_name = "agancy"
  database_path = "postgres://{}/{}".format('localhost:5432', database_name)
else:
  # app.debug = False
  database_path = 'postgres://yqoejtaqusepvz:25355970ef78992ba73439178894529144f78d10a057e1df26d20888ed81e22d@ec2-52-203-182-92.compute-1.amazonaws.com:5432/dap0b31vk38l09'

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
  app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db.app = app
  db.init_app(app)

  db.create_all()


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''
def db_drop_and_create_all():
  # db.drop_all()
  db.create_all()

# Movie_Actor = db.Table('movie_actor', db.Model.metadata,
#   Column('movie_id', db.Integer, db.ForeignKey('Movie.id')),
#   Column('actor_id', db.Integer, db.ForeignKey('Actor.id')),
# )

class Movie(db.Model):
  __tablename__ = 'Movie'

  id = Column(Integer, primary_key=True)
  title = Column(String,unique=True ,nullable=False)
  release_date = Column(String, nullable=False)   #need to check date type
  # Movie_Actor = db.relationship('Movie_Actor', backref='Movie', lazy=True)


  # def __init__(self, title, release_date):
  #   self.title = title
  #   self.release_date = release_date


  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date
    }

  def __repr__(self):
    return f"<Movie {self.id} {self.title}>"

'''

Actors

'''

class Actor(db.Model):  
  __tablename__ = 'Actor'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False )
  age = Column(Integer,nullable=False)
  gender = Column(String, nullable=False)
  # movie_id = db.Column(db.Integer, db.ForeignKey('Movie.id'))
  # movies = db.relationship('Movie', secondary=Movie_Actor, backref='movies_list', lazy=True)
  # Movie_Actor = db.relationship('Movie_Actor', backref='Actor', lazy=True)

  def __repr__(self):
    return f"<Actor {self.id} {self.name}>"


  # def __init__(self, name,age,gender):
  #   self.name = name
  #   self.age = age
  #   self.gender = gender

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender
    }