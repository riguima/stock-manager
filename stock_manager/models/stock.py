from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

from stock_manager.database import db
from stock_manager.models.product import ProductModel


class Base(DeclarativeBase):
    pass


class StockModel(Base):
    __tablename__ = 'stock'
    id: Mapped[int] = mapped_column(primary_key=True)
    product: Mapped['ProductModel'] = relationship(back_populates='stock')
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    amount: Mapped[int]


Base.metadata.create_all(db)
