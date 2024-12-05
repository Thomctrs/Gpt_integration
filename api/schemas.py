from pydantic import BaseModel
from typing import List, Optional



class ImageBase(BaseModel):
    image_url: str
    is_primary: bool = False

class WatchBase(BaseModel):
    model: str
    price: float
    description: Optional[str] = None
    technical_details: Optional[str] = None
    reference_number: Optional[str] = None
    movement_type: Optional[str] = None
    case_material: Optional[str] = None
    water_resistance: Optional[int] = None
    diameter: Optional[float] = None
    stock_quantity: Optional[int] = None

class WatchCreate(WatchBase):
    brand_id: int
    collection_id: int

class WatchResponse(WatchBase):
    watch_id: int
    brand_name: str
    collection_name: str
    images: List[ImageBase] = []

    class Config:
        orm_mode = True

class BrandResponse(BaseModel):
    brand_id: int
    name: str
    description: Optional[str] = None
    founded_year: Optional[int] = None
    country: Optional[str] = None