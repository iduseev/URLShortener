# backend/crud.py

from typing import AnyStr

from sqlalchemy.orm import Session

from . import schemas, models, keygen


def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    """_summary_

    :param db: _description_
    :type db: Session
    :param url: _description_
    :type url: schemas.URLBase
    :return: _description_
    :rtype: models.URL
    """
    key = keygen.create_unique_random_key(db=db)
    # the key prefix indicates which shortened URL the secret key belongs to
    secret_key = f"{key}_{keygen.create_random_key(length=8)}"
    db_url = models.URL(
        target_url=url.target_url,
        key=key,
        secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

    # add key and secret_key to db_url to match the required URLInfo schema that we need to return 
    # db_url.url = key
    # db_url.admin_url = secret_key


def get_db_url_by_key(db: Session, url_key: AnyStr) -> models.URL:
    """
    Check if a key already exists in the database

    :param db: Session object of connection to the DB
    :type db: Session
    :param url_key: key to be checked
    :type url_key: AnyStr
    :return: either None or a DB entry with a provided key
    :rtype: models.URL
    """
    return (
        db.query(models.URL).filter(
            models.URL.key == url_key,
            models.URL.is_active
        ).first()
    )