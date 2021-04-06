
INTRO:
	This API is written as the final project in the Full 
	Stack Web Developer course offered by Udacity.


DEPENDENCIES:
	Can be found in the requirements.txt file.


LOCAL DEVELOPMENT:
	API designed on Windows 7 using Git-Bash. This means
	that some of the commands listed below may need to be
	slightly altered if you're using a different OS or a 
	different CLI. For example: 
	
	on Git-Bash its 	
		export FLASK_APP=app.py
	
	on CMD its
		set FLASK_APP=app.py


ROLES AND PERMISSIONS:
	Roles and permissions for this API are below. As defined
	on Auth0 website.

	Casting Assistant
		permissions: 	get:movies
				get:actors

	Casting Director
		permissions: 	get:movies, patch:movies
				get:actors, patch:actors, post:actors, delete:actors

	Executive Producer
		permissions:	get:movies, patch:movies, post:movies, delete:movies
                                get:actors, patch:actors, post:actors, delete:actors



URL:
	https://capstone100.us.herokuapp.com



RUNNING TESTS LOCALLY:


	1. run the environment
		$ source env/Scripts/activate
			OR
		$ source env/bin/activate

	2. install dependencies
		$ pip install -r requirements.txt

	3. renew jwts
		-copy and paste this URL inside the Url bar, hit ENTER 
		https://capstone100.us.auth0.com/authorize?audience=Cap100&response_type=token&client_id=6yRMwnrOJGPCvl3jnkGzW25LopesQaPa&redirect_uri=https://capstone100.herokuapp.com/movies

		-login to all of these emails:	
				john@assistant.com 	bob@director.com	david@executive.com
		
		password same for all: Capstone100 

		-retrieve jwt from URL after successful login

		-paste the jwt into setup.sh into appropriate spot.

		-delete history and cookies.

		-do this for all three users.
	
	4. run setup.sh
		This sets up the environment variables, including the three jwts you just inserted.
		$ source setup.sh

	5. data dump
		LOG INTO POSTGRES
		$ psql database username
			OR
		$ psql -h localhost -U username -p5432

		RESET DATABASE
		# drop database my_database;
		# create database my_database;
		# \q (logout of postgres)

		LOAD PSQL FILE INTO DATABASE
		$ psql -h localhost -d my_database -U username -f movies.psql

	6. run tests:
		$ python -m unittest test_app.py


RUN THE DEVELOPMENT SERVER:

	$ export FLASK_APP=app.py
	$ export FLASK_ENV=development
	$ flask run


ENDPOINTS:

	GET /movies
		Retrieves list of movies.
	
	POST /movies
		Allows you to create and add a new movie to the database.
		Example Body: {
						    "title": "Terminator",
						    "release_date": "1984"
						}
	
	PATCH /movies/<int:movie_id>
		This endpoint lets you make changes movie variables such as title and release_date.
		Example Body: {
					        "title": "Terminator 2",
					        "release_date": "1990"
					    }
	
	DELETE /movie/<int:movie_id>/delete
		Deletes a movie from the database.


	GET /actors
                Retrieves a list of actors.

        POST /actors
                Allows you to create and add a new actor to the database. 
                Example Body: {
                                                    "name": "Keanu Reeves",
                                                    "age": 35,
                                                    "gender": "M",
						    "movie_id": 5
                                                }
        
	PATCH /actor/<int:actor_id>
                Make edits to actor variables.
                Example Body: {
                                                "name": "Kim Bassinger",
                                                "age": "37",
                                                "gender": "F",
						"movie_id": 5
                                            }

        DELETE /actor/<int:actor_id>/delete
                Deletes an actor from the database.


FILE SYSTEM:
	capstone100 (root directory)
		
		app.py 
		  (this is your API)
		
		test_app.py 
		  (This file includes all your unittests)
		
		setup.sh 
		  (Loads the environment variables)
		
		movies.psql 
		  (Loads the database) 
		
		migrations/ 
		  (chronicles the data model versions)
		
		auth.py
		  (verifies authorization and permissions)
		
		requirements.txt
		  (houses all your dependencies)
		
		README.md 
		  (instructions/details on running app)
		
		models.py
		
		manage.py
		
		Procfile 
		  (this tells heroku to use the Gunicorn server)
		
		templates/login.html 
		   (this page takes the user to Auth0 for authentication)
