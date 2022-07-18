from flask import Flask
from flask_marshmallow import Marshmallow
from db import db, query, init_db

from models.actors_model import Actors
from models.directors_model import Directors
from models.movies_model import Movies

import routes

app = Flask(__name__)

database_host = "127.0.01:5432"
database_name = "movies"
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{database_host}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app, db)
ma = Marshmallow(app)

def create_all():
    with app.app_context():
        db.create_all()

        print("Querying for Movie...")
        movie_data = query(Movies).filter(Movies.movie_name == "Top Gun").first()
        if movie_data == None:
            print("Movie not found! Creating Top Gun...")
            actor_data = query(Actors).filter(Actors.actor_first_name == "Tom").first()
            director_data = query(Directors).filter(Directors.director_first_name == "Tony").first()
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

app.register_blueprint(routes.actor)
app.register_blueprint(routes.director)
app.register_blueprint(routes.movie)
app.register_blueprint(routes.search)

if __name__ == "__main__":
    create_all()
    app.run()