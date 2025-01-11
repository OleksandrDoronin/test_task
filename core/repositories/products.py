from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from core.models import Products, Seller
from core.repositories.postgres_base import get_db_session
from core.schemas.products import ProductBase, SellerBase


class ProductsRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_seller_by_name(self, name: str) -> Seller | None:
        return self.session.query(Seller).filter_by(name=name).first()

    def save_seller(self, seller_data: SellerBase) -> Seller:
        seller = Seller(**seller_data.model_dump())

        try:
            self.session.add(seller)
            self.session.commit()
            return seller
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f'Error saving seller: {str(e)}')

    def save_product(self, product_data: ProductBase, seller_name: str) -> None:
        seller = self.get_seller_by_name(name=seller_name)

        if not seller:
            self.save_seller(product_data.seller)

        product_dict = product_data.model_dump()
        product_dict['seller_id'] = seller.id
        product = Products(**product_dict)

        try:
            self.session.add(product)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f'Error saving product: {str(e)}')

    def add_product(self, product_data: ProductBase) -> None:
        seller_name = product_data.seller.name
        self.save_product(product_data=product_data, seller_name=seller_name)


def get_products_repository() -> ProductsRepository:
    with get_db_session() as session:
        return ProductsRepository(session=session)
