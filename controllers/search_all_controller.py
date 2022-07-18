from flask import jsonify

from controllers.actor_contollers import actors_get_by_search
from controllers.directors_contollers import directors_get_by_search
from controllers.movie_controllers import movies_get_by_search

def get_all_by_search(search_term):
    search_term = search_term.lower()
    
    search_results = {}
    search_results["actors"] = actors_get_by_search(search_term, True)
    search_results["directors"] = directors_get_by_search(search_term, True)
    search_results["movies"] = movies_get_by_search(search_term, True)

    return jsonify(search_results)