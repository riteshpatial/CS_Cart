from sqlalchemy.orm import Session
from app.models.models import Product, MaterialImpact, CategoryBaseline, TransportFactor
from app.db.database import SessionLocal


def get_product_with_data(product_id: str, db: Session):
    product = db.query(Product).filter(Product.item_id == product_id).first()
    if not product:
        return None

    return product


def get_material_impacts(db: Session):
    rows = db.query(MaterialImpact).all()
    return {
        row.material.lower(): {
            "carbon": row.carbon_kgco2e_per_kg,
            "water": row.water_m3_per_kg,
            "waste": row.waste_kg_per_kg
        }
        for row in rows
    }


def get_category_baselines(db: Session):
    rows = db.query(CategoryBaseline).all()
    return {row.category_code: row.total_co2e_kg for row in rows}


def get_transport_factors(db: Session):
    rows = db.query(TransportFactor).all()
    return {row.mode.lower(): row.factor_kgco2e_per_tonne_km for row in rows}
