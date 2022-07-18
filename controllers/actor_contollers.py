from flask import request, jsonify
from db import db, query

from models.actors_model import Actors, actor_schema, actors_schema

def add_actor():
    form = request.form

    actor_first_name = form.get('actor_first_name')
    actor_last_name = form.get('actor_last_name')
    new_actor = Actors(actor_first_name, actor_last_name)

    db.session.add(new_actor)
    db.session.commit()

    return jsonify(actor_schema.dump(new_actor))

def get_all_actors():
    actor_records = query(Actors).all()

    return jsonify(actors_schema.dump(actor_records)), 200

def get_one_actor(actor_id):
    actor_record = query(Actors).filter(Actors.actor_id == actor_id).first()

    return jsonify(actor_schema.dump(actor_record)), 200

def edit_actor(actor_id):
    form = request.form

    actor_data = query(Actors).filter(Actors.actor_id == actor_id).first()
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

        return jsonify(actor_schema.dump(actor_data)), 200

def delete_actor(actor_id):
    actor_data = query(Actors).filter(Actors.actor_id == actor_id).first()
    if actor_data:
        db.session.delete(actor_data)
        db.session.commit()
        return jsonify(f'Actor with actor_id {actor_id} deleted'), 200
    
    return jsonify(f'Actor with actor_id {actor_id} not found!'), 404

def deactivate_actor(actor_id):
    actor_data = query(Actors).filter(Actors.actor_id == actor_id).first()
    if actor_data == None:
        return jsonify(f'Actor with actor_id {actor_id} not found!')
    actor_data.active = False
    db.session.commit()
    return jsonify(f'Actor with actor_id {actor_id} deactivated'), 200

def activate_actor(actor_id):
    actor_data = query(Actors).filter(Actors.actor_id == actor_id).first()
    if actor_data == None:
        return jsonify(f'Actor with actor_id {actor_id} not found!')
    actor_data.active = True
    db.session.commit()
    return jsonify(f'Actor with actor_id {actor_id} activated'), 200

def actors_get_by_search(search_term, internal_call=False):
    search_term = search_term.lower()

    actor_data = {}

    actor_data = query(Actors).filter(db.or_( \
        db.func.lower(Actors.actor_first_name).contains(search_term), \
        db.func.lower(Actors.actor_last_name).contains(search_term)))

    if internal_call:
        return actors_schema.dump(actor_data)
    return jsonify(actors_schema.dump(actor_data))