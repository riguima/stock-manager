from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    id: Optional[int]
    code: int
    name: str
    description: str
    minimum_stock: int
