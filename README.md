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

### Payout Structure
- Full day lost (GPS inactive 6+ hrs) → 1/7th of weekly covered earnings
- Partial day (GPS active but reduced 2–5 hrs) → proportional payout
- Multiple trigger days in one week → capped at max weekly payout

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

## 📄 Demo Policy — GigShield Standard Plan

**GIGSHIELD INCOME PROTECTION POLICY**

| Field | Details |
|---|---|
| **Policyholder** | Raju Verma |
| **Aadhaar (masked)** | XXXX-XXXX-4521 |
| **Platform** | Swiggy + Zomato |
| **Operating Zone** | Lajpat Nagar, South Delhi |
| **Zone Risk Tier** | High |
| **Plan** | Standard |
| **Policy Period** | Mon 17 Mar 2026 – Sun 23 Mar 2026 |
| **Weekly Premium** | ₹38 |
| **Max Weekly Payout** | ₹1,200 |
| **Policy ID** | GS-DL-2026-003847 |

### Terms & Conditions

**1. Eligibility**
1.1 Policyholder must be an active gig delivery partner on at least one registered platform.
1.2 Valid Aadhaar-based KYC must be completed at onboarding.
1.3 GigShield app must remain installed and active throughout the policy period.

**2. Premium & Payment**
2.1 Premium charged weekly, debited every Monday at 12:00 AM IST.
2.2 Failed payment = immediate lapse for that week.
2.3 Premium may be revised weekly based on ML risk model, communicated 24hrs before debit.

**3. Coverage & Payouts**
3.1 Parametric income protection only — fixed amounts tied to verified triggers.
3.2 Full day payout triggered when GPS inactivity confirmed for 6+ hours.
3.3 Partial day payout triggered when GPS shows reduced movement of 2–5 hours.
3.4 Total payouts capped at plan's maximum weekly payout.
3.5 Payout transferred to UPI within 24 hours of trigger verification.

**4. Waiting Period**
4.1 Mandatory 2-week waiting period from first policy activation.
4.2 Exception: flood and cyclone triggers have 1-week waiting period.

**5. Exclusions**
- Health, medical, or hospitalisation expenses
- Life insurance or death benefits
- Accident, injury, or disability claims
- Vehicle repair, damage, or theft
- Platform-side issues (app downtime, account suspension)
- Pre-planned events announced > 48 hours in advance

**6. Fraud**
6.1 False zone information at signup = immediate cancellation without refund.
6.2 GPS spoofing detected = permanent ban and claim rejection.
6.3 Multiple accounts under same Aadhaar = all policies cancelled.

**7. Claim Process**
7.1 Fully automated — no manual filing required.
7.2 Payout dispatched within 24 hours of clean fraud check.
7.3 Flagged claims resolved within 72 hours.

**8. Governing Law**
8.1 Governed by laws of India. Jurisdiction: Delhi.
8.2 This is a hackathon prototype and does not constitute a legally binding contract.

## ✨ Additional Features

### 1. Streak Rewards
- 4 weeks continuous = 5% premium discount
- 8 weeks = 10% off
- 12+ weeks = 15% off (capped)
- Resets on valid payout

### 2. Zone Safety Score
- Live risk score on app home screen every morning
- 🟢 Safe / 🟡 Caution / 🔴 High Risk
- Computed from IMD forecast, AQI, NDMA alerts, historical frequency

## 📵 Platform API Limitation & Workaround

Major platforms (Zomato, Swiggy, Zepto) do not expose public APIs for gig worker earnings. Synthetic data used for hackathon demo.

**Production path:** Direct platform partnerships or driver-consent OAuth via Account Aggregator framework.

## 🚫 Exclusions

- Health or medical expenses
- Life insurance
- Accident or injury claims
- Vehicle repair or damage

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

## 🔗 Repository

**Team:** AFK
**Team Leader:** Sarthak Kalyani
**Video:** [LINK PLACEHOLDER]