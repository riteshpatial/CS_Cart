from fastapi import APIRouter, HTTPException
from app.schemas.co2 import CO2Request, CO2Response
from app.services.co2_engine import calculate_co2

router = APIRouter(prefix="/co2", tags=["CO2"])

@router.post("/calculate", response_model=CO2Response)
def calculate(payload: CO2Request):
    try:
        return calculate_co2(payload.product_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
