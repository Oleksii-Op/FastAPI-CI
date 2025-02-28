from typing import Annotated, Sequence
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, ScalarResult
from starlette import status
from sqlalchemy.orm import Session

from api.dependencies import get_current_superuser
from core.get_db import get_db
from core.models.manufacturer import Manufacturer
from core.schemas import UserPublic

from core.schemas.manufacturer import (
    ManufacturerBase,
    ManufacturerView,
    ManufacturerUpdate,
)

router = APIRouter(
    prefix="/manufacturers",
    tags=["Manufacturers"],
)


@router.get(
    "/all",
    response_model=list[ManufacturerBase],
    status_code=status.HTTP_200_OK,
)
def get_all_manufacturers(
    session: Annotated[
        Session,
        Depends(get_db.session_getter),
    ],
) -> Sequence[Manufacturer] | None:
    stmt = select(Manufacturer)
    result: ScalarResult[Manufacturer] | None = session.scalars(stmt)
    manufacturers: Sequence[Manufacturer] | None = result.all()
    if not manufacturers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No manufacturers found",
        )
    return manufacturers


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


@router.patch(
    "/{manufacturer_id}",
    response_model=ManufacturerBase,
    status_code=200,
)
def update_manufacturer(
    session: Annotated[
        Session,
        Depends(get_db.session_getter),
    ],
    manufacturer_id: int,
    model_update: ManufacturerUpdate,
    superuser: UserPublic = Depends(get_current_superuser),
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
    for field, value in model_update.model_dump(exclude_unset=True).items():
        setattr(manufacturer, field, value)
    session.commit()
    session.refresh(manufacturer)
    logging.warning(
        "User id: %s username: %s has updated manufacturer id: %s",
        superuser.id,
        superuser.username,
        manufacturer.id,
    )
    return manufacturer


@router.delete(
    "/{manufacturer_id}",
    status_code=204,
)
def delete_manufacturer(
    session: Annotated[
        Session,
        Depends(get_db.session_getter),
    ],
    manufacturer_id: int,
    superuser: UserPublic = Depends(get_current_superuser),
) -> None:
    manufacturer: Manufacturer | None = session.get(
        Manufacturer,
        manufacturer_id,
    )
    if not manufacturer:
        raise HTTPException(
            status_code=404,
            detail="Manufacturer not found",
        )
    session.delete(manufacturer)
    session.commit()
    logging.warning(
        "User id: %s username: %s has deleted manufacturer id: %s",
        superuser.id,
        superuser.username,
        manufacturer.id,
    )


@router.post(
    "/create",
    response_model=ManufacturerBase,
    status_code=201,
)
def create_manufacturer(
    session: Annotated[
        Session,
        Depends(get_db.session_getter),
    ],
    manufacturer: ManufacturerBase,
    superuser: UserPublic = Depends(get_current_superuser),
):
    obj_in = Manufacturer(
        name=manufacturer.name,
    )
    session.add(obj_in)
    session.commit()
    session.refresh(obj_in)
    logging.info(
        "User (id=%r,username=%r) has created %r id=%r",
        superuser.id,
        superuser.username,
        obj_in.__class__.__name__,
        obj_in.id,
    )
    return obj_in
