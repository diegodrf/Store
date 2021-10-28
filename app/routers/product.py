import datetime

from fastapi import APIRouter, Depends, status, HTTPException
from .. import dependencies
from sqlmodel import Session, select
from ..repository.models import model
from typing import List
from uuid import UUID
from datetime import datetime, date, timedelta

router = APIRouter(
    tags=['Product']
)


@router.get('/', response_model=List[model.ProductBasicWithBrandResponse])
async def get_all_products(session: Session = Depends(dependencies.get_session)):
    result = session.exec(
        select(
            model.Product.id,
            model.Product.name,
            model.Product.description,
            model.Brand.name.label('brand')
        ).join(
            model.Brand
        ).where(
            model.Product.deleted_at == None
        )
    ).all()
    return result


@router.get('/{product_id}', response_model=model.ProductDetailedResponse)
async def get_product_by_id(product_id: UUID, session: Session = Depends(dependencies.get_session)):
    product = session.exec(
        select(
            model.Product
        ).where(
            model.Product.id == product_id,
            model.Product.deleted_at == None
        )
    ).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found.')
    return product


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=model.ProductDetailedResponse)
async def create_product(
        product_request: model.ProductCreateRequest,
        session: Session = Depends(dependencies.get_session)
):
    product = model.Product.from_orm(product_request)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@router.put('/{product_id}', status_code=status.HTTP_200_OK, response_model=model.ProductDetailedResponse)
async def update_product(
        product_id: UUID,
        product_request: model.ProductUpdateRequest,
        session: Session = Depends(dependencies.get_session)
):
    product = session.exec(
        select(
            model.Product
        ).where(
            model.Product.id == product_id,
            model.Product.deleted_at == None
        )
    ).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found.')

    for key, value in product_request.dict().items():
        setattr(product, key, value)

    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_product(product_id: UUID, session: Session = Depends(dependencies.get_session)):
    product = session.exec(
        select(
            model.Product
        ).where(
            model.Product.id == product_id,
            model.Product.deleted_at == None
        )
    ).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found.')
    product.deleted_at = datetime.utcnow()
    session.add(product)
    session.commit()


@router.post('/{product_id}/prices', status_code=status.HTTP_201_CREATED, response_model=model.ProductDetailedResponse)
async def create_product_price(
        product_id: UUID,
        price_request: model.PriceCreateOrUpdateRequest,
        session: Session = Depends(dependencies.get_session)
):
    if price_request.initial_validity_date <= date.today():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Initial validity date must a future date.'
        )

    product = session.exec(
        select(
            model.Product
        ).where(
            model.Product.id == product_id,
            model.Product.deleted_at == None
        )
    ).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found.')

    price = model.Price(**price_request.dict(), product_id=product_id)

    if product.prices:
        current_price = session.exec(
            select(
                model.Price
            ).join(
                model.Product
            ).where(
                model.Price.product_id == product_id,
                model.Price.final_validity_date == None,
                model.Product.deleted_at == None,
            )
        ).one()

        if price_request.initial_validity_date <= current_price.initial_validity_date:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Initial validity date must a future date')

        current_price.final_validity_date = price_request.initial_validity_date - timedelta(1)
        session.add(current_price)

    product.prices.append(price)
    session.add(product)

    session.commit()
    session.refresh(product)

    return product