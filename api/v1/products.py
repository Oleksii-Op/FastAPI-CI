from typing import Annotated, Sequence

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, ScalarResult

from api.dependencies import get_current_superuser
from core.models import Product, Manufacturer
from core.schemas import UserPublic
from core.schemas.product import ProductBase, ProductView, ProductUpdate
from core.get_db import get_db
import logging

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

logger = logging.getLogger(__name__)


@router.get(
    "/all",
    response_model=list[ProductView],
    status_code=status.HTTP_200_OK,
)
def get_all_products(
    session: Annotated[
        Session,
        Depends(get_db.session_getter),
    ],
) -> Sequence[Product] | None:
    stmt = select(Product).order_by(Product.name)
    result: ScalarResult[Product] | None = session.scalars(stmt)
    products: Sequence[Product] | None = result.all()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Products not found",
        )
    return products


@router.get(
    "/{product_id}",
    response_model=ProductView,
    status_code=status.HTTP_200_OK,
)
def get_product(
    session: Annotated[
        Session,
        Depends(get_db.session_getter),
    ],
    product_id: int,
) -> Product | None:
    product: Product | None = session.get(
        Product,
        product_id,
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product


@router.patch(
    "/{product_id}",
    response_model=ProductView,
    status_code=status.HTTP_200_OK,
)
def update_product(
    session: Annotated[
        Session,
        Depends(get_db.session_getter),
    ],
    product_id: int,
    model_update: ProductUpdate,
    superuser: UserPublic = Depends(get_current_superuser),
):
    product: Product | None = session.get(
        Product,
        product_id,
    )
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Manufacturer not found",
        )
    for field, value in model_update.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    session.commit()
    session.refresh(product)
    logging.warning(
        "User id: %s username: %s has updated product id: %s",
        superuser.id,
        superuser.username,
        product.id,
    )
    return product


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product(
    session: Annotated[
        Session,
        Depends(get_db.session_getter),
    ],
    product_id: int,
    superuser: UserPublic = Depends(get_current_superuser),
):
    product: Product | None = session.get(
        Product,
        product_id,
    )
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Manufacturer not found",
        )
    session.delete(product)
    session.commit()
    logging.warning(
        "User id: %s username: %s has deleted product id: %s",
        superuser.id,
        superuser.username,
        product.id,
    )


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductView,
)
def create_product(
    session: Annotated[
        Session,
        Depends(get_db.session_getter),
    ],
    manufacturer_id: int,
    product: ProductBase,
    superuser: UserPublic = Depends(get_current_superuser),
):
    manufacturer = session.get(Manufacturer, manufacturer_id)
    if not manufacturer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manufacturer not found",
        )
    obj_in = Product(
        name=product.name,
        year=product.year,
        cpu=product.cpu,
    )
    manufacturer.products.append(obj_in)
    session.add(manufacturer)
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
