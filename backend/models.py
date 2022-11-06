from typing import AnyStr
from pydantic import BaseModel, Field

class CreateURLShortener(BaseModel):
    url: AnyStr
    