from flask import Blueprint
import controllers

search = Blueprint('search', __name__)

@search.route('/search/<search_term>')
def get_all_by_search(search_term):
    return controllers.get_all_by_search(search_term)