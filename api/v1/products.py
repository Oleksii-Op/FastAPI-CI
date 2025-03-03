from typing import Annotated, Sequence

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy import select, ScalarResult

from api.dependencies import (
    get_current_superuser,
    SessionGetter,
    get_product_by_id_dep,
    get_manufacturer_by_id_dep,
)
from core.models import Product, Manufacturer
from core.schemas import UserPublic
from core.schemas.product import ProductBase, ProductView, ProductUpdate
import logging

router = APIRouter(
    tags=["Products"],
)

logger = logging.getLogger(__name__)


@router.get(
    "/all",
    response_model=list[ProductView],
    status_code=status.HTTP_200_OK,
)
def get_all_products(
    session: SessionGetter,
) -> Sequence[Product]:
    stmt = select(Product).order_by(Product.name)
    result: ScalarResult[Product] = session.scalars(stmt)
    products: Sequence[Product] = result.all()
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
    product: Annotated[
        Product,
        Depends(get_product_by_id_dep),
    ],
) -> Product | None:
    return product


@router.patch(
    "/{product_id}",
    response_model=ProductView,
    status_code=status.HTTP_200_OK,
)
def update_product(
    session: SessionGetter,
    model_update: ProductUpdate,
    superuser: Annotated[
        UserPublic,
        Depends(get_current_superuser),
    ],
    product: Annotated[
        Product,
        Depends(get_product_by_id_dep),
    ],
):
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
    session: SessionGetter,
    superuser: Annotated[
        UserPublic,
        Depends(get_current_superuser),
    ],
    product: Annotated[
        Product,
        Depends(get_product_by_id_dep),
    ],
):
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
    session: SessionGetter,
    product: ProductBase,
    superuser: Annotated[
        UserPublic,
        Depends(get_current_superuser),
    ],
    manufacturer: Annotated[
        Manufacturer,
        Depends(get_manufacturer_by_id_dep),
    ],
):
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
