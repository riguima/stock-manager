from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from stock_manager.database import db


class Base(DeclarativeBase):
    pass


class ProductModel(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[int]
    name: Mapped[str]
    description: Mapped[str]
    minimum_stock: Mapped[int]
    stock: Mapped['StockModel'] = relationship(back_populates='product')


class StockModel(Base):
    __tablename__ = 'stock'
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    product: Mapped['ProductModel'] = relationship(back_populates='stock')
    amount: Mapped[int]


Base.metadata.create_all(db)
