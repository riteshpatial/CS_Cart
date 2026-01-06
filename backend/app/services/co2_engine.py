from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db import models


# -------------------------------------------------
# HELPERS
# -------------------------------------------------

def eco_score_from_co2(value: float):
    if value <= 5:
        return "A"
    elif value <= 10:
        return "B"
    elif value <= 20:
        return "C"
    elif value <= 40:
        return "D"
    else:
        return "E"


def eco_badge_from_score(score: str):
    badges = {
        "A": {"color": "#1B5E20", "text": "Excellent environmental performance"},
        "B": {"color": "#4CAF50", "text": "Good environmental performance"},
        "C": {"color": "#FFC107", "text": "Average environmental impact"},
        "D": {"color": "#FF9800", "text": "High environmental impact"},
        "E": {"color": "#B71C1C", "text": "Very high environmental impact"},
    }

    return {
        "label": score,
        "color": badges[score]["color"],
        "text": badges[score]["text"]
    }


# -------------------------------------------------
# INTERNAL ENGINE (NO SESSION CREATION HERE)
# -------------------------------------------------

def _calculate_from_product(product, db: Session):

    confidence = 1.0
    weight_kg = product.estimated_weight_g / 1000

    # ---------- CATEGORY ----------
    category = db.query(models.CategoryBaseline).filter(
        models.CategoryBaseline.category_code == product.category_code
    ).first()

    if category:
        category_baseline = category.total_co2e_kg
        category_avg = category.total_co2e_kg
    else:
        confidence -= 0.3
        category_baseline = 0
        category_avg = None

    # ---------- MATERIALS ----------
    materials = db.query(models.ProductMaterial).filter(
        models.ProductMaterial.item_id == product.item_id
    ).all()

    if not materials:
        confidence -= 0.2

    material_carbon = 0
    material_water = 0
    material_waste = 0

    for m in materials:
        impact = db.query(models.MaterialImpact).filter(
            models.MaterialImpact.material == m.material.lower()
        ).first()

        if not impact:
            confidence -= 0.1
            continue

        share_weight = weight_kg * m.share
        material_carbon += share_weight * impact.carbon_kgco2e_per_kg
        material_water += share_weight * impact.water_m3_per_kg * 1000
        material_waste += share_weight * impact.waste_kg_per_kg

    # ---------- TRANSPORT ----------
    transport = db.query(models.TransportFactor).filter(
        models.TransportFactor.mode == product.shipping_mode.lower()
    ).first()

    if not transport:
        confidence -= 0.2
        transport_co2 = 0
    else:
        transport_co2 = (
            (weight_kg / 1000)
            * product.shipping_distance_km
            * transport.factor_kgco2e_per_tonne_km
        )

    # ---------- TOTAL ----------
    total_co2 = material_carbon + transport_co2 + category_baseline
    eco_score = eco_score_from_co2(total_co2)
    eco_badge = eco_badge_from_score(eco_score)
    vs_category = round(total_co2 - category_avg, 2) if category_avg else None

    return {
        "total": total_co2,
        "eco_score": eco_score,
        "eco_badge": eco_badge,
        "category_avg": category_avg,
        "vs_category": vs_category,
        "material_carbon": material_carbon,
        "material_water": material_water,
        "material_waste": material_waste,
        "transport_co2": transport_co2,
        "category_baseline": category_baseline,
        "confidence": max(round(confidence, 2), 0.3)
    }


# -------------------------------------------------
# ECO ALTERNATIVES ENGINE (NO NEW SESSION)
# -------------------------------------------------

def find_eco_alternatives(product, base_total, db: Session, limit=3):

    candidates = db.query(models.Product).filter(
        models.Product.category_code == product.category_code,
        models.Product.item_id != product.item_id
    ).all()

    alternatives = []

    for p in candidates:
        try:
            r = _calculate_from_product(p, db)

            if r["total"] < base_total:
                alternatives.append({
                    "product_id": p.item_id,
                    "co2_total_kg": round(r["total"], 3),
                    "eco_score": r["eco_score"],
                    "eco_badge": r["eco_badge"]
                })
        except:
            continue

    alternatives.sort(key=lambda x: x["co2_total_kg"])
    return alternatives[:limit]


# -------------------------------------------------
# PUBLIC ENGINE (ONLY PLACE SESSION IS CREATED)
# -------------------------------------------------

def calculate_co2(product_id: str):

    if not isinstance(product_id, str):
        raise ValueError("product_id must be string")

    db: Session = SessionLocal()

    try:
        product = db.query(models.Product).filter(
            models.Product.item_id == product_id
        ).first()

        if not product:
            raise ValueError("Product not found")

        r = _calculate_from_product(product, db)

        eco_alternatives = find_eco_alternatives(product, r["total"], db)

        return {
            "co2_total_kg": round(r["total"], 3),
            "eco_score": r["eco_score"],
            "eco_badge": r["eco_badge"],

            "category_comparison": {
                "category_avg_kg": r["category_avg"],
                "difference_kg": r["vs_category"]
            },

            "eco_alternatives": eco_alternatives,

            "water_l_total": round(r["material_water"], 2),
            "waste_kg_total": round(r["material_waste"], 3),
            "confidence_score": r["confidence"],

            "breakdown": {
                "materials_co2_kg": round(r["material_carbon"], 3),
                "transport_co2_kg": round(r["transport_co2"], 3),
                "category_baseline_kg": round(r["category_baseline"], 3),
                "water_l": round(r["material_water"], 2),
                "waste_kg": round(r["material_waste"], 3)
            }
        }

    finally:
        db.close()
