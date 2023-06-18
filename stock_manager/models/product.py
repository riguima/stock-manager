from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from stock_manager.database import db


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


Base.metadata.create_all(db)
