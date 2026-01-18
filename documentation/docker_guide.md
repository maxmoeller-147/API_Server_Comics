# How to Run the Application with Docker

The application is fully containerised and can be executed in both development and production environments using Docker and Docker Compose. This ensures that the system can be run consistently on any machine without requiring manual installation of dependencies such as Python or PostgreSQL.

### Prerequisites

To run the project, the following software must be installed:

    - Docker

    - Docker Compose

No additional local setup is required, as all dependencies are managed inside containers.

## Running the Development Environment

The development environment is designed for local testing and debugging. It runs the Flask application using the built-in development server and connects to a PostgreSQL database container.

To start the development environment, run the following command from the project root directory:

    docker compose -f docker-compose.dev.yml up -d

This command will:

- Build the API image from the Dockerfile
- Start a PostgreSQL container
- Start the Flask API container
- Create an isolated Docker network for communication
- Mount a persistent database volume

Once the containers are running, the API will be available at:

     http://localhost:8080
 
### Database Setup in Development

After starting the containers for the first time, the database can be initialised using the custom Flask CLI commands included in the project:

    docker compose -f docker-compose.dev.yml exec api flask db create
    
    docker compose -f docker-compose.dev.yml exec api flask db seed

These commands create the database tables and populate them with initial sample data.

## Running the Production Environment

The production configuration uses Gunicorn as the WSGI server and runs with debugging disabled to simulate a real deployment scenario.

To run the production version of the application:

    docker compose -f docker-compose.prod.yml up -d


This setup mirrors a realistic deployment environment and includes:
- Optimised Gunicorn server
- Production environment variables
- Persistent PostgreSQL database
- Isolated internal Docker network

## Stopping the Application

To stop and remove all running containers, the following command can be used:

For development:

    docker compose -f docker-compose.dev.yml down

For production:

    docker compose -f docker-compose.prod.yml down


## Verifying the Application

A health check endpoint is included to confirm that the API is running correctly. After starting the containers, the application status can be verified by visiting:

    http://localhost:8080/health

If the system is running correctly, it will return a JSON response indicating that the service is operational.

## Environment Variables

All sensitive configuration values are managed using environment variables. In development, default values are provided for convenience, while in production these values are supplied securely using external secrets. This approach ensures that credentials are never hard-coded into the source code or committed to version control.