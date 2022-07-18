from flask import request, jsonify
from db import db, query

from models.directors_model import Directors, director_schema, directors_schema

def add_director():
    form = request.form

    director_first_name = form.get('director_first_name')
    director_last_name = form.get('director_last_name')

    new_director = Directors(director_first_name, director_last_name)

    db.session.add(new_director)
    db.session.commit()

    return jsonify(director_schema.dump(new_director)), 200

def get_all_directors():
    director_records = query(Directors).all()

    return jsonify(directors_schema.dump(director_records)), 200

def get_one_director(director_id):
    director_record = query(Directors).filter(Directors.director_id == director_id).first()

    return jsonify(director_schema.dump(director_record)), 200

def edit_director(director_id):
    form = request.form

    director_data = query(Directors).filter(Directors.director_id == director_id).first()
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

        return jsonify(director_schema.dump(director_data)), 200

def delete_director(director_id):
    director_data = query(Directors).filter(Directors.director_id == director_id).first()
    if director_data:
        db.session.delete(director_data)
        db.session.commit()
        return jsonify(f'Director with director_id {director_id} deleted'), 200
    
    return jsonify(f'Director with director_id {director_id} not found'), 404

def deactivate_director(director_id):
    director_data = query(Directors).filter(Directors.director_id == director_id).first()
    if director_data == None:
        return jsonify(f'Director with director_id {director_id} not found!')
    director_data.active = False
    db.session.commit()
    return jsonify(f'Director with director_id {director_id} deactiviated'), 200

def activate_director(director_id):
    director_data = query(Directors).filter(Directors.director_id == director_id).first()
    if director_data == None:
        return jsonify(f'Director with director_id {director_id} not found!')
    director_data.active = True
    db.session.commit()
    return jsonify(f'Director with director_id {director_id} activiated'), 200

def directors_get_by_search(search_term, internal_call=False):
    search_term = search_term.lower()

    director_data = {}

    director_data = query(Directors).filter(db.or_( \
        db.func.lower(Directors.director_first_name).contains(search_term), \
        db.func.lower(Directors.director_last_name).contains(search_term)))
    if internal_call:
        return directors_schema.dump(director_data)
    return jsonify(directors_schema.dump(director_data))