from sqlmodel import SQLModel, Relationship, Field
from datetime import datetime, date
from typing import List, Optional
from uuid import uuid4, UUID


class BrandBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Brand(BrandBase, table=True):
    __tablename__ = 'brands'
    products: List['Product'] = Relationship(back_populates='brand')


class ProductBase(SQLModel):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: Optional[str]


class Product(ProductBase, table=True):
    __tablename__ = 'products'
    created_at: datetime = Field(default_factory=datetime.utcnow)
    brand_id: int = Field(foreign_key='brands.id')
    brand: Brand = Relationship(back_populates='products')
    prices: List['Price'] = Relationship(back_populates='product')


class PriceBase(SQLModel):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    initial_validity_date: datetime = Field(default_factory=datetime.utcnow)
    fina_validity_date: Optional[datetime] = Field(default=None)


class Price(PriceBase, table=True):
    __tablename__ = 'prices'
    created_at: datetime = Field(default_factory=datetime.utcnow)
    product_id: UUID = Field(foreign_key='products.id')
    product: Product = Relationship(back_populates='prices')

