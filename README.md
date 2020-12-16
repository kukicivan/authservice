# Authentication Service with Fast API

<p align="center">
    <em>Ready-to-use Authentication and Users Management backend.</em>
</p>

---
**Repository URL**: <a href="https://gitlab.com/ivan.kukic/authservice" target="_blank">
gitlab.com/ivan.kukic/authservice</a>
---

Authentication service provides **authentication** and **user management** supports. Therefore, it can be used by any
software project that needs to implement some kind of authentication mechanism and basic user management system in
place.

Authentication service is build on top of **FastAPI** framework. **FastAPI** is high performance framework build in **Python**.

## Features

* [X] Ready-to-use **register**, **login**, **forgot** and **reset password** endpoints
    * [X] POST `/auth/login`
    * [X] POST `/auth/register`
    * [X] POST `/auth/forgot-password`
    * [X] POST `/auth/reset-password`
* [X] Ready-to-use **user profile** routes
    * [X] GET `/users/me`
    * [X] PATCH `/users/me`
    * [X] GET `/users/{id}`
    * [X] DELETE `/users/{id}`
    * [X] PATCH `/users/{id}`
* [X] High performance **FastAPI** framework
* [X] Database backend with **SQLAlchemy**
* [X] Authentication backend with **FastAPI Users**
* [X] Writes **JWT token in a database**

## Install

### Setup environement

You should have [Pipenv](https://pipenv.readthedocs.io/en/latest/) installed. Then, you can install the dependencies
with:

```bash
pipenv install --dev
```

After that, `activate` the virtual environment:

### Configure

Enter your `DATABASE_URL` and `SECRET` in `.env` file.

```bash
DATABASE_URL = "sqlite:///./auth_service.db"
SECRET = "SECRET"
```

### Run server

You can run a server with:

```bash
uvicorn main:app --reload
```

## License

This project is licensed under the terms of the MIT license.
