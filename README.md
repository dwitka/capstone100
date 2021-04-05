-Project includes at least two different roles that have 
distinct permissions for actions. These roles and permissions 
are clearly defined in the project README. Students can 
reference the Casting Agency Specs in the Specifications 
section of this rubric as an example.

-URL is provided in project README 

-Instructions are provided in README for setting up 
authentication so reviewers can test endpoints at live 
application endpoint

-Project includes an informative README
        ? Motivation for project 
        ? Project dependencies, local development and hosting 
	instructions, 
        ? Detailed instructions for scripts to install any 
	project dependencies, and to run the development server. 
        ? Documentation of API behavior and RBAC controls



----------RUNNING TESTS FOR CAPSTONE100-----------------


1. run the environment
	$ source env/Scripts/activate

2. renew jwts
	INSIDE THE URL BAR(do this 3 times logging in for each role)
	https://capstone100.us.auth0.com/authorize?audience=Cap100&response_type=token&client_id=6yRMwnrOJGPCvl3jnkGzW25LopesQaPa&redirect_uri=https://capstone100.herokuapp.com/movies

3. run setup.sh
	SETUP ENVVIRONMENT VARIABLES
	$ source setup.sh

4. data dump
	LOG INTO POSTGRES
	$ psql postgres postgres

	RESET DATABASE
	# drop database hollywood;
	# create database hollywood;
	# \q (logout of postgres)

	LOAD PSQL FILE INTO DATABASE
	$ psql -h localhost -d hollywood -U postgres -f hollywood.psql

5. run tests:
	$ python -m unittest test_app.py
