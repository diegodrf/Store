from fastapi import APIRouter, Depends, status, HTTPException
from .. import dependencies
from sqlmodel import Session, select
from ..repository.models import model
from typing import List

router = APIRouter(
    tags=['Brand']
)


@router.get('/', response_model=List[model.BrandBasicResponse])
async def get_all_brands(session: Session = Depends(dependencies.get_session)):
    return session.exec(
        select(model.Brand)
    ).all()


@router.get('/{brand_id}', response_model=model.BrandDetailedResponse)
async def get_brand_by_id(brand_id: int, session: Session = Depends(dependencies.get_session)):
    brand = session.exec(
        select(
            model.Brand
        ).join(
            model.Product
        ).where(
            model.Brand.id == brand_id,
            model.Product.deleted_at == None
        )
    ).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Brand not found.')
    return brand


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=model.BrandBasicResponse)
async def create_brand(brand_request: model.BrandCreateRequest, session: Session = Depends(dependencies.get_session)):
    brand = model.Brand.from_orm(brand_request)
    session.add(brand)
    session.commit()
    session.refresh(brand)
    return brand


@router.put('/{brand_id}', status_code=status.HTTP_200_OK, response_model=model.BrandBasicResponse)
async def update_brand(
        brand_id: int,
        brand_request: model.BrandUpdateRequest,
        session: Session = Depends(dependencies.get_session)
):
    brand = session.get(model.Brand, brand_id)
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Brand not found.')
    for key, value in brand_request.dict().items():
        setattr(brand, key, value)
    session.add(brand)
    session.commit()
    session.refresh(brand)
    return brand


@router.delete('/{brand_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_brand(brand_id: int, session: Session = Depends(dependencies.get_session)):
    brand = session.get(model.Brand, brand_id)
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Brand not found.')
    session.delete(brand)
    session.commit()
