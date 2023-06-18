from typing import Optional

from pydantic import BaseModel


class ProductModel(BaseModel):
    id: Optional[int]
    code: int
    description: str
    purchase_price: float
    sale_price: float
    minimum_stock: int
