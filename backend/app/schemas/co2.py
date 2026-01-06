from pydantic import BaseModel
from typing import List, Dict


class Material(BaseModel):
    name: str
    share: float   # value between 0 and 1


class Shipping(BaseModel):
    mode: str      # sea / air / rail
    distance_km: float


class CO2Request(BaseModel):
    item_id: str
    category_code: str
    weight_grams: float
    materials: List[Material]
    shipping: Shipping


class CO2Response(BaseModel):
    co2_total_kg: float
    breakdown: Dict[str, float]
