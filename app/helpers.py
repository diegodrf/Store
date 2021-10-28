from sqlmodel import SQLModel, Session
from .repository.database import engine
from .repository.models import model


def create_tables_if_not_exists() -> None:
    SQLModel.metadata.create_all(engine)


def drop_tables() -> None:
    SQLModel.metadata.drop_all(engine)


def is_pre_populated() -> bool:
    with Session(engine) as session:
        brand = session.get(model.Brand, 1)
        if brand:
            return True


def pre_populate_database() -> None:
    with Session(engine) as session:
        brand_1 = model.Brand(name='Apple Teste')

        session.add(brand_1)

        product_1 = model.Product(name='Iphone 11', brand=brand_1)
        product_2 = model.Product(name='Iphone 12', brand=brand_1)
        product_3 = model.Product(name='Iphone 7', description='Preto', brand=brand_1)

        session.add(product_1)
        session.add(product_2)
        session.add(product_3)

        session.commit()

