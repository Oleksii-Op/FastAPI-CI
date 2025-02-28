from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class ProductBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
    )
    year: int = Field(
        ge=1,
        le=datetime.now().year,
    )
    cpu: str
    model_config = ConfigDict(
        from_attributes=True,
    )


class ProductView(ProductBase):
    id: int
    manufacturer_id: int
    created_at: datetime
    updated_at: datetime


class ProductUpdate(ProductBase):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    year: int | None = Field(
        default=None,
        ge=1,
        le=datetime.now().year,
    )
    cpu: str | None = None