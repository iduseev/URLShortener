# backend/main.py

from typing import AnyStr, Dict, Union, Optional, Tuple, List, NoReturn

import validators
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse

from .database import SessionLocal, engine
from . import schemas, models, keygen, crud


app = FastAPI()

# binds the database engine
# if the defined DB does not exist yet, then it'll be created with all modeled tables one the app will be run
models.Base.metadata.create_all(bind=engine)

def get_db():
    """
    Creates and yields new DB session with each request

    :rtype: None
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        # close DB session even in case of errors
        db.close()


def raise_bad_request(message: AnyStr) -> NoReturn:
    """
    Raises Bad Request (400) error on demand

    :param message: descriptive message
    :type message: AnyStr
    :raises HTTPException: Bad Request (400) error
    :rtype: NoReturn
    """
    raise HTTPException(status_code=400, detail=message)


def raise_not_found(request: Request) -> NoReturn:
    """
    Raises Not Found (404) error on demand

    :param request: request object
    :type request: Request
    :raises HTTPException: Not Found (404) error
    :rtype: NoReturn
    """
    message = f"URL '{request.url}' doesn't exist!"
    raise HTTPException(status_code=404, detail=message)


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
    # create a DB entry to target_url
    db_url = models.URL(
        target_url=url.target_url,
        key=keygen.create_random_key(length=5),
        secret_key=keygen.create_random_key(length=8)
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    # add key and secret_key to db_url to match the required URLInfo schema that we need to return 
    db_url = crud.create_db_url(db=db, url=url)
    db_url.url = db_url.key
    db_url.admin_url = db_url.secret_key
    return db_url


@app.post("/url/{target_url}")
def show_url_info():
    pass


@app.get("/{url_key}")
def forward_to_target_url(
    url_key: AnyStr,
    request: Request,
    db: Session = Depends(get_db)
) -> Union[RedirectResponse, NoReturn]:
    """
    Redirecting HTTP request with URL.key to the actual target URL address

    :param url_key: _description_
    :type url_key: AnyStr
    :param request: Request object
    :type request: Request
    :param db: Session object (session with SQL DB), defaults to Depends(get_db)
    :type db: Session, optional
    :return: either RedirectResponse class instance or raising not found exception if key doesn't match any URL in DB
    :rtype: Union[RedirectResponse, NoReturn]
    """
    db_url = (
        db.query(models.URL).filter(
            models.URL.key == url_key,
            models.URL.is_active
        ).first()
    )
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request=request)
