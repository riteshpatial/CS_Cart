from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# DB
from app.db.database import engine
from app.db import models

# Routers
from app.routes.events import router as events_router
from app.routes.co2 import router as co2_router
from app.routes.cart import router as cart_router
from app.routes.products import router as products_router   # ✅ ADD THIS

# -------------------------------------------------
# Create DB tables
# -------------------------------------------------
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CS-Cart Sustainability AI Engine",
    description="AI + CO2 calculation engine for CS-Cart integration",
    version="1.0.0"
)

# -------------------------------------------------
# CORS (CS-Cart + Frontend)
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Static files + Demo page
# -------------------------------------------------
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", include_in_schema=False)
def demo():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

# -------------------------------------------------
# Health Check
# -------------------------------------------------
@app.get("/health")
def health():
    return {"status": "running", "service": "AI + CO2 Engine"}

# -------------------------------------------------
# API Routers
# -------------------------------------------------

# CS-Cart → Event-driven AI + CO2
app.include_router(events_router)

# Standalone CO2 calculation
app.include_router(co2_router)

# Cart-level CO2 aggregation
app.include_router(cart_router)

# ✅ Product intelligence APIs
app.include_router(products_router)
