import os
from flask import Flask, jsonify
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

    @app.route('/movies', methods=['GET', 'POST', 'DELETE', 'PATCH'])
    def movies():
        text = "Here we go again!!! Another awesome endpoint!!!!"
        return text

    @app.route('/actors', methods=['GET', 'POST', 'DELETE', 'PATCH'])
    def actors():
        text = "This is your actors page!!! Yeahhhh!!!!!"
        return text

    @app.route('/')
    def get_greeting():
        # excited = os.environ['EXCITED']
        # greeting = "Hello" 
        # if excited == 'true': greeting = greeting + "!!!!!"
        return jsonify({"success":true})

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
