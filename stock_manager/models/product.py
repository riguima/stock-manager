from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from stock_manager.database import db
from stock_manager.models.stock import StockModel


class Base(DeclarativeBase):
    pass


class ProductModel(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[int]
    name: Mapped[str]
    description: Mapped[str]
    purchase_price: Mapped[float]
    sale_price: Mapped[float]
    minimum_stock: Mapped[int]
    stock: Mapped['StockModel'] = relationship(back_populates='product')


Base.metadata.create_all(db)
