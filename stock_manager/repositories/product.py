from sqlalchemy import select

from stock_manager.domain.product import Product
from stock_manager.database import Session
from stock_manager.models import ProductModel


class ProductRepository():
    def all(self) -> list[Product]:
        with Session() as session:
            return [
                self.to_dataclass(m)
                for m in session.scalars(select(ProductModel)).all()
            ]

    def create(self, product: Product) -> Product:
        with Session() as session:
            model = ProductModel(
                code=product.code,
                name=product.name,
                minimum_stock=product.minimum_stock,
                description=product.description,
            )
            session.add(model)
            session.commit()
            return self.to_dataclass(model)

    def delete(self, id: int) -> None:
        with Session() as session:
            model = session.get(ProductModel, id)
            if model is not None:
                session.delete(model)
                session.commit()

    def to_dataclass(self, model: ProductModel) -> Product:
        return Product(
            id=model.id,
            code=model.code,
            name=model.name,
            minimum_stock=model.minimum_stock,
            description=model.description,
        )
