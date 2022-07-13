from flask import request, Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.dialects.postgresql import UUID
import uuid
import marshmallow as mar

app = Flask(__name__)

database_host = "127.0.01:5432"
database_name = "movies"
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{database_host}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

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

class Actors(db.Model):
    __tablename__= 'actors'
    actor_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    actor_first_name = db.Column(db.String(), nullable=False)
    actor_last_name = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), nullable = False, default = True)

    def __init__(self, actor_first_name, actor_last_name):
        self.actor_first_name = actor_first_name
        self.actor_last_name = actor_last_name

class ActorsSchema(ma.Schema):
    class Meta:
        fields = ['actor_id', 'actor_first_name', 'actor_last_name', 'active']

actor_schema = ActorsSchema()
actors_schema = ActorsSchema(many=True)

class Directors(db.Model):
    __tablename__= 'directors'
    director_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    director_first_name = db.Column(db.String(), nullable=False)
    director_last_name = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), nullable = False, default = True)

    def __init__(self, director_first_name, director_last_name):
        self.director_first_name = director_first_name
        self.director_last_name = director_last_name

class DirectorsSchema(ma.Schema):
    class Meta:
        fields = ['director_id', 'director_first_name', 'director_last_name', 'active']

director_schema = DirectorsSchema()
directors_schema = DirectorsSchema(many=True)

class MoviesSchema(ma.Schema):
    class Meta:
        fields = ['movie_id', 'movie_name', 'actors', 'director', 'active']
    actors = mar.fields.Nested(ActorsSchema(only=('actor_first_name', 'actor_last_name')))
    director = mar.fields.Nested(DirectorsSchema(only=('director_first_name', 'director_last_name')))

movie_schema = MoviesSchema()
movies_schema = MoviesSchema(many=True)

def create_all():
    db.create_all()

    print("Querying for Movie...")
    movie_data = db.session.query(Movies).filter(Movies.movie_name == "Top Gun").first()
    if movie_data == None:
        print("Movie not found! Creating Top Gun...")
        actor_data = db.session.query(Actors).filter(Actors.actor_first_name == "Tom").first()
        director_data = db.session.query(Directors).filter(Directors.director_first_name == "Tony").first()
        if actor_data == None:
            print("Adding Actor: Tom Cruise...")
            actor_first_name = "Tom"
            actor_last_name = "Cruise"
            new_actor = Actors(actor_first_name, actor_last_name)

            db.session.add(new_actor)
            db.session.commit()
            
        if director_data == None:
            print("Adding Director: Tony Scott...")
            director_first_name = "Tony"
            director_last_name = "Scott"
            new_director = Directors(director_first_name, director_last_name)

            db.session.add(new_director)
            db.session.commit()
            
            print("Adding Movie: Top Gun...")
            new_movie = Movies("Top Gun", new_actor.actor_id, actor_first_name, actor_last_name, new_director.director_id, director_first_name, director_last_name)
            db.session.add(new_movie)
            db.session.commit()
            print("Movie Added! Starting Application...")

    else:
        print("Top Gun found! Starting Application...")

@app.route('/actors/add', methods=['POST'])
def add_actor():
    form = request.form

    actor_first_name = form.get('actor_first_name')
    actor_last_name = form.get('actor_last_name')

    new_actor = Actors(actor_first_name, actor_last_name)

    db.session.add(new_actor)
    db.session.commit()

    return actor_schema.jsonify(new_actor), 200

@app.route('/actors/list')
def get_all_actors():
    actor_records = db.session.query(Actors).all()

    return jsonify(actors_schema.dump(actor_records)), 200

@app.route('/actors/list/<actor_id>')
def get_one_actor(actor_id):
    actor_record = db.session.query(Actors).filter(Actors.actor_id == actor_id).first()

    return actor_schema.jsonify(actor_record), 200

@app.route('/actors/edit/<actor_id>', methods=['PUT'])
def edit_actor(actor_id):
    form = request.form

    actor_data = db.session.query(Actors).filter(Actors.actor_id == actor_id).first()
    actor_first_name = form.get('actor_first_name')
    actor_last_name = form.get('actor_last_name')

    if actor_data == None:
        return jsonify('ERROR: actor_id missing!'), 400
    if actor_data:
        actor_data.actor_id = actor_id
        if actor_first_name:
            actor_data.actor_first_name = actor_first_name
        if actor_last_name:
            actor_data.actor_last_name = actor_last_name
        
        db.session.commit()

        return actor_schema.jsonify(actor_data), 200

@app.route('/actors/delete/<actor_id>', methods=['DELETE'])
def delete_actor(actor_id):
    actor_data = db.session.query(Actors).filter(Actors.actor_id == actor_id).first()
    if actor_data:
        db.session.delete(actor_data)
        db.session.commit()
        return jsonify(f'Actor with actor_id {actor_id} deleted'), 200
    
    return jsonify(f'Actor with actor_id {actor_id} not found!'), 404

@app.route('/actors/deactivate/<actor_id>', methods=['PUT'])
def deactivate_actor(actor_id):
    actor_data = db.session.query(Actors).filter(Actors.actor_id == actor_id).first()
    actor_data.active = False
    db.session.commit()
    return jsonify(f'Actor with actor_id {actor_id} deactivated'), 200

@app.route('/actors/activate/<actor_id>', methods=['PUT'])
def activate_actor(actor_id):
    actor_data = db.session.query(Actors).filter(Actors.actor_id == actor_id).first()
    actor_data.active = True
    db.session.commit()
    return jsonify(f'Actor with actor_id {actor_id} activated'), 200

@app.route('/actor/search/<search_term>')
def actors_get_by_search(search_term, internal_call=False):
    search_term = search_term.lower()

    actor_data = {}

    actor_data = db.session.query(Actors).filter(db.or_( \
        db.func.lower(Actors.actor_first_name).contains(search_term), \
        db.func.lower(Actors.actor_last_name).contains(search_term)))

    if internal_call:
        return actors_schema.dump(actor_data)
    return jsonify(actors_schema.dump(actor_data))


@app.route('/directors/add', methods=['POST'])
def add_director():
    form = request.form

    director_first_name = form.get('director_first_name')
    director_last_name = form.get('director_last_name')

    new_director = Directors(director_first_name, director_last_name)

    db.session.add(new_director)
    db.session.commit()

    return director_schema.jsonify(new_director), 200

@app.route('/directors/list')
def get_all_directors():
    director_records = db.session.query(Directors).all()

    return jsonify(directors_schema.dump(director_records)), 200

@app.route('/directors/list/<director_id>')
def get_one_director(director_id):
    director_record = db.session.query(Directors).filter(Directors.director_id == director_id).first()

    return director_schema.jsonify(director_record), 200

@app.route('/directors/edit/<director_id>', methods=['PUT'])
def edit_director(director_id):
    form = request.form

    director_data = db.session.query(Directors).filter(Directors.director_id == director_id).first()
    director_first_name = form.get('director_first_name')
    director_last_name = form.get('director_last_name')

    if director_data == None:
        return jsonify("ERROR: director_id missing!"), 400
    if director_data:
        director_data.director_id = director_id
        if director_first_name:
            director_data.director_first_name = director_first_name
        if director_last_name:
            director_data.director_last_name = director_last_name
        
        db.session.commit()

        return director_schema.jsonify(director_data), 200

@app.route('/directors/delete/<director_id>', methods=['DELETE'])
def delete_director(director_id):
    director_data = db.session.query(Directors).filter(Directors.director_id == director_id).first()
    if director_data:
        db.session.delete(director_data)
        db.session.commit()
        return jsonify(f'Director with director_id {director_id} deleted'), 200
    
    return jsonify(f'Director with director_id {director_id} not found'), 404

@app.route('/directors/deactivate/<director_id>', methods=['PUT'])
def deactivate_director(director_id):
    director_data = db.session.query(Directors).filter(Directors.director_id == director_id).first()
    director_data.active = False
    db.session.commit()
    return jsonify(f'Director with director_id {director_id} deactiviated'), 200

@app.route('/directors/activate/<director_id>', methods=['PUT'])
def activate_director(director_id):
    director_data = db.session.query(Directors).filter(Directors.director_id == director_id).first()
    director_data.active = True
    db.session.commit()
    return jsonify(f'Director with director_id {director_id} activiated'), 200

@app.route('/director/search/<search_term>')
def directors_get_by_search(search_term, internal_call=False):
    search_term = search_term.lower()

    director_data = {}

    director_data = db.session.query(Directors).filter(db.or_( \
        db.func.lower(Directors.director_first_name).contains(search_term), \
        db.func.lower(Directors.director_last_name).contains(search_term)))
    if internal_call:
        return directors_schema.dump(director_data)
    return jsonify(directors_schema.dump(director_data))

@app.route('/movies/add', methods=['POST'])
def movie_add():
    form = request.form

    movie_name = form.get('movie_name')
    actor_id = form.get('actor_id')
    actor_first_name = form.get('actor_first_name')
    actor_last_name = form.get('actor_last_name')
    director_id = form.get('director_id')
    director_first_name = form.get('director_first_name')
    director_last_name = form.get('director_first_name')

    new_movie = Movies(movie_name, actor_id, actor_first_name, actor_last_name, director_id, director_first_name, director_last_name)

    db.session.add(new_movie)
    db.session.commit()

    return movie_schema.jsonify(new_movie), 200

@app.route('/movies/list')
def get_all_movies():
    movie_data = db.session.query(Movies).all()

    return jsonify(movies_schema.dump(movie_data)), 200

@app.route('/movies/list/<movie_id>')
def get_one_movie(movie_id):
    movie_record = db.session.query(Movies).filter(Movies.movie_id == movie_id).first()

    return jsonify(movie_schema.dump(movie_record)), 200

@app.route('/movies/edit/<movie_id>', methods=['PUT'])
def edit_movie(movie_id):
    form = request.form

    movie_data = db.session.query(Movies).filter(Movies.movie_id == movie_id).first()
    movie_name = form.get('movie_name')

    if movie_data == None:
        return jsonify("ERROR: movie_id missing!"), 400
    if movie_data:
        movie_data.movie_id = movie_id
        if movie_name:
            movie_data.movie_name = movie_name

        db.session.commit()

        return movie_schema.jsonify(movie_data), 200

@app.route('/movies/delete/<movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie_data = db.session.query(Movies).filter(Movies.movie_id == movie_id).first()

    if movie_data:
        db.session.delete(movie_data)
        db.session.commit()
        return jsonify(f'Movie with movie_id {movie_id} deleted')

    return jsonify(f'Movie with movie_id {movie_id} not found'), 400

@app.route('/movies/deactivate/<movie_id>', methods=['PUT'])
def deactivate_movie(movie_id):
    movie_data = db.session.query(Movies).filter(Movies.movie_id == movie_id).first()
    movie_data.active = False
    db.session.commit()
    return jsonify(f'Movie with movie_id {movie_id} deactivated'), 200

@app.route('/movies/activate/<movie_id>', methods=['PUT'])
def activate_movie(movie_id):
    movie_data = db.session.query(Movies).filter(Movies.movie_id == movie_id).first()
    movie_data.active = True
    db.session.commit()
    return jsonify(f'Movie with movie_id {movie_id} activated'), 200

@app.route('/movie/search/<search_term>')
def movies_get_by_search(search_term, internal_call=False):
    search_term = search_term.lower()

    movie_data = {}

    movie_data = db.session.query(Movies).filter(db.or_( \
        db.func.lower(Movies.movie_name).contains(search_term)))

    if internal_call:
        return movies_schema.dump(movie_data)
    return jsonify(movies_schema.dump(movie_data))

@app.route('/search/<search_term>')
def get_all_by_search(search_term):
    search_term = search_term.lower()
    
    search_results = {}
    search_results["actors"] = actors_get_by_search(search_term, True)
    search_results["directors"] = directors_get_by_search(search_term, True)
    search_results["movies"] = movies_get_by_search(search_term, True)

    return jsonify(search_results)

if __name__ == "__main__":
    create_all()
    app.run()