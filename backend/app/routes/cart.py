from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.db.database import get_db
from app.db.models import EventLog
from app.services.ai_service import generate_ai_response

router = APIRouter(prefix="/cart", tags=["Cart Impact"])


@router.post("/impact")
def calculate_cart_impact(
    payload: Dict[str, str],
    db: Session = Depends(get_db)
):
    """
    Calculate total CO2 impact for user's cart
    """

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")

    # -------------------------------------------------
    # Fetch latest ADD_TO_CART + PRODUCT_VIEW events
    # -------------------------------------------------
    events = (
        db.query(EventLog)
        .filter(
            EventLog.user_id == user_id,
            EventLog.event.in_(["product_view", "add_to_cart"])
        )
        .order_by(EventLog.created_at.desc())
        .all()
    )

    if not events:
        return {
            "user_id": user_id,
            "total_co2_kg": 0,
            "items": [],
            "ai_result": {
                "type": "empty_cart",
                "message": "No products in cart"
            }
        }

    # -------------------------------------------------
    # Aggregate CO2
    # -------------------------------------------------
    total_co2 = 0
    items = []

    for e in events:
        if e.co2_data:
            co2_val = e.co2_data.get("co2_total_kg", 0)
            total_co2 += co2_val

            items.append({
                "product_id": e.product_id,
                "category": e.category_code,
                "co2_kg": co2_val
            })

    # -------------------------------------------------
    # AI Summary
    # -------------------------------------------------
    ai_result = generate_ai_response(
        event="cart_impact",
        details=f"""
        user_id: {user_id}
        total_items: {len(items)}
        total_co2: {round(total_co2, 2)} kg
        """
    )

    return {
        "user_id": user_id,
        "total_co2_kg": round(total_co2, 2),
        "items": items,
        "ai_result": ai_result
    }
