from pydantic import BaseModel
from typing import List


class MaterialInput(BaseModel):
    name: str
    share: float


class ShippingInput(BaseModel):
    mode: str
    distance_km: float


class ProductViewEvent(BaseModel):
    user_id: str
    product_id: str
    category_code: str
    weight_grams: float
    materials: List[MaterialInput]
    shipping: ShippingInput
    
class CSCartEvent(BaseModel):
    event: str                  # product_view, add_to_cart, search
    user_id: str
    product_id: Optional[str] = None
    category_code: Optional[str] = None
    search_query: Optional[str] = None