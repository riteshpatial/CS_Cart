from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.services.ai_service import generate_ai_response
from app.services.co2_engine import calculate_co2
from app.services.event_store import save_event

router = APIRouter(prefix="/events", tags=["Events"])


# -------------------------
# Schema (CS-Cart payload)
# -------------------------

class CSCartEvent(BaseModel):
    event: str                 # product_view | search | add_to_cart
    user_id: str
    product_id: Optional[str] = None
    search_query: Optional[str] = None


# -------------------------
# Event Endpoint
# -------------------------

@router.post("/cscart")
def receive_cscart_event(payload: CSCartEvent):
    """
    Main CS-Cart → AI Engine endpoint

    Events:
    - product_view → CO2 + AI (DB driven)
    - search → AI only
    - add_to_cart → AI eco alternatives
    """

    response = {
        "status": "event processed",
        "event": payload.event,
        "user_id": payload.user_id,
        "product_id": payload.product_id
    }

    co2_result = None
    ai_result = None

    # ==================================================
    # PRODUCT VIEW → CO2 + AI
    # ==================================================
    if payload.event == "product_view":

        if not payload.product_id:
            raise HTTPException(
                status_code=400,
                detail="product_id required for product_view"
            )

        # 🔥 HARD TYPE SAFETY (this killed your bug)
        if not isinstance(payload.product_id, str):
            raise HTTPException(
                status_code=400,
                detail=f"product_id must be string, got {type(payload.product_id)}"
            )

        try:
            # ✅ ONLY STRING GOES INTO ENGINE
            co2_result = calculate_co2(payload.product_id)
            response["co2"] = co2_result

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"CO2 calculation failed: {str(e)}"
            )

        ai_result = generate_ai_response(
            event="product_view",
            details={
                "product_id": payload.product_id,
                "co2": co2_result
            }
        )

        response["ai_result"] = ai_result

    # ==================================================
    # SEARCH → AI ONLY
    # ==================================================
    elif payload.event == "search":

        if not payload.search_query:
            raise HTTPException(
                status_code=400,
                detail="search_query required for search event"
            )

        ai_result = generate_ai_response(
            event="search",
            details={
                "search_query": payload.search_query
            }
        )

        response["ai_result"] = ai_result

    # ==================================================
    # ADD TO CART → AI ONLY
    # ==================================================
    elif payload.event == "add_to_cart":

        if not payload.product_id:
            raise HTTPException(
                status_code=400,
                detail="product_id required for add_to_cart"
            )

        ai_result = generate_ai_response(
            event="add_to_cart",
            details={
                "product_id": payload.product_id,
                "intent": "suggest eco-friendly alternatives"
            }
        )

        response["ai_result"] = ai_result

    # ==================================================
    # UNSUPPORTED EVENT
    # ==================================================
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported event type: {payload.event}"
        )

    # ==================================================
    # STORE EVENT (ALL EVENTS)
    # ==================================================
    save_event(
        event=payload.event,
        user_id=payload.user_id,
        product_id=payload.product_id,
        co2_data=co2_result,
        ai_result=ai_result
    )
    


    return response
