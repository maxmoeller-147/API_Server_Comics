# API_Server_Comics
Comics Store API  Description: This API for a comic book store lets you manage comics, customers, and orders. 



## WHY I CHOSE POSTGRESQL?

* For this project, I decided to use PostgreSQL as my database system. It's a realiable relational database that organizes data into tables with clear connections. It's not only the one system that I can manage easier but it is also perfect for a comic store to manage all the costumer, orders, comics and puyblishers and collect information of the comics. 
Compared to the others options, Postgresql seems to be the best in terms of strict data integrity and its ability to handle complex queries.
While MySQL is also relational and widely used, PostgreSQL offers more advanced features and stricter rules, making it a better choice for applications that need precision. SQLite is a lightweight and easy for small apps, but it's not great for multi-user environments or production level systems. On the other hand, NoSQL databases like MongoDB are great for unstructured or highly flexible data, but the don't enforce relationships as strongly as relational systems, which is crucial for our use case. In summary, PostgreSQL strikes the right balance between stabilty, scalability and relational integrity, making it the ideal choice for this project.



## HOW TO SET AND START


1. CREATE A .env FILE with a connection to postgres (you can choose your DB. this project use this one):
	
	- [DATABASE_URI=postgresql+psycopg2://comic_dev:123456@localhost:5432/comic_store]




2. Ensure that a local database exist by making one in postgres shell:
	
	- enter the postgres shell
		- MacOS: run the `psql` command
		- Linux & WSL: run the `sudo -u postgres psql` command 
	
	- type `\l` to list all existing databases 
	
	- `CREATE DATABASE comic_store;` to create the database
	
	- connect to the database you want to use with `\c comic_store`




3. Ensure that a postgres shell user that has permissions to work with your database:
	
	- run `CREATE USER comic_dev WITH PASSWORD '123456';`
	
	- grant the user the permissions needed to work with the database, run `GRANT ALL PRIVILEGES ON DATABASE comic_store TO comic_dev;`
	
	- grant db schema permissions to the user as well, run `GRANT ALL ON SCHEMA public TO lms_dev;`




4. Exit the postgres shell with `\q`.




5. create a .flaskenv file and define: FLASK_APP=main.



6. Make a venv!:
	
	- run `python3 -m venv .venv` to make the venv
	
	- activate the venv with:
		- MacOS & Linux & WSL: `source .venv/bin/activate`
		- Windows: `.venv/Scripts/activate`
	
	- set the VSCode Python interpreter to the venv Python binary
		- CTRL + Shift + P to open up the command palette 
		- choose the interpreter with the path that matches the ".venv" path




7. Install dependencies from the project within the activated venv:
	
	- run `pip install -r ./requirements.txt`




8. Ensure that the flask app database exists and has any seed data:

	- check the source code for any CLI commands, e.g. `./controllers/cli_controller.py`

	- run the commands needed to drop tables, create tables, and then seed those created tables
		- flask db drop
		- flask db create
		- flask db seed

- flask run to run the server




9. OPTIONAL: set flask debug and a manual PORT value into `.flaskenv`:
	- `FLASK_DEBUG=1`
	- `FLASK_RUN_PORT=8080`




## API Endpoints


## Artists
| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST**   | `/artists/` | Create a new artist |
| **GET**    | `/artists/` | Get all artists |
| **GET**    | `/artists/<int:artist_id>` | Get a single artist |
| **PATCH/PUT** | `/artists/<int:artist_id>` | Update an artist |
| **DELETE** | `/artists/<int:artist_id>` | Delete an artist |

---

## Comics
| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST**   | `/comics/` | Create a new comic |
| **GET**    | `/comics/` | Get all comics |
| **GET**    | `/comics/<int:comic_id>` | Get a single comic |
| **PATCH/PUT** | `/comics/<int:comic_id>` | Update a comic |
| **DELETE** | `/comics/<int:comic_id>` | Delete a comic |

---

## Customers
| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST**   | `/costumers/` | Create a new customer |
| **GET**    | `/costumers/` | Get all customers |
| **GET**    | `/costumers/<int:costumer_id>` | Get a single customer |
| **PATCH/PUT** | `/costumers/<int:costumer_id>` | Update a customer |
| **DELETE** | `/costumers/<int:costumer_id>` | Delete a customer |

---

## Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST**   | `/orders/` | Create a new order |
| **GET**    | `/orders/` | Get all orders |
| **GET**    | `/orders/<int:order_id>` | Get a single order |
| **PATCH/PUT** | `/orders/<int:order_id>` | Update an order |
| **DELETE** | `/orders/<int:order_id>` | Delete an order |

---

## Order Comics (many-to-many relation)
| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST**   | `/order_comics/` | Create a new order-comic link |
| **GET**    | `/order_comics/` | Get all order-comic links |
| **GET**    | `/order_comics/<int:order_comic_id>` | Get a single order-comic link |
| **PATCH/PUT** | `/order_comics/<int:order_comic_id>` | Update an order-comic link |
| **DELETE** | `/order_comics/<int:order_comic_id>` | Delete an order-comic link |

---

## Publishers
| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST**   | `/publishers/` | Create a new publisher |
| **GET**    | `/publishers/` | Get all publishers |
| **GET**    | `/publishers/<int:publisher_id>` | Get a single publisher |
| **PATCH/PUT** | `/publishers/<int:publisher_id>` | Update a publisher |
| **DELETE** | `/publishers/<int:publisher_id>` | Delete a publisher |

---

## Writers
| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST**   | `/writers/` | Create a new writer |
| **GET**    | `/writers/` | Get all writers |
| **GET**    | `/writers/<int:writer_id>` | Get a single writer |
| **PATCH/PUT** | `/writers/<int:writer_id>` | Update a writer |
| **DELETE** | `/writers/<int:writer_id>` | Delete a writer |



- DISCLAIMER: Chatgpt was used to make this table look nice but all the contents were made by Max Acosta and the data of the routes was extracted using command `flask routes`.

REFERENCES: 
    PostgresSQL: Documentation [postgresql.org/docs/current/errcodes-appendix.html]

    (Help me with the validations)
    Docs.Python: [https://docs.python.org/3/library/re.html]

    Marshmallow: [https://marshmallow.readthedocs.io/en/stable/marshmallow.validate.html]

    w3schools: https://www.w3schools.com/python/ref_func_len.asp



Project Comic_Store API by Max Acosta. Thanks!
