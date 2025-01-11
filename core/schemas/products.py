from pydantic import BaseModel


class SellerBase(BaseModel):
    name: str
    rating: str | None = None
    registration_date: str
    last_login: str
    phone_number: str | None = None


class ProductBase(BaseModel):
    url: str
    title: str
    picture: str | None
    price: float
    attributes: str | None
    description: str | None
    locations: str | None
    product_id: str
    viewed: int
    seller: SellerBase
