from flask import Blueprint
import controllers

movie = Blueprint('movie', __name__)

@movie.route('/movies/add', methods=['POST'])
def movie_add():
    return controllers.movie_add()

@movie.route('/movies/list')
def get_all_movies():
    return controllers.get_all_movies()

@movie.route('/movies/list/<movie_id>')
def get_one_movie(movie_id):
    return controllers.get_one_movie(movie_id)

@movie.route('/movies/edit/<movie_id>', methods=['PUT'])
def edit_movie(movie_id):
    return controllers.edit_movie(movie_id)

@movie.route('/movies/delete/<movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    return controllers.delete_movie(movie_id)

@movie.route('/movies/deactivate/<movie_id>', methods=['PUT'])
def deactivate_movie(movie_id):
    return controllers.deactivate_movie(movie_id)

@movie.route('/movies/activate/<movie_id>', methods=['PUT'])
def activate_movie(movie_id):
    return controllers.activate_movie(movie_id)

@movie.route('/movie/search/<search_term>')
def movies_get_by_search(search_term):
    return controllers.movies_get_by_search(search_term)