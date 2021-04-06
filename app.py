from flask import Flask, render_template, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import db_drop_and_create_all, setup_db, Movie, Actor


def create_app(test_config=None):
    '''create and configure the app'''
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={"/": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, PUT, POST,DELETE, OPTIONS')
        return response

    # db_drop_and_create_all()

    # Home
    @app.route('/')
    def login():
        return render_template('login.html')

    # Movie endpoints
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        '''Retrieves movies from database.'''
        try:
            movies = Movie.query.all()
            movies_list = []
            count = 0
            if len(movies) != 0:
                while count < len(movies):
                    movies_list.append(movies[count].format())
                    count = count + 1
            else:
                pass
            return jsonify({
                'success': True,
                'movies': movies_list
                }), 200
        except Exception:
            abort(500)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
        '''Adds a movie to the database.'''
        data = request.get_json()
        if data:
            movie = Movie(
                title=data['title'],
                release_date=data['release_date']
                )
            try:
                movie.insert()
                return jsonify({
                    'success': True,
                    'movie': movie.format()
                    }), 200
            except Exception:
                abort(500)
        else:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['GET', 'PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        '''Edits a movie from the database.'''
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        data = request.get_json()
        if movie:
            movie.title = data['title']
            movie.release_date = data['release_date']
        else:
            abort(404)
        try:
            movie.update()
            return jsonify({
                'success': True,
                'movie': [movie.format()]
                }), 200
        except Exception:
            abort(500)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        '''Deletes a movie from the database.'''
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie:
            try:
                movie.delete()
                return jsonify({
                    'success': True,
                    'delete': movie_id
                    }), 200
            except Exception:
                db.session.rollback()
                abort(500)
        else:
            abort(404)

    # Actor endpoints
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        '''Retrieves a list of all actors from the database.'''
        try:
            actors = Actor.query.all()
            actors_list = []
            count = 0
            if len(actors) != 0:
                while count < len(actors):
                    actors_list.append(actors[count].format())
                    count = count + 1
            else:
                pass
            return jsonify({
                            'success': True,
                            'actors': actors_list
                            }), 200
        except Exception:
            abort(500)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(payload):
        '''Adds an actor to the database.'''
        data = request.get_json()
        if data:
            actor = Actor(
                name=data['name'],
                age=data['age'],
                gender=data['gender'],
                movie_id=data['movie_id']
                )
        else:
            abort(422)
        try:
            actor.insert()

            return jsonify({
                'success': True,
                'actor': actor.format()
                }), 200
        except Exception:
            abort(500)

    @app.route('/actors/<int:actor_id>', methods=['GET', 'PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        '''Edits an actor from the database.'''
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        data = request.get_json()
        if actor:
            actor.name = (data['name'] if data['name']
                          else Actor.name)
            actor.age = (data['age'] if data['age']
                         else actor.age)
            actor.gender = (data['gender'] if data['gender']
                            else actor.gender)
            actor.movie_id = (data['movie_id'] if data['movie_id']
                              else actor.movie_id)
        else:
            abort(404)
        try:
            actor.update()
            return jsonify({
                'success': True,
                'actor': [actor.format()]
                }), 200
        except Exception:
            abort(500)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        '''Deletes an actor from the database.'''
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor:
            try:
                actor.delete()
                return jsonify({
                    'success': True,
                    'delete': actor_id
                    }), 200
            except Exception:
                db.session.rollback()
                abort(500)
        else:
            abort(404)

    # Error Handling
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request."
            }), 400

    @app.errorhandler(401)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
            }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found."
            }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Sorry, but there is a server error."
            }), 500

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
            }), 422

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Sorry, you dont have permissions.",
                }), 403

    @app.errorhandler(AuthError)
    def auth_error(ex):
        res = jsonify(ex.error)
        res.status_code = ex.status_code
        return res

    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
