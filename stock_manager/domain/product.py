from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    id: Optional[int]
    code: int
    name: str
    description: str
    purchase_price: float
    sale_price: float
    minimum_stock: int
