from sqlalchemy import Integer, PickleType
from sqlalchemy.orm import Mapped, mapped_column

from core.repositories.postgres_base import Base


class OlxData(Base):
    __tablename__ = 'olx_data'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    seller_name: Mapped[str | None]
    registration_date: Mapped[str | None]
    last_login: Mapped[str | None]
    url: Mapped[str | None]
    title: Mapped[str | None]
    image_urls: Mapped[list[str]] = mapped_column(PickleType)
    price: Mapped[str | None]
    created_at: Mapped[str | None]
    attributes: Mapped[str | None] = mapped_column(PickleType)
    description: Mapped[str | None]
    product_id: Mapped[str | None]
