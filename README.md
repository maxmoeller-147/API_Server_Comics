# API_Server_Comics
Comics Store API  Description: This API for a comic book store lets you manage comics, customers, and orders. 


## Setup

Follow this steps to ensure the successfully operation of the server:

- create a .env file with the variables included in .env
	- DATABASE_URI with a connection string to your chosen database, e.g. postgres

- ensure that a local database exists by making one in the postgres shell
	- enter the postgres shell
		- MacOS: run the `psql` command
		- Linux & WSL: run the `sudo -u postgres psql` command 
	- list all existing databases by running `\l`
	- if the database you want to use does not currently exist, create it by running `CREATE DATABASE lms_db;`
	- check that it exists by running `\l` again
	- connect to the database you want to use with `\c lms_db`
- ensure that a postgres shell user that has permissions to work with your database 
	- in the postgres shell, run `CREATE USER lms_dev WITH PASSWORD '123456';`
	- grant the user the permissions needed to work with the database, run `GRANT ALL PRIVILEGES ON DATABASE lms_db TO lms_dev;`
	- grant db schema permissions to the user as well, run `GRANT ALL ON SCHEMA public TO lms_dev;`
- exit the postgres shell with `\q`


- create a .flaskenv file and define: FLASK_APP=main 

- make a venv!
	- run `python3 -m venv .venv` to make the venv
	- activate the venv with:
		- MacOS & Linux & WSL: `source .venv/bin/activate`
		- Windows: `.venv/Scripts/activate`
	- set the VSCode Python interpreter to the venv Python binary
		- CTRL + Shift + P to open up the command palette 
		- choose the interpreter with the path that matches the ".venv" path

- install dependencies from the project within the activated venv
	- run `pip install -r ./requirements.txt`

- ensure that the flask app database exists and has any seed data that it's meant to have
	- check the source code for any CLI commands, e.g. `./controllers/cli_controller.py`
	- run the commands needed to drop tables, create tables, and then seed those created tables

- flask run to run the server

- OPTIONAL: set flask debug and a manual PORT value into `.flaskenv`:
	- `FLASK_DEBUG=1`
	- `FLASK_RUN_PORT=8080`





REFERENCES: 
    PostgresSQL: Documentation [postgresql.org/docs/current/errcodes-appendix.html]

    (Help me with the validations)
    Docs.Python: [https://docs.python.org/3/library/re.html]

    Marshmallow: [https://marshmallow.readthedocs.io/en/stable/marshmallow.validate.html]

    w3schools: https://www.w3schools.com/python/ref_func_len.asp