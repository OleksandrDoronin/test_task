from pydantic import BaseModel, ConfigDict


class OlxDataBase(BaseModel):
    id: int | None = None
    seller_name: str | None = None
    registration_date: str | None = None
    last_login: str | None
    url: str | None = None
    title: str | None = None
    image_urls: list[str] | None = None
    price: str | None = None
    created_at: str | None = None
    attributes: list[str] | None = None
    description: str | None = None
    product_id: str | None = None

    model_config = ConfigDict(from_attributes=True)
