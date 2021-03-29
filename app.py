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
    #CORS(app)
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


    @app.route('/render_page', methods=['GET', 'POST'])
    def render_page():
        data = request.data()
        print("---------------------------------->DATA", data)
        jwt = data['jwt']
        os.environ['JWT'] = jwt 
        return redirect(url_for('get_movies'))
    

    @app.route('/set_jwt', methods=['GET', 'POST'])
    def set_jwt():
        if request.form.get('jwt') == None:
            return render_template('set_jwt.html')
        else:
            data = request.form.get('jwt')
            print("---------------------------------->DATA", data)
            jwt = data['jwt']
            os.environ['JWT'] = jwt
            return redirect(url_for('get_movies'))

    '''@app.route('/set_jwt', methods=['POST'])
    def setjwt():
        data = request.form.get('jwt')
        print("---------------------------------->DATA", data)
        jwt = data['jwt']
        os.environ['JWT'] = jwt
        return redirect(url_for('get_movies'))'''


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
    # @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth('post:movies')
    def add_movies(payload):
        '''creates a new row in the movies table'''
        '''if not requires_auth(permission='post:movies'):
            raise AuthError({
                'code': 'invalid_permission',
                'description': 'Do not have permission to add movies.'
            }, 403)
        else:
        '''
        data_t = request.form.get('title')
        print('---------->', data_t)
        data_rd = request.form.get('release_date')
        
        #data = request.get_json()
        print("---------->", data_rd)
        if data_t:
            movie = Movie(title=data_t, release_date=data_rd)
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
                actors_list.append(actors[count].format())
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
    def auth_error(ex):
        res = jsonify(ex.error)
        res.status_code = ex.status_code
        return res

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
