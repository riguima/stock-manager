from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from stock_manager.database import db


class Base(DeclarativeBase):
    pass


class ProductModel(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[int]
    description: Mapped[str]
    purchase_price: Mapped[float]
    sale_price: Mapped[float]
    minimum_stock: Mapped[int]


Base.metadata.create_all(db)
