# Şañıraq.kz - Real Estate Marketplace


## Project Overview
Şañıraq.kz is a dynamic real estate marketplace that connects property owners and seekers in Kazakhstan. The platform allows users to create, modify, and delete property listings, along with the ability to add and manage comments. This Minimum Viable Product (MVP) focuses on essential features like user registration, property management, and commenting functionality.

## Features
1. User Registration: Users can register on the platform by providing essential details like email, phone number, password, name, and city.

2. User Authentication: Utilizing OAuth2PasswordBearer, the platform ensures secure user authentication.

3. User Profile Management: Authenticated users can update their personal information, including phone number, name, and city.

4. Property Listing Creation: Users can create property listings with details such as type, price, address, area, number of rooms, and a description.

5. Property Listing Modification and Deletion: Authenticated users can modify and delete their property listings.

6. Commenting System: Users can add comments to property listings, providing valuable insights and feedback.

7. Comment Management: Users can modify and delete their comments on property listings.

8. API Endpoints: The project exposes various API endpoints for user registration, authentication, property listing management, and commenting.

## Technology Stack
* FastAPI: A modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints.

* SQLAlchemy: A powerful and flexible SQL toolkit and Object-Relational Mapping (ORM) library for Python.

* Alembic: A lightweight database migration tool for usage with SQLAlchemy.

* Docker: Containerization for easy deployment and consistent environments.


## Project Structure
```bash
.
├── alembic
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
│       ├── 5373a36b15a2_create_user_ad_comment_tables.py
├── alembic.ini
├── app
│   ├── api
│   │   ├── repositories
│   │   │   ├── comments.py
│   │   │   ├── posts.py
│   │   │   └── users.py
│   │   ├── serializers
│   │   │   ├── comments.py
│   │   │   ├── posts.py
│   │   │   └── users.py
│   │   └── views
│   │       ├── auth.py
│   │       ├── __init__.py
│   │       └── shanyraks.py
│   ├── db
│   │   ├── base.py
│   │   ├── database.py
│   │   ├── __init__.py
│   │   ├── models.py
│   ├── main.py
├── Dockerfile
├── railway.json
├── requirements.txt
├── scripts
│   └── launch.sh
└── sql_app.db
```


## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/Bayashat/Shanyrak.kz.git
cd Shanyrak.kz
```

Create a virtual environment (optional but recommended):

```bash
python3 -m venv .venv
```

Activate the virtual environment:

* Windows:
```bash
.venv\Scripts\activate
```

* macOS/Linux:
```bash
source .venv/bin/activate
```

Install the project dependencies:
```bash
pip install -r requirements.txt
```

## Database Setup

Migrate the database using Alembic:

```bash
alembic upgrade head
```

## Running the API

Run the FastAPI application:

```bash
uvicorn app.main:app --reload
```
The API will be available at http://127.0.0.1:8000.

## API Endpoints

### User Authentication
* `POST /auth/users`: Register a new user.
* `POST /auth/users/login`: Log in with email and password.
* `GET/auth/users/me`: View user profile information.
* `PATCH/auth/users/me`: Modify profile information.

### Property Listings
* `POST /shanyraks`: Create a new property listing
* `GET /shanyraks/{id}`: Retrieve details of a property listing.
* `PATCH /shanyraks/{id}`: Modify details of a property listing.
* `DELETE /shanyraks/{id}`: Delete a property listing.



### Comments
* `POST /shanyraks/{id}/comments`: Add a comment to a property listing.
* `GET /shanyraks/{id}/comments`: Retrieve comments for a property listing.
* `PATCH /shanyraks/{id}/comments/{comment_id}`: Modify a comment on a property listing.
* `DELETE /shanyraks/{id}/comments/{comment_id}`: Delete a comment on a property listing.

## Docker
Build the Docker image:
```bash
docker build -t shanyrak-api .
```

Run the Docker container:

```bash
docker run -p 8080:8080 -e PORT=8080 shanyrak-api
```
The API will be available at http://0.0.0.0:8080.

## Author
Tokmukamet Bayashat