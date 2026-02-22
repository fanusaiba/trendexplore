from pydantic import BaseModel
from typing import optional 
class trend(BaseModel):
    title: str
    source: str
    score: optional[int] = None
    url: optional[str] = None
    country: str
    category: str