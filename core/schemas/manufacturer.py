from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ManufacturerBase(BaseModel):
    name: str
    model_config = ConfigDict(
        from_attributes=True,
    )

class ManufacturerView(ManufacturerBase):
    id: int
    created_at: datetime
    updated_at: datetime