from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from app.db.database import Base
# -------------------------------------------------
# PRODUCTS (from client item sheets)
# -------------------------------------------------

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(String, unique=True, index=True)
    category_code = Column(String, index=True)
    estimated_weight_g = Column(Float)
    shipping_mode = Column(String)
    shipping_distance_km = Column(Float)


# -------------------------------------------------
# MATERIAL IMPACT DATA
# -------------------------------------------------

class MaterialImpact(Base):
    __tablename__ = "material_impacts"

    id = Column(Integer, primary_key=True, index=True)
    material = Column(String, unique=True, index=True)

    carbon_kgco2e_per_kg = Column(Float)
    water_m3_per_kg = Column(Float)
    waste_kg_per_kg = Column(Float)

    source = Column(String)
    source_url = Column(String)


# -------------------------------------------------
# CATEGORY BASELINES (ADEME)
# -------------------------------------------------

class CategoryBaseline(Base):
    __tablename__ = "category_baselines"

    id = Column(Integer, primary_key=True, index=True)
    category_code = Column(String, unique=True, index=True)
    category_name = Column(String)

    total_co2e_kg = Column(Float)
    fabrication_total = Column(Float)
    use_phase = Column(Float)
    end_of_life = Column(Float)
    lifespan_years = Column(Float)

    source = Column(String)
    source_url = Column(String)


# -------------------------------------------------
# TRANSPORT FACTORS
# -------------------------------------------------

class TransportFactor(Base):
    __tablename__ = "transport_factors"

    id = Column(Integer, primary_key=True, index=True)
    mode = Column(String, index=True)
    factor_kgco2e_per_tonne_km = Column(Float)
    source = Column(String)
    source_url = Column(String)


# -------------------------------------------------
# EVENT LOGS (CS-Cart analytics + AI memory)
# -------------------------------------------------

class EventLog(Base):
    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True, index=True)

    event = Column(String, index=True)
    user_id = Column(String, index=True)
    product_id = Column(String, nullable=True)
    category_code = Column(String, nullable=True)

    co2_data = Column(JSON, nullable=True)
    ai_result = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

# -------------------------------------------------
# PRODUCT MATERIAL COMPOSITION
# -------------------------------------------------

class ProductMaterial(Base):
    __tablename__ = "product_materials"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(String, index=True)   # FK logically from products.item_id
    material = Column(String, index=True)
    share = Column(Float)
