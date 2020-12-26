# Authentication service with Fast API

<p align="center">
    <em>Ready-to-use Authentication and Users Management backend.</em>
</p>

---
**URL**: <a href="https://gitlab.com/ivan.kukic/authservice" target="_blank">
gitlab.com/ivan.kukic/authservice</a>
---

Authentication service provides **authentication** and **user management** out of the box. It can be used by project
that needs authentication and user management system.

## Features

*  **Authentication**
    * [X] POST `/auth/login`
    * [X] POST `/auth/register`
    * [X] POST `/auth/forgot-password`
    * [X] POST `/auth/reset-password`
*  **Users**
    * [X] GET `/users/me`
    * [X] PATCH `/users/me`
    * [X] GET `/users/{id}`
    * [X] DELETE `/users/{id}`
    * [X] PATCH `/users/{id}`
    * [X] GET `/users`
*  Under the hood
    * [X]  **FastAPI** framework
    * [X] **JWT** Authentication
    * [X] **SQL Alchemy**

## Install

### Setup environement

`Activate` the virtual environment. Then, you can install the dependencies with:

```bash
pip install -r requirements.txt
```

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
