from fastapi import APIRouter, Depends
from .. import dependencies
from sqlmodel import Session, select
from ..repository.models import model

router = APIRouter(
    tags=['Brand']
)


@router.get('/')
async def get_all_brands(session: Session = Depends(dependencies.get_session)):
    return session.exec(
        select(model.Brand)
    ).all()
