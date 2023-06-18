from sqlalchemy import select

from stock_manager.domain.product import Product
from stock_manager.database import Session
from stock_manager.models.product import ProductModel


class ProductRepository():
    def all(self) -> list[Product]:
        with Session() as session:
            return [
                self._to_dataclass(m)
                for m in session.scalars(select(ProductModel)).all()
            ]

    def create(self, product: Product) -> Product:
        with Session() as session:
            model = ProductModel(
                code=product.code,
                purchase_price=product.purchase_price,
                sale_price=product.sale_price,
                minimum_stock=product.minimum_stock,
                description=product.description,
            )
            session.add(model)
            session.commit()
            return self._to_dataclass(model)

    def delete(self, id: int) -> None:
        with Session() as session:
            model = session.get(ProductModel, id)
            if model is not None:
                session.delete(model)
                session.commit()

    def _to_dataclass(self, model: ProductModel) -> Product:
        return Product(
            id=model.id,
            code=model.code,
            name=model.name,
            purchase_price=model.purchase_price,
            sale_price=model.sale_price,
            minimum_stock=model.minimum_stock,
            description=model.description,
        )
