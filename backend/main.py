# backend/main.py

import string
import secrets
import asyncio
from pathlib import Path
from typing import Any, AnyStr, Dict, Union, Optional, Tuple, List, NoReturn

import requests
import validators
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import schemas, models
from .database import SessionLocal, engine


app = FastAPI()

# binds the database engine
# if the defined DB does not exist yet, then it'll be created with all modeled tables one the app will be run
models.Base.metadata.create_all(bind=engine)

def get_db():
    """
    Creates and yields new DB session with each request

    :rtype: _type_
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        # close DB session even in case of errors
        db.close()

def raise_bad_request(message: AnyStr) -> NoReturn:
    raise HTTPException(status_code=400, detail=message)


@app.get("/")
def read_root() -> AnyStr:
    return "Welcome to the URL shortener API!"


@app.get("/about")
def about() -> Dict:
    return {"Data": "About"}


# path operation decorator that makes sure that the create_url() function responds to any 
# POST request at the /url path
@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Optional[Session] = Depends(get_db)) -> models.URL:
    """
    Requires a URLBase schema as an argument and depends on the database session. 
    By passing get_db into Depends(), you establish a database session for the request 
    and close the session when the request is finished

    :param url: instance of URLBase parent class with target_url attribute
    :type url: schemas.URLBase

    :param db: instance of Session class, defaults to Depends(get_db)
    :type db: Optional[Session]

    :return: instance of models.URL class with updated values of attributes
    :rtype: models.URL
    """
    # ensure that a valid URL is provided, otherwise raise Exception
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid!")
    # generate unique key and secret_key
    chars = string.ascii_uppercase
    key = "".join(secrets.choice(chars) for _ in range(5))
    secret_key = "".join(secrets.choice(chars) for _ in range(8))
    # create a DB entry to target_url
    db_url = models.URL(
        target_url=url.target_url,
        key=key,
        secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    # add key and secret_key to db_url to match the required URLInfo schema that we need to return 
    db_url.url = key
    db_url.admin_url = secret_key

    return db_url


@app.post("/url/{target_url}")
def show_url_info():
    pass