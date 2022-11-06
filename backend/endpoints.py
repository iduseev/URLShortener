import asyncio
from pathlib import Path
from typing import Any, AnyStr, Dict, Union, Optional, Tuple, List, NoReturn

import requests
from fastapi import Depends, Path, File, Body, Form, Query, UploadFile, FastAPI, HTTPException, status


app = FastAPI()


@app.get("/")
def home() -> AnyStr:
    return "Hello, World!"


@app.get("/about")
def about() -> Dict:
    return {"Data": "About"}


@app.post("/url/{target_url}")
def show_url_info():
    pass