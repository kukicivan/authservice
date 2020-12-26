from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def add_middleware(app: FastAPI):
    origins = [
        "http://localhost:4200",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )