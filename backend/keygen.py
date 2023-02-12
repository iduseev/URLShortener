# backend/keygen.py

import string
import secrets
from typing import AnyStr, Optional

from sqlalchemy.orm import Session

from . import crud


def create_random_key(length: Optional[int] = 5) -> AnyStr:
    """
    Generate unique key / secret_key

    :param length: _description_, defaults to 5
    :type length: int, optional
    :return: random unique key
    :rtype: AnyStr
    """
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


def create_unique_random_key(db: Session) -> AnyStr:
    """
    Check that every shortened URL exists only once within DB

    :param db: session with SQL DB
    :type db: Session
    :return: unique key
    :rtype: AnyStr
    """
    key = create_random_key()
    while crud.get_db_url_by_key(db=db, url_key=key):
        key = create_random_key()
    return key
