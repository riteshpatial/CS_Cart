from fastapi import APIRouter, HTTPException
from app.services.co2_engine import calculate_co2
from app.db.database import SessionLocal
from app.db import models

router = APIRouter(prefix="/products", tags=["Products"])


# =========================================================
# 1️⃣ PRODUCT ECO CARD (for product page badge)
# =========================================================
@router.get("/{product_id}/eco")
def get_product_eco(product_id: str):
    try:
        result = calculate_co2(product_id)

        return {
            "product_id": product_id,
            "co2_total_kg": result["co2_total_kg"],
            "eco_score": result["eco_score"],
            "eco_badge": result["eco_badge"],
            "confidence_score": result["confidence_score"],
            "category_comparison": result["category_comparison"]
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================================
# 2️⃣ ECO ALTERNATIVES ONLY
# =========================================================
@router.get("/{product_id}/eco-alternatives")
def get_eco_alternatives(product_id: str):
    try:
        result = calculate_co2(product_id)

        return {
            "product_id": product_id,
            "eco_alternatives": result["eco_alternatives"]
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================================
# 3️⃣ FULL ECO REPORT (admin / dashboards / AI)
# =========================================================
@router.get("/{product_id}/eco-report")
def get_full_eco_report(product_id: str):
    db = SessionLocal()

    try:
        product = db.query(models.Product).filter(
            models.Product.item_id == product_id
        ).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        eco = calculate_co2(product_id)

        return {
            "product": {
                "item_id": product.item_id,
                "category_code": product.category_code,
                "estimated_weight_g": product.estimated_weight_g,
                "shipping_mode": product.shipping_mode,
                "shipping_distance_km": product.shipping_distance_km
            },
            "eco_report": eco
        }

    finally:
        db.close()
