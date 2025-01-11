from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.repositories.postgres_base import Base


class Seller(Base):
    __tablename__ = 'sellers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str]
    rating: Mapped[str | None]
    registration_date: Mapped[str]
    last_login: Mapped[str]
    phone_number: Mapped[str | None]

    products: Mapped[list['Products']] = relationship(
        'Products', back_populates='seller', cascade='all, delete-orphan'
    )


class Products(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    url: Mapped[str]
    title: Mapped[str]
    picture: Mapped[str | None]
    price: Mapped[float]
    attributes: Mapped[str | None]
    description: Mapped[str | None]
    locations: Mapped[str | None]
    product_id: Mapped[str]
    viewed: Mapped[int]
    seller_id: Mapped[int] = mapped_column(ForeignKey('sellers.id', ondelete='CASCADE'))

    seller: Mapped['Seller'] = relationship('Seller', back_populates='products')
