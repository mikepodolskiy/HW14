# import required libraries and modules
import sqlite3
import json


# defining class for creating methods to use in views
class Netflix:

    def get_sql_all(self, query):
        connection = sqlite3.connect('./netflix.db')
        cursor = connection.cursor()
        cursor.execute(query)
        responses = cursor.fetchall()
        return responses

    def get_sql_one(self, query):
        connection = sqlite3.connect('./netflix.db')
        cursor = connection.cursor()
        cursor.execute(query)
        response = cursor.fetchone()
        return response

    def get_by_title(self, required_title: str):
        """method of searching in db by title - SQL request getting
        item with required title, with order by date and
        limit 1 to get one latest item then put relative data
        into dict, and dump it to json"""
        query = ("SELECT title, country, release_year, listed_in, description "
                 "FROM netflix "
                 f"WHERE title='{required_title}' "
                 "ORDER BY release_year desc "
                 "LIMIT 1")

        response = self.get_sql_one(query)
        show_data = {"title": response[0],
                     "country": response[1],
                     "release_year": response[2],
                     "listed_in": response[3],
                     "description": response[4].strip('\n')}
        return json.dumps(show_data)

    def get_by_years_range(self, first_year: int, second_year: int):
        """
        method requesting movies between two years
        :param first_year: first limit for search
        :param second_year: second limit for search
        :return: list of dicts with movies data - title - release year
        """
        query = ("SELECT title, release_year "
                 "FROM netflix "
                 "WHERE type='Movie' "
                 f"AND  release_year BETWEEN {first_year} AND {second_year} "
                 "ORDER BY release_year "
                 "LIMIT 100")
        responses = self.get_sql_all(query)
        data = []
        for response in responses:
            movie_data = {"title": response[0], "release_year": response[1]}
            data.append(movie_data)
        return data

    def get_by_rating(self, rating: str):
        """
        method transforming string rating request into set of ratings (as in db)
        searching in db by rating - SQL request getting
        items with required rating, then put relative data
        into list of dicts, and dump it to json
        :param rating: required audience
        :return: list of dicts with movie/show title, rating and description
        """

        if rating == 'children':
            request_rating = ('G', 'TV-Y', 'TV-G')
        elif rating == 'family':
            request_rating = ('PG', 'TV-PG', 'TV-Y7', 'PG-13', 'TV-14')
        else:
            request_rating = ('R', 'NC-17', 'TV-MA', 'NR')

        query = ("SELECT title, rating, description "
                 "FROM netflix "
                 f"WHERE rating in {request_rating} ")
        responses = self.get_sql_all(query)
        data = []
        for response in responses:
            movie_data = {"title": response[0],
                          "rating": response[1],
                          "description": response[2].strip('\n')}
            data.append(movie_data)
        return data

    def get_by_genre(self, required_genre: str):
        """method of searching in db by genre - SQL request getting
        items with required genre, with order by date (desc) and
        limit 10 to get ten latest items, then put relative data
        into dict, and dump it to json"""
        query = ("SELECT title,  description "
                 "FROM netflix "
                 f"WHERE listed_in LIKE '%{required_genre}%' "
                 "ORDER BY release_year desc "
                 "LIMIT 10")

        responses = self.get_sql_all(query)
        data = []
        for response in responses:
            show_data = {"title": response[0],
                         "description": response[1].strip('\n')}
            data.append(show_data)
        return json.dumps(data)


# defining required functions
def get_by_type_release_genre(required_type: str, required_release: int, required_genre: str):
    """function searching in db by type,release year and genre
        SQL request getting items with required args, and put relative data
        into list of dicts, and dump it to json"""
    query = ("SELECT title,  description "
             "FROM netflix "
             f"WHERE listed_in LIKE '%{required_genre}%' "
             f"AND type = '{required_type}' "
             f"AND `release_year`= '{required_release}' ")

    movie = Netflix()
    responses = movie.get_sql_all(query)
    data = []
    for response in responses:
        show_data = {"title": response[0],
                     "description": response[1].strip('\n')}
        data.append(show_data)
    return json.dumps(data)


def get_co_cast_by_names(name_1: str, name_2: str):
    """
    function searching in db by names
        SQL request getting items with required args,
        first cycle transforms response to list of strings
        second cycle making list of names of co-cast out of previous
        third cycle making list of names which complies condition
    :param name_1: first actor/actress name
    :param name_2: second actor/actress name
    :return: list of co-cast with more than 2 joint movies
    """
    query = ("SELECT `cast` "
             "FROM netflix "
             f"WHERE netflix.'cast' LIKE '%{name_1}%' "
             f"AND netflix.'cast' LIKE '%{name_2}%' ")

    movie = Netflix()
    responses = movie.get_sql_all(query)
    # first cycle
    full_co_actors_list_strings = []
    for response in responses:
        for item in response:
            full_co_actors_list_strings.append(item)

    # second cycle
    full_co_actors_list = []
    for resp in full_co_actors_list_strings:
        for item in resp.split(', '):
            full_co_actors_list.append(item)
    full_co_actors_list.remove(name_1),
    full_co_actors_list.remove(name_2)

    # third cycle
    required_actors = []
    for actor in full_co_actors_list:
        if full_co_actors_list.count(actor) > 2:
            required_actors.append(actor)
            required_actors = list(set(required_actors))

    return required_actors


query = Netflix()

# print(query.get_by_title('Zodiac'))

# print(query.get_by_years_range(2010, 2015))

# print(query.get_by_rating('adult'))
# print(query.get_by_genre('dramas'))
# print(get_by_type_release_genre('Movie', 2005, 'dramas'))
print(get_co_cast_by_names('Jack Black', 'Dustin Hoffman'))
