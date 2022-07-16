from sqlalchemy.dialects.postgresql import UUID
import uuid
import marshmallow as ma
from db import db

from models.actors_model import ActorsSchema
from models.directors_model import DirectorsSchema

class Movies(db.Model):
    __tablename__ = "movies"
    movie_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    movie_name = db.Column(db.String(), nullable=False)
    actor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('actors.actor_id'), nullable=False)
    actor_first_name = db.Column(db.String())
    actor_last_name = db.Column(db.String())
    director_id = db.Column(UUID(as_uuid=True), db.ForeignKey('directors.director_id'), nullable=False)
    director_first_name = db.Column(db.String(), nullable=False)
    director_last_name = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), nullable = False, default = True)
    actors = db.relationship('Actors', backref="actors", lazy=True)
    director = db.relationship('Directors', backref='director', lazy=True)

    def __init__(self, movie_name, actor_id, actor_first_name, actor_last_name, director_id, director_first_name, director_last_name):
        self.movie_name = movie_name
        self.actor_id = actor_id
        self.actor_first_name = actor_first_name
        self.actor_last_name = actor_last_name
        self.director_id = director_id
        self.director_first_name = director_first_name
        self.director_last_name = director_last_name

class MoviesSchema(ma.Schema):
    class Meta:
        fields = ['movie_id', 'movie_name', 'actors', 'director', 'active']
    actors = ma.fields.Nested(ActorsSchema(only=('actor_first_name', 'actor_last_name')))
    director = ma.fields.Nested(DirectorsSchema(only=('director_first_name', 'director_last_name')))

movie_schema = MoviesSchema()
movies_schema = MoviesSchema(many=True)