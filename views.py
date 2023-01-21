# import required libraries and modules
import json
from flask import Blueprint, render_template
from utils import Netflix

# creating blueprint for film info, setting template folder
movie_blueprint = Blueprint('movie_blueprint', __name__, template_folder='templates')
year_to_year_blueprint = Blueprint('year_to_year_blueprint', __name__)
rating_blueprint = Blueprint('rating_blueprint', __name__)
genre_blueprint = Blueprint('genre_blueprint', __name__)


@movie_blueprint.route('/movie/<title>')
def movie_by_title(title):
    """
    getting movie by required tittle using method get_by_title()
    :return: view of required format movie page, variables to be used in html
    """
    movie = Netflix()
    movie_info = movie.get_by_title(title)
    movie_dic = json.loads(movie_info)
    title = movie_dic["title"]
    country = movie_dic["country"]
    release_year = movie_dic["release_year"]
    listed_in = movie_dic["listed_in"]
    description = movie_dic["description"]
    return render_template('movie_info.html', title=title, country=country, release_year=release_year,
                           listed_in=listed_in, description=description)


@year_to_year_blueprint.route('/movie/<year_from>/to/<year_to>')
def movie_by_year_range(year_from, year_to):
    """
    getting movies in years range from <year_from> - <year_to>
    using method get_by_years_range()
    :return: list of dicts with movies
    """
    movie = Netflix()
    movies_year_to_year = movie.get_by_years_range(year_from, year_to)
    return movies_year_to_year


@rating_blueprint.route('/movie/rating/<rating>')
def movies_by_age_rating(rating):
    """
    getting required audience from request,
    getting movies for required auidence, using get_by_rating_method
    :param rating: required audience - children / family / adult
    :return: list of dicts with movies data as required
    """
    movie = Netflix()
    movies_by_rate = movie.get_by_rating(rating)
    return movies_by_rate


@genre_blueprint.route('/movie/genre/<genre>')
def movies_by_genre(genre):
    """
    getting required genre from request,
    getting movies for required genre, using get_by_rating_method
    :param genre: required genre
    :return: list of dicts with movies data as required
    """
    movie = Netflix()
    movies_by_genre_list = movie.get_by_genre(genre)
    return movies_by_genre_list
