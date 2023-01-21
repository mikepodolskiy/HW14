# import required libraries, functions, blueprints
from flask import Flask
from views import movie_blueprint, year_to_year_blueprint, \
    rating_blueprint, genre_blueprint


# starting app
app = Flask(__name__)
# allow сyrillic symbols, setting configuration parameter for encoding
app.config['JSON_AS_ASCII'] = False

# registering blueprints
app.register_blueprint(movie_blueprint)
app.register_blueprint(year_to_year_blueprint)
app.register_blueprint(rating_blueprint)
app.register_blueprint(genre_blueprint)

# setting condition for app launch
if __name__ == '__main__':
    app.run()
