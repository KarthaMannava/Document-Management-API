[![Document API CI/CD](https://github.com/pmutua/fastapi-project/actions/workflows/cicd.yml/badge.svg)](https://github.com/pmutua/fastapi-project/actions/workflows/cicd.yml)

# Document API

## Technologies

- Python 3.11+
- Poetry
- Fast API
- PostgreSQL
- SQLAlchemy
- Uvicorn
- AWS

## Local Development

1. Clone the repository and `cd` into the repository directory.
2. Check out the Python version `python --version` if less than 3.11 use `pyenv` to install and swithc to 3.11+
3. Make sure [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) is installed.
4. Create a virtual environment: `python -n venv env`
5. Activate the virtual environment:

    **On Windows:**
    Run the following command: `env\Scripts\activate`

    **On Linux:**
    Run the following command: `source env/bin/activate`

6. Install dependences: `poetry install`
7. You can run the server in 3 `different ways. Choose the one you want.

   - **Option 1 (run with poetry):**

      Run the following command `poetry run uvicorn main:app --reload`

   - **Option 2 (run using existing scripts):**

      _On Windows_
      Run the following command `scripts\run.bat`

      _On Linux_
    Make sure to give the scripts executable permissions if running on a Unix-like system. You can do this by running `chmod +x scripts/run.sh` in the terminal. Then run the following command `scripts/run.sh`

   - **Option 3 (run with Docker):**

    Run: `docker-compose build`
    Then run the following command: `docker-compose up`

8. Updating migrations
    **Updating Migrations**
    Run the following:

    `alembic revision --autogenerate -m "Added user and document table"`

    `alembic upgrade head`

9. Access swagger docs at: `http:127.0.0.1:8080/docs`

## Schema

User Table
----------

| Column      | Description                                              |
|-------------|----------------------------------------------------------|
| user_id     | Unique identifier for each user (Primary Key).            |
| email       | User's email address.                                    |
| password    | User's password (stored securely, e.g., hashed).          |
| created_at  | Timestamp indicating when the user was created.           |
| updated_at  | Timestamp indicating the last update to the user's information. |

Document Table
--------------

| Column         | Description                                              |
|----------------|----------------------------------------------------------|
| document_id    | Unique identifier for each document (Primary Key).        |
| user_id        | Reference to the user_id in the User table, indicating the owner of the document (Foreign Key). |
| title          | Title of the document.                                   |
| file_type      | Type of the document, selected from a predefined list (enum). |
| file_url       | URL or path to the uploaded file.                         |
| description    | Description of the document.                              |
| created_at     | Timestamp indicating when the document was uploaded.      |
| updated_at     | Timestamp indicating the last update to the document.     |

## Features

### Authentication

- User registration: Users should be able to register by providing their username, email, and password.
- User login: Registered users should be able to log in using their username and password to obtain a JSON Web Token (JWT).
- JWT-based authentication: All protected routes should require authentication using JWT. Users should include the JWT in the authorization header of their requests.

### Document Upload

- Document Model: Create a document model with the following attributes:
  - `title`: Title of the document (string).
  - `file_type`: Type of the document, selected from a predefined list (enum).
  - `file_url`: URL or path to the uploaded file (string).
  - `description`: Description of the document (string).

- Upload Endpoint: Create an API endpoint to upload a document with the following features:
  - Accepts the document details (title, file type, file URL, description) as input.
  - Validates the input data against the defined model.
  - Stores the document in a database or file storage system.
  - Returns a success message or appropriate error response.

### Protected Route

- Retrieve All Documents: Create a protected route that requires authentication to retrieve all uploaded documents.
- Retrieve a Specific Document: Create a protected route that requires authentication to retrieve a specific document by its ID.
- Update Document Details: Create a protected route that requires authentication to update the details of a specific document.
- Delete Document: Create a protected route that requires authentication to delete a specific document.

### Additional Requirements

- Error Handling: Implement appropriate error handling and return meaningful error responses for various scenarios (e.g., invalid input, authentication failure, resource not found).
- Documentation: Generate API documentation automatically based on the defined routes and models.
- Unit Testing: Write unit tests to verify the functionality of the authentication, document upload, and text extraction endpoints.
- Security Considerations: Implement necessary security measures, such as password hashing for user authentication and secure file storage for uploaded documents.
- Extract Text from Images: Create an API endpoint to extract text from uploaded images. This endpoint should:
  - Accept an image file as input.
  - Process the image and extract text from it using OCR or other image processing techniques.
  - Return the extracted text as a response.
- CI/CD Pipeline: Set up a CI/CD pipeline for automated building, testing, and deployment of the application. Configure tasks for building the application, running tests, generating documentation, and deploying to a server or cloud platform.
- Deployment: Prepare the application for deployment to a server or cloud platform, including any necessary configuration files and instructions.

## Project idea skeleton

- `main.py`: The main entry point of the application.

- `app/`: The root folder of the application.
  - `api/`: Contains API-related components.
    - `routers/`: Contains API route handlers.
      - `__init__.py`: Initializes the API routers.
      - `route1.py`: Defines routes and handlers for Route 1.
      - `route2.py`: Defines routes and handlers for Route 2.
      - ... (additional route files)
    - `models/`: Contains data models for the API.
      - `__init__.py`: Initializes the API models.
      - `model1.py`: Defines the data model for Model 1.
      - `model2.py`: Defines the data model for Model 2.
      - ... (additional model files)
    - `schemas/`: Contains Pydantic schemas for request/response validation.
      - `__init__.py`: Initializes the API schemas.
      - `schema1.py`: Defines the Pydantic schema for Schema 1.
      - `schema2.py`: Defines the Pydantic schema for Schema 2.
      - ... (additional schema files)
  - `services/`: Contains service modules that handle business logic.
    - `__init__.py`: Initializes the services.
    - `route1_service.py`: Implements the service logic for Route 1.
    - `route2_service.py`: Implements the service logic for Route 2.
    - ... (additional service files)
  - `repositories/`: Contains repository modules for data access.
    - `__init__.py`: Initializes the repositories.
    - `route1_repository.py`: Implements the repository logic for Route 1.
    - `route2_repository.py`: Implements the repository logic for Route 2.
    - ... (additional repository files)
  - `utils/`: Contains utility modules with reusable functions.
    - `__init__.py`: Initializes the utility modules.
    - `utility1.py`: Provides utility functions for common tasks.
    - `utility2.py`: Provides utility functions for common tasks.
    - ... (additional utility files)

- `tests/`: Contains test cases for the application.
  - `test_route1.py`: Test cases for Route 1.
  - `test_route2.py`: Test cases for Route 2.
  - ... (additional test files)

- `config/`: Contains configuration files and settings.
  - `__init__.py`: Initializes the configuration.
  - `settings.py`: Stores application settings.
  - `database.py`: Configuration related to the database.
  - ... (additional configuration files)

- `requirements.txt`: Lists the project dependencies.

- `Dockerfile`: Defines the Docker image configuration for the application.
- `docker-compose.yml`: Defines the Docker configuration for docker containers
