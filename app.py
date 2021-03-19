import os
from flask import Flask, jsonify, render_template
from models import setup_db
from flask_cors import CORS

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
    CORS(app)


    '''login page should route to Auth0 site and Authorize user.'''
    @app.route('/login', methods=['GET'])
    def login():
        return render_template('login.html')

    
    @app.route('/movies', methods=['GET'])
    def get_movies():
        '''returns a list of movies'''
        movies = Movie.query.all()
        movies_list = []
        count = 0
        if len(movies) != 0:
            while count < len(movies):
                movies_list.append(movies[count])
                count = count + 1
        else:
            pass
        return jsonify({"success": True, "movies": movies_list}), 200


    @app.route('/movies', methods=['POST'])
    def add_movies():
        '''creates a new row in the movies table'''
        if not requires_auth(permission='post:movies'):
            raise AuthError({
                'code': 'invalid_permission',
                'description': 'Do not have permission to add movies.'
            }, 403)
        else:
            data = request.get_json()
        if data:
            movie = Movie(title=data['title'])
            movie.insert()
        else:
            abort(401)
        return jsonify({"success": True,
                        "movies": [movie.format()]}), 200


    @app.route('/movies/<id>', methods=['PATCH'])
    def edit_title(id):
        '''changes the name of the movie'''
        if not requires_auth(permission='patch:movies'):
            raise AuthError({
                'code': 'invalid_permission',
                'description': 'Do not have permission to edit.'
            }, 403)
        movie = Movie.query.filter_by(id=id).one_or_none()
        if not movie:
            abort(401)
        else:
            try:
                data = request.get_json()
                new_title = data['title']
                movie.title = new_title
                movie.update()
            except Exception:
                abort(422)
        return jsonify({"success": True, "movies": [movie.format()]}), 200


    @app.route('/movies/<id>', methods=['DELETE'])
    def delete_movies(id):
        '''deletes a movie'''
        if not requires_auth(permission='delete:movies'):
            raise AuthError({
                'code': 'invalid_permission',
                'description': 'permission to delete not granted.'
            }, 403)
        movie = Movie.query.filter_by(id=id).one_or_none()
        if not movie:
            abort(401)
        else:
            movie.delete()
            return jsonify({"success": True, "delete": id}), 200


    @app.route('/actors', methods=['GET'])
    def get_actors():
        '''returns a list of actors'''
        actors = Actor.query.all()
        actors_list = []
        count = 0
        if len(actors) != 0:
            while count < len(actors):
                actors_list.append(actors[count])
                count = count + 1
        else:
            pass
        return jsonify({"success": True, "actors": actors_list}), 200



    @app.route('/')
    def get_greeting():
        # excited = os.environ['EXCITED']
        # greeting = "Hello" 
        # if excited == 'true': greeting = greeting + "!!!!!"
        return jsonify({"success": True})

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
    def autherror(error):
        return jsonify({
                        "success": False,
                        "error": AuthError,
                        "message": "AuthError"
                        }), AuthError

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
