# CS-Cart Sustainability AI Engine

Ek FastAPI-based backend engine jo CS-Cart e-commerce platform ke saath integrate hota hai. Yeh system har product ka **CO2 footprint calculate karta hai**, **eco-friendly alternatives suggest karta hai**, aur **AI-powered product recommendations** deta hai — sab kuch real-time mein.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [How It Works](#how-it-works)
- [Database Models](#database-models)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Server Chalana](#server-chalana)
- [API Endpoints](#api-endpoints)
- [Eco Score System](#eco-score-system)
- [AI Mode](#ai-mode)

---

## Project Overview

Yeh project ek **sustainability intelligence layer** hai jo CS-Cart store ke upar baithta hai. Jab koi user:

- **Product dekhe** → CO2 footprint calculate hota hai + similar products suggest hote hain
- **Search kare** → AI recommended products dikhata hai
- **Cart mein add kare** → Low-CO2 eco-friendly alternatives suggest hoti hain
- **Cart impact dekhe** → User ke poore cart ka total CO2 footprint calculate hota hai

---

## Project Structure

```
CS_Cart/
│
├── backend/
│   ├── app/
│   │   ├── main.py                   # FastAPI app entry point
│   │   ├── config.py                 # Settings (AI_MODE, OpenAI key)
│   │   │
│   │   ├── routes/
│   │   │   ├── events.py             # CS-Cart events (product_view, search, add_to_cart)
│   │   │   ├── co2.py                # Standalone CO2 calculation
│   │   │   ├── cart.py               # Cart-level CO2 aggregation
│   │   │   └── products.py           # Product eco card, alternatives, full report
│   │   │
│   │   ├── services/
│   │   │   ├── co2_engine.py         # Core CO2 calculation engine
│   │   │   ├── ai_service.py         # AI response generator (demo mode)
│   │   │   ├── openai_service.py     # OpenAI integration (production)
│   │   │   ├── event_store.py        # Event save to DB
│   │   │   └── product_service.py    # Product DB helpers
│   │   │
│   │   ├── db/
│   │   │   ├── database.py           # SQLAlchemy engine + session
│   │   │   └── models.py             # DB table definitions
│   │   │
│   │   ├── schemas/
│   │   │   ├── co2.py                # CO2 request/response schema
│   │   │   ├── ai.py                 # AI response schema
│   │   │   ├── cscart.py             # CS-Cart event schema
│   │   │   └── events.py             # Event log schema
│   │   │
│   │   ├── models/
│   │   │   └── request_models.py     # Pydantic request models
│   │   │
│   │   ├── data/
│   │   │   ├── category_baseline.py  # Category CO2 baseline data (ADEME)
│   │   │   ├── material_impact.py    # Material carbon/water/waste impact data
│   │   │   └── transport_factors.py  # Shipping mode CO2 factors
│   │   │
│   │   └── utils/
│   │       └── prompt_builder.py     # AI prompt construction utility
│   │
│   ├── product_service.py            # Standalone product service
│   └── requirements.txt              # Python dependencies
│
└── events.db                         # SQLite database (auto-created)
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend Framework | FastAPI (Python) |
| Database | SQLite (via SQLAlchemy) |
| AI Integration | OpenAI API (demo mode by default) |
| Data Validation | Pydantic |
| Server | Uvicorn (ASGI) |
| Config | python-dotenv |

---

## How It Works

```
CS-Cart Store
      |
      | POST /events/cscart
      ↓
  FastAPI Engine
      |
      ├── CO2 Engine ─────────────────────────────────────────────────┐
      │   ├── Product weight × Material impact (carbon/water/waste)   │
      │   ├── Shipping mode × Distance × Transport factor             │
      │   └── Category baseline (ADEME data)                          │
      │                                                               ↓
      └── AI Service                                        CO2 Result + Eco Score
          ├── Demo Mode → Hardcoded smart responses
          └── Prod Mode → OpenAI GPT responses
```

**CO2 Formula:**
```
Total CO2 = Material Carbon + Transport CO2 + Category Baseline
```

---

## Database Models

| Table | Description |
|-------|-------------|
| `products` | Product info (weight, shipping mode, distance, category) |
| `material_impacts` | Har material ka carbon/water/waste factor per kg |
| `category_baselines` | Category-wise average CO2 (ADEME source) |
| `transport_factors` | Shipping mode wise CO2 per tonne-km |
| `event_logs` | Har CS-Cart event ka log (CO2 + AI result JSON) |
| `product_materials` | Product ki material composition (material + share %) |

---

## Setup & Installation

### Step 1 — Repo Clone Karo

```bash
git clone https://github.com/riteshpatial/CS_Cart
cd CS_Cart/backend
```

### Step 2 — Virtual Environment Banao (Optional but Recommended)

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### Step 3 — Dependencies Install Karo

```bash
pip install -r requirements.txt
```

Dependencies:
- `fastapi`
- `uvicorn`
- `python-dotenv`
- `openai`
- `sqlalchemy` *(manually add if missing)*

---

## Environment Variables

`backend/` folder mein `.env` file banao:

```env
AI_MODE=demo
OPENAI_API_KEY=your_openai_api_key_here
```

| Variable | Values | Description |
|----------|--------|-------------|
| `AI_MODE` | `demo` / `prod` | Demo = hardcoded responses, Prod = real OpenAI |
| `OPENAI_API_KEY` | OpenAI key | Sirf `prod` mode mein zaroori |

---

## Server Chalana

```bash
cd CS_Cart/backend
uvicorn app.main:app --reload
```

Server chalega: `http://127.0.0.1:8000`

Interactive API docs: `http://127.0.0.1:8000/docs`

---

## API Endpoints

### Health Check

```
GET /health
```
```json
{ "status": "running", "service": "AI + CO2 Engine" }
```

---

### CS-Cart Event Receive Karo

```
POST /events/cscart
```

**Product View:**
```json
{
  "event": "product_view",
  "user_id": "user_123",
  "product_id": "prod_456"
}
```

**Search:**
```json
{
  "event": "search",
  "user_id": "user_123",
  "search_query": "eco friendly laptop"
}
```

**Add to Cart:**
```json
{
  "event": "add_to_cart",
  "user_id": "user_123",
  "product_id": "prod_456"
}
```

---

### CO2 Calculate Karo (Standalone)

```
POST /co2/calculate
```
```json
{ "product_id": "prod_456" }
```

**Response:**
```json
{
  "co2_total_kg": 12.5,
  "eco_score": "C",
  "eco_badge": {
    "label": "C",
    "color": "#FFC107",
    "text": "Average environmental impact"
  },
  "category_comparison": {
    "category_avg_kg": 10.0,
    "difference_kg": 2.5
  },
  "eco_alternatives": [...],
  "water_l_total": 45.2,
  "waste_kg_total": 0.8,
  "confidence_score": 0.9,
  "breakdown": {
    "materials_co2_kg": 8.0,
    "transport_co2_kg": 2.0,
    "category_baseline_kg": 2.5
  }
}
```

---

### Cart ka Total CO2

```
POST /cart/impact
```
```json
{ "user_id": "user_123" }
```

---

### Product Eco Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products/{id}/eco` | Eco badge + score |
| GET | `/products/{id}/eco-alternatives` | Low-CO2 alternatives |
| GET | `/products/{id}/eco-report` | Full detailed eco report |

---

## Eco Score System

CO2 value ke hisaab se product ko grade milti hai:

| Score | CO2 Range | Color | Meaning |
|-------|-----------|-------|---------|
| **A** | ≤ 5 kg | Dark Green | Excellent environmental performance |
| **B** | 5–10 kg | Green | Good environmental performance |
| **C** | 10–20 kg | Yellow | Average environmental impact |
| **D** | 20–40 kg | Orange | High environmental impact |
| **E** | > 40 kg | Red | Very high environmental impact |

---

## AI Mode

| Mode | Behavior |
|------|----------|
| `demo` | Hardcoded smart responses — no API key needed, testing ke liye |
| `prod` | Real OpenAI GPT responses — `.env` mein `OPENAI_API_KEY` chahiye |

Mode change karne ke liye `.env` mein update karo:
```env
AI_MODE=prod
```

---

## Author

- GitHub: [riteshpatial](https://github.com/riteshpatial)
