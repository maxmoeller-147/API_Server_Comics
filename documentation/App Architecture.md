# DEV1004 - AS01: Containerization of an Existing Application

## Table of Contents

1. [Project Summary](#project-summary)
2. [Application Architecture](#application-architecture)
3. [Database Architecture](#database-architecture)
4. [CI/CD Pipeline](#cicd-pipeline)
5. [Containerised Architecture](#containerized-architecture)
6. [Application Overview](#application-overview)

## Project Summary
The Comics API Server is a containerised web application that provides a RESTful API that allows users to manage the operations of a comic store, such as comics, customers, orders, artists, writers, and publishers. The project was developed using Python and Flask, with PostgreSQL as the database engine, and is containerised and executed using Docker. In addition to the core application, a continuous integration pipeline was implemented using GitHub Actions to automate building, testing, and validation.

This documentation explains the architecture of the application through diagrams and descriptions that illustrate how each component of the system interacts.

More Info on:  

- [Technical Readme](./README.md)
- [Leave your Feedback!](./documentation/Feedback.md)

## Application Architecture 

![Application Architecture Diagram](images/app_architecture.png)

A Flask Application is the core of this project, structured and initialilised throught a factory function named create_app(), instead of a global Flask instance. This allows configuration to be dynamically applied depending on the environment in which the application is running and provides significant flexibility, as it enables the same code to be reused for development, testing, and production environments without modification.

main.py imports and executes this function when the application starts. Then the function creates the Flask application instance, loads environment variables, configures the database connection, registers error handlers, and attaches all relevant blueprints.

The structure of the API is organised into layers. The presentation layer is implemented through a series of Flask Blueprints, each responsible for a specific domain entity. For example, there are dedicated controllers for customers, comics, orders, artists, writers, and publishers. These controllers define the HTTP routes that external clients interact with, and they handle tasks such as receiving requests, validating input data, interacting with the database, and returning formatted JSON responses.

Validation is handled using Marshmallow schemas and custom validator functions. All incoming data is checked before any database operation is performed. This ensures that invalid data cannot corrupt the system and that consistent error messages are returned to API consumers if any errors. Centralised error handling strengthens this layer by capturing and formatting exceptions in a industry standart way.

The data access layer is built using SQLAlchemy, all database models are defined as Python classes inside the models directory and represent the entities of the comic store. These models define relationships between tables, enforce constraints, and provide an object oriented way to interact with PostgreSQL. The database instance itself has a modular design and is initialised in a separate module and injected into the application by the factory function.

In addition to HTTP routes, the application includes custom Flask CLI commands that allow database tables to be created, dropped, and seeded with initial data. These commands provide a convenient way to manage the database lifecycle directly from the terminal and are particularly useful when running the application inside Docker containers.



## Database Architecture 

![Database Architecture Diagram](images/db_architecture.png)

The database is designed by an Entity Relationship Diagram that models the logic of the comic store. The schema includes tables for:
 - comics 
 - customers
 - orders 
 - artists
 - writers
 - publishers

As well as a junction table to represent the many-to-many relationship between orders and comics. 

Each entity has defined relationships. For instance, a publisher can publish many comics, a customer can place many orders, and a single order can contain multiple comics. Artists and writers are associated with the comics they helped create, enabling the system to represent real world scenarios. This relational model allows the API to support realistic operations such as retrieving a customer’s order history, listing all comics from a specific publisher, or determining which comics are included in a particular order.

The use of PostgreSQL as the database engine ensures data integrity, transactional reliability, and scalability. All interactions with the database happens through SQLAlchemy, which abstracts raw SQL into a higher level object relational mapping layer. This design choice makes the application easier to maintain and reduces the risk of database-related bugs.

## CI/CD Pipeline Architecture 

![CI/CD Pipeline Architecture Diagram](images/workflow_diagram.png)

To improve reliability and code quality, a continuous integration pipeline was implemented using GitHub Actions. The workflow is automatically triggered whenever new code is pushed to the main branch or when a pull request is opened. This ensures that every change to the project is validated before being merged.

The pipeline begins by checking out the repository and setting up Docker Buildx. It then builds the API image from the Dockerfile to confirm that the container can be created successfully. After the image is built, an isolated Docker network is created within the GitHub runner environment. A PostgreSQL container is launched using credentials stored securely as GitHub Secrets, followed by the API container configured with a secret database connection string.

Once both containers are running, the workflow performs a health check by calling a dedicated /health endpoint exposed by the API. This confirms that the application has started correctly and is able to respond to HTTP requests. If the API responds as expected, the build is marked as successful. Regardless of the outcome, the pipeline then cleans up all containers and networks to leave the environment in a clean state.

This automated workflow ensures that the project remains in a working state at all times. By relying on GitHub Secrets for sensitive data, the pipeline also satisfies security requirements by avoiding the exposure of credentials in source code.

## Containerised Architecture 

![Containerised Architecture Diagram](images/container_architecture.png)

The system is composed of two main containers: one running the Flask API and the other running PostgreSQL. These containers are orchestrated using Docker Compose, which defines how the services are built, configured, and connected.

#### API Container:

The API container is built from a custom Dockerfile based on the python:3.12-slim image. During the build process, all project dependencies are installed, the source code is copied into the container, and the appropriate startup command is defined.

Two separate Docker Compose configurations are included in the project: one for development and one for production. The development configuration exposes additional ports and enables debugging features, while the production configuration focuses on security and stability.

In development mode, the container runs the Flask development server, while in production mode it runs Gunicorn, a more robust WSGI server.

External clients such as web browsers or API tools send HTTP requests to the server’s public IP address on port 8080. These requests are routed by Docker to the Flask API container, where they are processed by Gunicorn and Flask. Whenever the application needs to access persistent data, it communicates internally with the PostgreSQL container through the private Docker network.

#### Database Container:

The database container runs PostgreSQL 16 using the lightweight Alpine image. A persistent Docker volume is attached to the container so that database data is not lost when containers are restarted or rebuilt. The API container communicates with the database container through an internal Docker network using a connection string provided via environment variables.

#### Environment Variables:

This variables control all configuration, making the project easy to deploy the same system on different operating systems with minimal configurations. 
Sensitive information such as database credentials and connection strings are never hardcoded into the source code. Instead, they are injected into containers at runtime, allowing secure and flexible configuration.

## Interaction between Components

Although each diagram focuses on a different aspect of the system, they all describe parts of the same integrated architecture.
- The internal application design explains how the Flask codebase is structured and how requests are handled. 

- The database diagram shows how information is stored and related. 

- The Docker Compose architecture demonstrates how the application is packaged and executed.

- CI/CD diagram illustrates how the project is automatically built and validated.

A user request flows through the entire architecture. A client sends an HTTP request to the deployed API. The request is received by the Flask controller layer, validated using Marshmallow schemas, and translated into database operations via SQLAlchemy. PostgreSQL processes the query and returns the necessary data, which is formatted into JSON and sent back to the client. Throughout this process, Docker ensures that both services remain isolated and portable, while the CI pipeline ensures that the system remains reliable and maintainable.


## Application Overview

The architecture designed for this project combines a modular Flask codebase, well structured relational database, full Docker containerisation, and an automated CI/CD pipeline.

The use of the application factory pattern, blueprints, validation layers, and ORM models ensures that the code remains clean and maintainable. Docker Compose provides reproducible environments for both development and production, while GitHub Actions guarantees that every change to the project is automatically tested and verified.






