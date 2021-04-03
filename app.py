import os
from flask import Flask, jsonify, render_template, request, abort, redirect, url_for
from models import setup_db, Movie, Actor
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from auth.auth import AuthError, requires_auth

'''
Endpoints:

    GET /actors and /movies
    DELETE /actors/ and /movies/
    POST /actors and /movies and
    PATCH /actors/ and /movies/
    '''

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={"/": {"origins": "*"}})
    
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Origin', 'https://capstone100.herokuapp.com')
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response


    @app.route('/')
    def index():
        return redirect(url_for('login'))


    '''login page should route to Auth0 site and Authorize user.'''
    @app.route('/login', methods=['GET'])
    def login():
        return render_template('login.html')
    

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        '''returns a list of movies'''
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
        except Exception:
            abort(500)
        return render_template('movies.html', movies=movies_list, list_header="Movies!"), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movies(payload):
        '''creates a new row in the movies table'''
        if request.form.get('title'):
            data_t = request.form.get('title')
            data_rd = request.form.get('release_date')
            movie = Movie(title=data_t, release_date=data_rd)
        elif request.json_get():
            data = request.json_get()
            movie = Movie(title=data['title'],release_date=data['release_date'])
        else:
            abort(403)
        movie.insert()
        return jsonify({"success": True,
                        "movies": [movie.format()]}), 200


    @app.route('/movies/<edit_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movies(payload, edit_id):
        '''changes the name of the movie'''
        movie = Movie.query.get(edit_id)
        if not movie:
            abort(401)
        else:
            try:
                new_title = request.form.get('edit_title')
                new_release_date = request.form.get('edit_release_date')
                movie.release_date = new_release_date
                movie.title = new_title
                movie.update()
            except Exception:
                abort(422)
        return jsonify({"success": True, "movies": [movie.format()]}), 200


    @app.route('/movies/<movie_id>/deleted', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(payload, movie_id):
        '''deletes a movie'''
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(401)
        else:
            movie.delete()
            return jsonify({"success": True, "delete": movie_id}), 200


    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors():
        '''returns a list of actors'''
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
        except Exception:
            abort(500)
        return render_template('actors.html', actors=actors_list, list_header="Actors!"), 200


    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actors(payload):
        '''creates a new row in the actors table'''
        data_n = request.form.get('name')
        if data_n:
            actor = Actor(name=data_n, age=00, gender="")
            actor.insert()
        else:
            abort(403)
        return jsonify({"success": True,
                        "actors": [actor.format()]}), 200


    @app.route('/actors/<edit_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actors(payload, edit_id):
        '''changes the name of the actor'''
        actor = Actor.query.get(edit_id)
        if not actor:
            abort(401)
        else:
            try:
                new_name = request.form.get('edit_name')
                new_age = request.form.get('edit_age')
                actor.name = new_name
                actor.age = new_age
                actor.update()
            except Exception:
                abort(422)
        return jsonify({"success": True, "actors": [actor.format()]}), 200


    @app.route('/actors/<actor_id>/deleted', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(payload, actor_id):
        '''deletes an actor'''
        actor = Actor.query.get(actor_id)
        if not actor:
            abort(401)
        else:
            actor.delete()
            return jsonify({"success": True, "delete": actor_id}), 200


    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    # Error Handling
    '''
    Example error handling for unprocessable entity
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False,
                        "error": 422,
                        "message": "unprocessable"
                        }), 422


    '''
    implement error handlers using the @app.errorhandler(error) decorator
        each error handler should return (with approprate messages):
                 jsonify({
                        "success": False,
                        "error": 404,
                        "message": "resource not found"
                        }), 404
    '''
    @app.errorhandler(403)
    def unprocessable(error):
        return jsonify({
                        "success": False,
                        "error": 403,
                        "message": "don't have permissions"
                        }), 403


    '''
    implement error handler for 404
        error handler should conform to general task above
    '''
    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
                        "success": False,
                        "error": 404,
                        "message": "resource not found"
                        }), 404


    @app.errorhandler(401)
    def resource_not_found(error):
        return jsonify({
                        "success": False,
                        "error": 401,
                        "message": "Unauthorized"
                        }), 401


    '''
    implement error handler for AuthError
        error handler should conform to general task above
    '''
    @app.errorhandler(AuthError)
    def auth_error(ex):
        res = jsonify(ex.error)
        res.status_code = ex.status_code
        return res

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
