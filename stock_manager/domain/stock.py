from typing import Optional

from pydantic import BaseModel

from stock_manager.domain.product import Product


class Stock(BaseModel):
    id: Optional[int] = None
    product: Product
    amount: int
