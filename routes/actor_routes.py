from flask import Blueprint
import controllers

actor = Blueprint('actor', __name__)

@actor.route('/actors/add', methods=['POST'])
def add_actor():
    return controllers.add_actor()

@actor.route('/actors/list')
def get_all_actors():
    return controllers.get_all_actors()

@actor.route('/actors/list/<actor_id>')
def get_one_actor(actor_id):
    return controllers.get_one_actor(actor_id)

@actor.route('/actors/edit/<actor_id>', methods=['PUT'])
def edit_actor(actor_id):
    return controllers.edit_actor(actor_id)

@actor.route('/actors/delete/<actor_id>', methods=['DELETE'])
def delete_actor(actor_id):
    return controllers.delete_actor(actor_id)

@actor.route('/actors/deactivate/<actor_id>', methods=['PUT'])
def deactivate_actor(actor_id):
    return controllers.deactivate_actor(actor_id)

@actor.route('/actors/activate/<actor_id>', methods=['PUT'])
def activate_actor(actor_id):
    return controllers.activate_actor(actor_id)

@actor.route('/actor/search/<search_term>')
def actors_get_by_search(search_term):
    return controllers.actors_get_by_search(search_term)