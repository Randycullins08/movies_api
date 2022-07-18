from flask import request, jsonify
from db import db, query

from models.movies_model import Movies, movie_schema, movies_schema

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

    return jsonify(movie_schema.dump(new_movie)), 200

def get_all_movies():
    movie_data = query(Movies).all()

    return jsonify(movies_schema.dump(movie_data)), 200

def get_one_movie(movie_id):
    movie_record = query(Movies).filter(Movies.movie_id == movie_id).first()

    return jsonify(movie_schema.dump(movie_record)), 200

def edit_movie(movie_id):
    form = request.form

    movie_data = query(Movies).filter(Movies.movie_id == movie_id).first()
    movie_name = form.get('movie_name')

    if movie_data == None:
        return jsonify("ERROR: movie_id missing!"), 400
    if movie_data:
        movie_data.movie_id = movie_id
        if movie_name:
            movie_data.movie_name = movie_name

        db.session.commit()

        return jsonify(movie_schema.dump(movie_data)), 200

def delete_movie(movie_id):
    movie_data = query(Movies).filter(Movies.movie_id == movie_id).first()

    if movie_data:
        db.session.delete(movie_data)
        db.session.commit()
        return jsonify(f'Movie with movie_id {movie_id} deleted')

    return jsonify(f'Movie with movie_id {movie_id} not found'), 400

def deactivate_movie(movie_id):
    movie_data = query(Movies).filter(Movies.movie_id == movie_id).first()
    if movie_data == None:
        return jsonify(f'Movie with movie_id {movie_id} not found!')
    movie_data.active = False
    db.session.commit()
    return jsonify(f'Movie with movie_id {movie_id} deactivated'), 200

def activate_movie(movie_id):
    movie_data = query(Movies).filter(Movies.movie_id == movie_id).first()
    if movie_data == None:
        return jsonify(f'Movie with movie_id {movie_id} not found!')
    movie_data.active = True
    db.session.commit()
    return jsonify(f'Movie with movie_id {movie_id} activated'), 200

def movies_get_by_search(search_term, internal_call=False):
    search_term = search_term.lower()

    movie_data = {}

    movie_data = query(Movies).filter(db.or_( \
        db.func.lower(Movies.movie_name).contains(search_term)))

    if internal_call:
        return movies_schema.dump(movie_data)
    return jsonify(movies_schema.dump(movie_data)), 200