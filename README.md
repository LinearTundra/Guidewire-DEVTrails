# 🛵 GigShield — Parametric Income Protection for Gig Delivery Workers

## 📌 Problem Statement

India's platform-based delivery partners (Zomato, Swiggy, Zepto, Amazon, Dunzo, etc.) lose **20–30% of monthly earnings** during external disruptions like extreme weather, flooding, and dangerous pollution levels. They have no financial safety net. When disruption strikes, they bear the full loss alone.

## 🎯 Chosen Persona Segment

**Food Delivery Partners — Zomato / Swiggy**

Rationale: Food delivery riders are the largest and most vulnerable segment. They operate in dense urban zones and are most exposed to rain, flooding, and pollution events that directly halt deliveries.

## 👤 Personas (Draft)

### Persona 1 — Raju Verma
- **City:** Delhi (Lajpat Nagar / Greater Kailash)
- **Platform:** Swiggy + Zomato
- **Weekly earnings:** ~₹5,500
- **Scenario:** Heavy rainfall floods his zone. Loses full day income with no compensation.

### Persona 2 — Meena Devi
- **City:** Delhi (Dwarka)
- **Platform:** Swiggy
- **Weekly earnings:** ~₹4,750
- **Scenario:** AQI crosses 400 for 3 days. Works reduced hours, partial income lost.

### Persona 3 — Arjun Singh
- **City:** Delhi (Karol Bagh)
- **Platform:** Zomato
- **Weekly earnings:** ~₹6,000
- **Scenario:** Unplanned local bandh shuts down his pickup zone for a full day.

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

### Stage 3: Active Coverage
1. Policy live for 7 days from payment
2. App runs in background logging GPS passively

### Stage 4: Trigger Monitoring
1. APIs polled every hour for worker's zone
2. Threshold crossed → worker flagged automatically
3. Fraud checks run in parallel

### Stage 5: Payout
1. Auto-transferred via UPI within 24 hours
2. Worker notified in-app

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

## 🔌 Tech Stack (Draft)

- **Frontend:** Flutter (Android + iOS)
- **Backend:** Python + FastAPI
- **Database:** MongoDB
- **ML:** XGBoost
- **APIs:** IMD, NDMA, AQICN, Tomorrow.io, IDfy, Razorpay

## 📅 Development Plan

| Phase | Theme | Deadline |
|---|---|---|
| Phase 1 | Ideate & Know Your Worker | March 20 |
| Phase 2 | Protect Your Worker | April 4 |
| Phase 3 | Perfect for Your Worker | April 17 |