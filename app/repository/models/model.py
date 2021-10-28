from sqlmodel import SQLModel, Relationship, Field
from datetime import datetime, date, timedelta
from typing import List, Optional
from uuid import uuid4, UUID


class BrandBase(SQLModel):
    name: str = Field(index=True)


class Brand(BrandBase, table=True):
    __tablename__ = 'brands'
    id: Optional[int] = Field(default=None, primary_key=True)
    products: List['Product'] = Relationship(back_populates='brand')


class ProductBase(SQLModel):
    name: str
    description: Optional[str] = Field(default=None)


class Product(ProductBase, table=True):
    __tablename__ = 'products'
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = Field(default=None)
    brand_id: int = Field(foreign_key='brands.id')
    brand: Brand = Relationship(back_populates='products')
    prices: List['Price'] = Relationship(back_populates='product')


class PriceBase(SQLModel):
    initial_validity_date: date = Field(default_factory=date.today)
    amount: int


class Price(PriceBase, table=True):
    __tablename__ = 'prices'
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    final_validity_date: Optional[date] = Field(default=None)
    product_id: UUID = Field(foreign_key='products.id')
    product: Product = Relationship(back_populates='prices')


"""
Below start the Response Models block
"""

# Basic Responses


class BrandBasicResponse(BrandBase):
    id: int


class ProductBasicResponse(ProductBase):
    id: UUID


class PriceResponse(PriceBase):
    id: UUID
    final_validity_date: Optional[date] = None

# Complex Responses


class ProductBasicWithBrandResponse(ProductBase):
    id: UUID
    brand: str


class ProductDetailedResponse(ProductBase):
    id: UUID
    brand: BrandBasicResponse
    prices: List[PriceResponse]


class BrandDetailedResponse(BrandBase):
    id: int
    products: List[ProductBasicResponse]


"""
Below start the Request Models block
"""


class BrandCreateRequest(BrandBase):
    pass


class BrandUpdateRequest(BrandBase):
    pass


class ProductCreateRequest(ProductBase):
    brand_id: int


class ProductUpdateRequest(ProductBase):
    brand_id: int


class PriceCreateOrUpdateRequest(PriceBase):
    pass
