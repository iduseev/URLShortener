# backend/schemas.py

from typing import AnyStr
from pydantic import BaseModel, Field, AnyHttpUrl

'''
    Here we define what data the API is expecting from the client and the server
'''

class URLBase(BaseModel):
    target_url: AnyHttpUrl
    

class URL(URLBase):
    is_active: bool
    clicks: int

    class Config:
        orm_mode = True  # required by pydantic BaseModel to use ORM approach to work with DB


class URLInfo(URL):
    url: AnyStr
    admin_url: AnyStr
