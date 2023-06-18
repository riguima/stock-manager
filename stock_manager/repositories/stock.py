from sqlalchemy import select

from stock_manager.database import Session
from stock_manager.domain.product import Product
from stock_manager.domain.stock import Stock
from stock_manager.models.stock import StockModel


class StockRepository():
    def create(self, stock: Stock) -> Stock:
        with Session() as session:
            model = StockModel(
                product=stock.product,
                amount=stock.amount,
            )
            session.add(model)
            session.commit()

    def get_amount(self, product: Product) -> int:
        with Session() as session:
            query = select(Stock).where(Stock.product_id == product.id)
            return sum([s.amount for s in session.scalars(query).all()])
