from flask import Blueprint
import controllers

director = Blueprint('director', __name__)

@director.route('/directors/add', methods=['POST'])
def add_director():
    return controllers.add_director()

@director.route('/directors/list')
def get_all_directorrs():
    return controllers.get_all_directors()

@director.route('/directors/list/<director_id>')
def get_one_director(director_id):
    return controllers.get_one_director(director_id)

@director.route('/directors/edit/<director_id>', methods=['PUT'])
def edit_director(director_id):
    return controllers.edit_director(director_id)

@director.route('/directors/delete/<director_id>', methods=['DELETE'])
def delete_director(director_id):
    return controllers.delete_director(director_id)

@director.route('/directors/deactivate/<director_id>', methods=['PUT'])
def deactivate_director(director_id):
    return controllers.deactivate_director(director_id)

@director.route('/directors/activate/<director_id>', methods=['PUT'])
def activate_director(director_id):
    return controllers.activate_director(director_id)

@director.route('/director/search/<search_term>')
def directors_get_by_search(search_term):
    return controllers.directors_get_by_search(search_term)