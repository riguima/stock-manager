from sqlalchemy import select

from stock_manager.database import Session
from stock_manager.domain.product import Product
from stock_manager.domain.stock import Stock
from stock_manager.models import ProductModel, StockModel
from stock_manager.repositories.product import ProductRepository


class StockRepository():
    def create(self, stock: Stock) -> Stock:
        with Session() as session:
            product = session.get(ProductModel, stock.product.id)
            model = StockModel(
                amount=stock.amount,
                product_id=product.id,
            )
            session.add(model)
            session.commit()
            return self.to_dataclass(model)

    def get_amount(self, product: Product) -> int:
        with Session() as session:
            query = select(StockModel).where(
                StockModel.product_id == product.id
            )
            return sum([s.amount for s in session.scalars(query).all()])

    def all(self) -> list[Stock]:
        with Session() as session:
            return [
                self.to_dataclass(s)
                for s in session.scalars(select(StockModel)).all()
            ]

    def to_dataclass(self, model: StockModel) -> Stock:
        product = ProductRepository().to_dataclass(model.product)
        return Stock(id=model.id, product=product, amount=model.amount)
