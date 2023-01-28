# backend/endpoints.py

import asyncio
from pathlib import Path
from typing import Any, AnyStr, Dict, Union, Optional, Tuple, List, NoReturn

import requests
import validators
from fastapi import Depends, Path, File, Body, Form, Query, UploadFile, FastAPI, HTTPException, status

from . import schemas


app = FastAPI()

def raise_bad_request(message: AnyStr) -> NoReturn:
    raise HTTPException(status_code=400, detail=message)


@app.get("/")
def read_root() -> AnyStr:
    return "Welcome to the URL shortener API!"


@app.get("/about")
def about() -> Dict:
    return {"Data": "About"}


@app.post("/url")
def create_url(url: schemas.URLBase):
    return f"TODO: reate database entry for {url.target_url}"


@app.post("/url/{target_url}")
def show_url_info():
    pass