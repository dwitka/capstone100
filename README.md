-Project includes an informative README
        ? Project dependencies, local development and hosting
        instructions,
        ? Detailed instructions for scripts to install any
        project dependencies, and to run the development server.
        ? Documentation of API behavior and RBAC controls

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

	2. renew jwts
		-copy and paste this URL inside the Url bar, hit ENTER 
		https://capstone100.us.auth0.com/authorize?audience=Cap100&response_type=token&client_id=6yRMwnrOJGPCvl3jnkGzW25LopesQaPa&redirect_uri=https://capstone100.herokuapp.com/movies

		-login with any of these three emails:	john@assistant.com 	bob@director.com	david@executive.com
				with password:

		-retrieve jwt from URL after successful login

		-paste the jwt into setup.sh into appropriate spot.
	
	3. run setup.sh
		This sets up the environment variables, including the three jwts you just inserted.
		$ source setup.sh

	4. data dump
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

	5. run tests:
		$ python -m unittest test_app.py




CHECKING ENDPOINTS LIVE:

-Instructions are provided in README for setting up
authentication so reviewers can test endpoints at live
application endpoint




FILE SYSTEM:
	capstone100 (root directory)
		|
		--app.py 
		|  (this is your API)
		|
		--test_app.py 
		|  (This file includes all your unittests)
		|
		--setup.sh 
		|  (Loads the environment variables)
		|
		--movies.psql 
		|  (Loads the database) 
		|
		--migrations/ 
		|  (chronicles the data model versions)
		|
		--auth.py
		|  (verifies authorization and permissions)
		|
		--requirements.txt
		|  (houses all your dependencies)
		|
		--README.md 
		|  (instructions/details on running app)
		|
		--models.py
		|
		--manage.py
		|
		--Procfile 
		|  (this tells heroku to use the Gunicorn server)
		|
		--templates/login.html 
		   (this page takes the user to Auth0 for authentication)
