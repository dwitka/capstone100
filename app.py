import os
from flask import Flask, jsonify, render_template
from models import setup_db
from flask_cors import CORS

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


    
    @app.route('/login', methods=['GET'])
    '''login page should route to Auth0 site and Authorize user.'''
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

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
