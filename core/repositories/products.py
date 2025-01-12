from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from core.models import OlxData
from core.repositories.postgres_base import get_db_session
from core.schemas.products import OlxDataBase


class OlxDataRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_product_by_product_id(self, product_id: str) -> OlxData | None:
        return self.session.query(OlxData).filter_by(product_id=product_id).first()

    def save_product(self, product_data: OlxDataBase) -> None:
        existing_product = self.get_product_by_product_id(product_id=product_data.product_id)

        if existing_product:
            for key, value in product_data.model_dump(exclude_unset=True).items():
                setattr(existing_product, key, value)
        else:
            product_dict = product_data.model_dump()
            product = OlxData(**product_dict)

            try:
                self.session.add(product)
                self.session.commit()
            except SQLAlchemyError as e:
                self.session.rollback()
                raise ValueError(f'Error saving product: {str(e)}')

    def add_product(self, product_data: OlxDataBase) -> None:
        self.save_product(product_data)


def get_olx_data_repository() -> OlxDataRepository:
    with get_db_session() as session:
        return OlxDataRepository(session=session)
