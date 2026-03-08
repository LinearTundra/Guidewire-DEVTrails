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

## ⚙️ Workflow (Draft)

1. Worker onboards with KYC
2. Selects zone and coverage plan
3. Pays weekly premium
4. App monitors triggers in background
5. Trigger fires → auto payout to UPI

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

## 🔌 APIs

| Purpose | API | Cost |
|---|---|---|
| Weather | IMD Mausam API | Free |
| Disaster alerts | NDMA SACHET | Free |
| Air quality | AQICN (WAQI) | Free |
| Supplemental weather | Tomorrow.io | Free tier |
| KYC | IDfy / Karza | Paid per-call |
| Payments | Razorpay | Per-transaction |

## 📅 Development Plan

| Phase | Theme | Deadline |
|---|---|---|
| Phase 1 | Ideate & Know Your Worker | March 20 |
| Phase 2 | Protect Your Worker | April 4 |
| Phase 3 | Perfect for Your Worker | April 17 |