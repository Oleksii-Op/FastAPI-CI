from typing import Annotated
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from api.dependencies import get_current_active_auth_user, get_current_superuser
from core.get_db import get_db
from core.models.manufacturer import Manufacturer
from core.schemas import UserPublic

from core.schemas.manufacturer import ManufacturerBase, ManufacturerView

router = APIRouter(prefix="/manufacturers", tags=["Manufacturers"])


@router.get(
    "/{manufacturer_id}",
    response_model=ManufacturerView,
    status_code=200,
)
def get_manufacturer(
    session: Annotated[
        Session,
        Depends(get_db.session_getter),
    ],
    manufacturer_id: int,
) -> Manufacturer:
    manufacturer: Manufacturer | None = session.get(
        Manufacturer,
        manufacturer_id,
    )
    if not manufacturer:
        raise HTTPException(
            status_code=404,
            detail="Manufacturer not found",
        )
    return manufacturer


@router.post(
    "/create",
    response_model=ManufacturerView,
    status_code=201,
)
def create_manufacturer(
    session: Annotated[
        Session,
        Depends(get_db.session_getter),
    ],
    manufacturer: ManufacturerBase,
    # user: UserPublic = Depends(get_current_superuser),
):
    obj_in = Manufacturer(
        name=manufacturer.name,
    )
    session.add(obj_in)
    session.commit()
    session.refresh(obj_in)
    # logging.info(
    #     "User (id=%r,username=%r) has created %r id=%r",
    #     user.id,
    #     user.username,
    #     obj_in.__class__.__name__,
    #     obj_in.id,
    # )
    return obj_in
