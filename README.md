# 🛵 GigShield — Parametric Income Protection for Gig Delivery Workers

## 📌 Problem Statement

India's platform-based delivery partners (Zomato, Swiggy, Zepto, Amazon, Dunzo, etc.) lose **20–30% of monthly earnings** during external disruptions like extreme weather, flooding, and dangerous pollution levels. They have no financial safety net. When disruption strikes, they bear the full loss alone.

## 🎯 Chosen Persona Segment

**Food Delivery Partners — Zomato / Swiggy**

Rationale: Food delivery riders are the largest and most vulnerable segment. They operate in dense urban zones and are most exposed to rain, flooding, and pollution events that directly halt deliveries.

## 👤 Personas

### Persona 1 — Raju Verma
- **Age:** 28
- **City:** Delhi (Lajpat Nagar / Greater Kailash)
- **Platform:** Swiggy + Zomato
- **Weekly earnings:** ~₹5,500
- **Weekly premium:** ₹38 (High risk zone)
- **Scenario:** Heavy rainfall triggers IMD red alert. GigShield detects trigger, cross-checks GPS inactivity, auto-transfers ₹785 to UPI within 24 hours.

### Persona 2 — Meena Devi
- **Age:** 34
- **City:** Delhi (Dwarka)
- **Platform:** Swiggy
- **Weekly earnings:** ~₹4,750
- **Weekly premium:** ₹35 (Medium risk zone)
- **Scenario:** AQI crosses 400 for 3 days. Partial payout of ₹950 triggered automatically.

### Persona 3 — Arjun Singh
- **Age:** 24
- **City:** Delhi (Karol Bagh)
- **Platform:** Zomato
- **Weekly earnings:** ~₹6,000
- **Weekly premium:** ₹42 (Medium-High risk zone)
- **Scenario:** Unplanned bandh shuts Karol Bagh. GPS confirms inactivity. Full day payout ₹857 triggered.

## ⚙️ Workflow

### Stage 1: Onboarding
1. Worker downloads GigShield app
2. Aadhaar-based KYC verification
3. Selects operating zone and coverage plan
4. Adds UPI ID for payouts
5. Account created, base risk profile generated

### Stage 2: Premium Calculation
1. System retrieves historical disruption data for worker's zone
2. Zone Risk Factor computed from flood history, AQI levels, road closures
3. Base weekly premium set from risk factor
4. ML model adjusts premium week-over-week
5. Worker pays weekly premium upfront
6. 2-week waiting period before first claim eligibility

### Stage 3: Active Coverage
1. Policy live for 7 days from payment
2. App runs in background logging GPS passively
3. No action required from worker

### Stage 4: Trigger Monitoring
1. APIs polled every hour for worker's zone
2. Threshold crossed → worker flagged automatically
3. Fraud checks run in parallel

### Stage 5: Payout
1. Auto-transferred via UPI within 24 hours
2. Worker notified in-app
3. Transaction logged for audit trail

## ⚡ Parametric Triggers

**Environmental**
| Trigger | Source | Threshold |
|---|---|---|
| Extreme Rainfall | IMD Mausam API | Red Alert or > 50mm/hr |
| Flooding | NDMA SACHET API | Active flood alert in district |
| Severe AQI | AQICN API | AQI > 300 sustained 4+ hrs |
| Extreme Heat | Tomorrow.io | Heat index > 45°C for 4+ hrs |

**Social**
| Trigger | Source | Threshold |
|---|---|---|
| Curfew / Bandh | News API / Govt alert feed | Active curfew in district |

## 💰 Weekly Premium Model

**Premium = Base Rate × Zone Risk Factor × Coverage Multiplier**

| Zone Risk Tier | Description | Example Weekly Premium |
|---|---|---|
| Low | Historically safe zone, low AQI, no flood record | ₹25 |
| Medium | Occasional disruptions, moderate AQI | ₹38 |
| High | Frequent floods, high AQI, disaster-prone | ₹55 |

### Example Policies

| Plan | Weekly Premium | Max Weekly Payout | Covers |
|---|---|---|---|
| **Basic** | ₹25 | ₹700 | Extreme rain + flood only |
| **Standard** | ₹38 | ₹1,200 | Rain + flood + AQI Severe |
| **Premium** | ₹55 | ₹2,000 | All triggers incl. heat, strike, curfew |

## 🤖 AI/ML Integration

### 1. Dynamic Premium Pricing
- Model: XGBoost trained on historical zone disruption data
- Features: flood frequency, average AQI, road closures, seasonal patterns
- Cold start: new workers assigned city-level base premium
- Adjusted weekly per worker zone as GPS data accumulates

### 2. Fraud Detection
| Check | Method | Flag if |
|---|---|---|
| Trigger real? | IMD/NDMA/AQICN cross-verify | No official alert found |
| Worker inactive? | GPS history during claim window | Movement detected |
| Identity fraud | Aadhaar → linked SIM check | Multiple accounts same ID |
| Claim anomaly | ML anomaly detection | Unusual claim frequency |

### 3. Zone Risk Scoring
- Heatmap of each city built from historical IMD, NDMA, traffic data
- Updated monthly
- Drives premium zone classification

## 🔌 Tech Stack

- **Frontend:** Flutter (Android + iOS)
- **Backend:** Python + FastAPI
- **Database:** MongoDB (GeoJSON support for heatmaps)
- **Cache:** Redis
- **ML:** XGBoost, retrained weekly
- **APIs:** IMD, NDMA SACHET, AQICN, Tomorrow.io, IDfy, Razorpay

## 📅 Development Plan

| Phase | Theme | Key Deliverables | Deadline |
|---|---|---|---|
| Phase 1 | Ideate & Know Your Worker | README, repo, 2-min video | March 20 |
| Phase 2 | Protect Your Worker | Registration, premium calc, claims, 2-min demo | April 4 |
| Phase 3 | Perfect for Your Worker | Fraud detection, payout simulation, dashboard, 5-min video | April 17 |