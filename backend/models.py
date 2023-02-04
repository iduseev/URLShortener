# backend/models.py

from sqlalchemy import Boolean, Column, Integer, String

from .database import Base

'''
    Decalre the way the data should be stored in the DB
'''

class URL(Base):
    """
    Database model

    :param Base: class that connects the DB engine to the SQLAlchemy
    :type Base: declarative_base instance
    """
    __tablename__ = "urls"  # it is common to give plural name to DB table 

    id = Column(
        Integer, 
        primary_key=True  # so we don't need to provide a unique argument as it default to True for primary key anyways
    )
    key = Column(
        String, 
        unique=True, 
        index=True
    )
    secret_key = Column(
        String, 
        unique=True, 
        index=True
    )
    target_url = Column(
        String,  # do not set argument unique=True as it will prevent users to be able to forward the same URL
        index=True
    )
    is_active = Column(
        Boolean, 
        default=True
    )
    clicks=Column(
        Integer, 
        default=0
    )
