# 🛵 GigShield — Parametric Income Protection for Gig Delivery Workers

> Automated, instant income protection for India's platform delivery partners against weather, pollution, and disaster disruptions.

> ⚡ TL;DR: Working prototype with onboarding flow, policy management, trigger simulation, and payout demo. Frontend uses mocked data; advanced fraud detection, real-time integrations, and full frontend-backend connectivity are planned for Phase 3.

---

## 📲 Try the App (APK)

- Download APK: [GigShield Demo APK](https://drive.google.com/drive/folders/15jDSIe9b2D0wlW0QF7XZjc3xy2DplAWi?usp=sharing)
- Platform: Android
- Note: This is a hackathon prototype using mocked data (see Demo Instructions below)

---

## 🔗 Backend API (Demo)

- API Docs (Swagger): [https://guidewire-devtrails.onrender.com/docs](https://guidewire-devtrails.onrender.com/docs)
- Demo Credentials
  - Mobile : 9876543210
  - Password : raju@123
  - Worker ID : 69c02315a762ca801b7c810d

> ⚠️ Note: Hosted on Render free tier — initial request may take ~30–60 seconds due to cold start.

> Note: This is a hackathon prototype. Some endpoints operate on mock/synthetic data, and full frontend-backend integration is planned for Phase 3.

---

## 📌 Problem Statement

India's platform-based delivery partners (Zomato, Swiggy, Zepto, Amazon, Dunzo, etc.) lose **20–30% of monthly earnings** during external disruptions like extreme weather, flooding, and dangerous pollution levels. They have no financial safety net. When disruption strikes, they bear the full loss alone.

**GigShield** solves this with a fully automated parametric insurance platform — no paperwork, no loss assessment, instant UPI payout when a verified trigger event occurs in the worker's operating zone.

---

## 🎯 Chosen Persona Segment

**Food Delivery Partners — Zomato / Swiggy**

Rationale: Food delivery riders are the largest and most vulnerable segment. They operate in dense urban zones, work across peak hours (lunch + dinner), and are most exposed to rain, flooding, and pollution events that directly halt deliveries. Their weekly earnings are highly predictable, making parametric modelling straightforward.

---

## 👤 Persona-Based Scenarios

### Persona 1 — Raju Verma
- **Age:** 28
- **City:** Delhi (Lajpat Nagar / Greater Kailash)
- **Platform:** Swiggy + Zomato (multi-platform rider)
- **Monthly earnings:** ~₹22,000
- **Weekly earnings:** ~₹5,500
- **Weekly GigShield premium:** ₹38 (High risk zone)
- **Disruption type:** Environmental — Extreme Rainfall / Flood
- **Scenario:** Delhi receives 80mm rainfall in 6 hours. IMD issues red alert for South Delhi. Lajpat Nagar underpasses flood. GigShield detects the trigger, cross-checks Raju's GPS showing him stationary at home from 11am–7pm, confirms no order movement. Full-day payout of ₹785 auto-transferred to UPI by next morning. Zero paperwork filed.

### Persona 2 — Meena Devi
- **Age:** 34
- **City:** Delhi (Dwarka / Uttam Nagar)
- **Platform:** Swiggy (full-time)
- **Monthly earnings:** ~₹19,000
- **Weekly earnings:** ~₹4,750
- **Weekly GigShield premium:** ₹35 (Medium risk zone)
- **Disruption type:** Environmental — Severe Air Pollution
- **Scenario:** Delhi's AQI crosses 400 for 3 consecutive days in November. GRAP Stage IV restrictions imposed. Meena works reduced hours due to health risk. GigShield detects sustained AQI > 400 via AQICN API, calculates partial income loss based on GPS activity, triggers partial payout of ₹950. Deposited automatically.

### Persona 3 — Arjun Singh
- **Age:** 24
- **City:** Delhi (Karol Bagh / Paharganj)
- **Platform:** Zomato (full-time)
- **Monthly earnings:** ~₹24,000
- **Weekly earnings:** ~₹6,000
- **Weekly GigShield premium:** ₹42 (Medium-High risk zone)
- **Disruption type:** Social — Unplanned Local Strike / Bandh
- **Scenario:** Unannounced traders' bandh shuts Karol Bagh market zone for a full day. GigShield cross-references the bandh alert with Arjun's GPS showing him stationary near his residence. No order movement detected for 9 hours. Full-day payout of ₹857 triggered automatically within 24 hours.

---

## ⚙️ How It Works — Application Workflow

### Stage 1: Onboarding
1. Worker downloads GigShield app
2. Submits Aadhaar-based KYC (identity + linked mobile number verification via IDfy/Karza API)
3. Provides preferred working zones (city/district level)
4. Selects coverage amount tier
5. Selects delivery platform(s)
6. Adds UPI ID / bank account for payouts
7. Account created, base risk profile generated, stored in database

### Stage 2: Premium Calculation
1. System retrieves historical disruption data for worker's zone (IMD, NDMA records)
2. Zone Risk Factor computed:
   - Flood history frequency
   - Average AQI levels
   - Road closure/waterlogging incidents
3. Base weekly premium set from risk factor
4. ML model adjusts premium week-over-week as new data accumulates
5. Worker pays weekly premium upfront (UPI/wallet debit)
6. **2-week waiting period** applies before first claim eligibility (except flood/extreme rain — 1 week; Waiting period logic defined but not enforced in prototype)

### Stage 3: Active Coverage
1. Policy is live for 7 days from payment
2. App runs in background (similar to WhatsApp background process)
3. GPS data passively logged to build movement heatmap of worker's operating zones (GPS logs stored; heatmap generation planned)
4. No action required from worker during this stage

### Stage 4: Trigger Monitoring
In Production: The system polls external APIs every hour for each active worker's zone
In Hackathon: Triggers are simulated by the frontend

**Environmental Triggers**
| Trigger Type | Data Source | Threshold |
|---|---|---|
| Extreme Rainfall | IMD Mausam API | Red alert or > 50mm/hr |
| Flooding / Disaster | NDMA SACHET API | Active flood alert in district |
| Dangerous Air Quality | AQICN API | AQI > 300 (Very Poor) |
| Cyclone / Storm | IMD Cyclone API | Any active alert in state |
| Extreme Heat | Tomorrow.io | Heat index > 45°C for 4+ hours |

**Social Triggers**
| Trigger Type | Data Source | Threshold |
|---|---|---|
| Curfew / Bandh | News API / Government alert feed | Active curfew in worker's district |
| Zone Closure | Admin manual flag + GPS cross-check | Worker's primary zone inaccessible |

When threshold is crossed:
- Affected workers in that zone are flagged automatically
- Fraud checks run in parallel
- If checks pass, payout is queued

### Stage 5: Payout
1. Payout amount determined by coverage tier and disruption severity
2. Auto-transferred via UPI within **24 hours** of verified trigger
3. Worker receives in-app notification with payout details
4. Transaction logged for audit trail

---

## 💰 Weekly Premium Model

- Pricing is **weekly**, aligned with gig worker payout cycles
- Premium is debited every Monday (or chosen day)
- Coverage runs for exactly 7 days
- No long-term commitment — worker can stop anytime
- Premium range: ₹25–₹55 per week depending on zone risk tier

**ML model adjusts premium week-over-week as new data accumulates**

| Zone Risk Tier | Description | Example Weekly Premium |
|---|---|---|
| Low | Historically safe zone, low AQI, no flood record | ₹25 |
| Medium | Occasional disruptions, moderate AQI | ₹38 |
| High | Frequent floods, high AQI, disaster-prone | ₹55 |

### Example Policies

| Plan | Weekly Premium | Max Weekly Payout | Covers | Best For |
|---|---|---|---|---|
| **Basic** | ₹25 | ₹700 | Extreme rain + flood only | Low-risk zone riders, part-time workers |
| **Standard** | ₹38 | ₹1,200 | Rain + flood + AQI Severe | Full-time riders in medium-risk zones |
| **Premium** | ₹55 | ₹2,000 | All triggers incl. heat, strike, curfew | Full-time riders in high-risk zones |

**Payout structure per disruption event:**
- Full day lost (GPS inactive 6+ hrs in trigger zone) → 1/7th of weekly covered earnings
- Partial day (GPS active but reduced, 2–5 hrs) → proportional payout
- Multiple trigger days in one week → capped at max weekly payout of chosen plan

---

## 🤖 AI/ML Integration

### 1. Dynamic Premium Pricing (ML)
- Model: XGBoost trained on historical zone disruption data
- Features: Zone flood frequency, average AQI, road closure incidents, seasonal patterns, worker's actual operating heatmap
- Output: Adjusted weekly premium per worker per week
- Cold start: New workers assigned city-level base premium, adjusted after 2 weeks of GPS data
- Pre-trained models are served via API for risk and fraud scoring.
- Retraining pipelines and real-time model updates are planned for Phase 3 and are not part of the current prototype.

### 2. Fraud Detection (Planned — Phase 3)
When a trigger fires, the following checks run automatically:

| Check | Method | Flag if |
|---|---|---|
| Was trigger real? | IMD/NDMA/AQICN API cross-verify | No official alert found |
| Was worker inactive? | GPS history during claimed window | Movement detected in city |
| Order history check | Platform API partnership / synthetic data in hackathon | Active deliveries during claimed window |
| Identity fraud | Aadhaar → linked SIM check (IDfy/TRAI) | Multiple accounts on same ID |
| Claim pattern anomaly | ML anomaly detection on claim history | Unusual claim frequency |

All checks pass → auto payout. Any flag → manual review queue.

> **Note on order history:** In production, platform API partnerships enable real-time order history cross-referencing — a worker with active deliveries during a claimed disruption window is auto-rejected. For this hackathon, order history is simulated via synthetic data.

### 3. Zone Risk Scoring (ML)
- Risk score map of each city built from historical IMD, NDMA, and traffic data
- Updated monthly
- Drives premium zone classification

---

## 🛡️ Adversarial Defense & Anti-Spoofing Strategy
- Note: This section will be implemented in Phase 3
  
> **Market Crash Event Response:** 500 delivery partners. Fake GPS. Real payouts. A coordinated fraud ring just drained a platform's liquidity pool. Here is how GigShield fights back.

### The Core Challenge
A genuine mass flood event and a coordinated fraud ring look identical at the surface level — hundreds of workers in the same zone, all inactive at the same time. Zone-level clustering alone cannot distinguish them. Timing cannot distinguish them because our system auto-triggers simultaneously for everyone in the affected zone. We need deeper signals.

### Layer 1 — Individual GPS Spoofing Detection

**Mock Location Flag**
Android exposes `LocationManagerCompat.isMockLocationEnabled()` on every GPS reading. Any reading flagged as mocked is sent to manual review. This catches the majority of casual spoofing attempts. Note: mock flag alone is not grounds for auto-rejection as legitimate navigation apps running simultaneously can trigger false positives. Confirmed only when combined with other signals.

**GPS Teleportation Detection**
Real GPS moves gradually. Spoofed GPS snaps instantly. If consecutive GPS readings imply a physically impossible speed — for example jumping from Delhi to a flood zone in Tamil Nadu in 30 seconds — that is a hard spoof signal with no legitimate explanation. Implied speed > 200km/h → auto-reject.

**Accelerometer Cross-Check**
Spoofing GPS coordinates is easy. Faking physical sensors is not. If the accelerometer and gyroscope show real movement during the claim window while GPS reports the device as stationary, the phone is physically moving while pretending not to be. Real sensor movement + stationary GPS = auto-reject. Mock flag + accelerometer mismatch together = auto-reject with no manual review needed.

**Order History Cross-Check**
Where platform API partnerships exist, delivery activity logs are cross-referenced against the claim window. A worker with active order pickups or deliveries during a claimed disruption period is auto-rejected — genuine disruptions halt platform activity entirely. For this hackathon, order history is simulated via synthetic data.

**Emulator Detection**
Fraud rings often run fake accounts on Android emulators. Emulators have detectable signatures — unusual build fingerprints, missing or non-responsive sensors, and identical hardware specs across supposedly different devices. Any device matching emulator signatures is blocked at onboarding entirely.

### Layer 2 — Fraud Ring Detection (Coordinated Attack)

**Account Creation Clustering**
Genuine workers onboard gradually over weeks from different devices, IPs, and times. A fraud ring bulk-creates accounts before a known high-risk event. We flag accounts when 10+ are created within a 24-hour window from nearby IP ranges, onboarding timestamps are near-identical, or multiple accounts select the same zone + plan + UPI prefix combination at signup.

**Android ID Clustering**
Each Android device has a unique Android ID per app install. A fraud ring using rooted or emulated devices produces multiple accounts sharing the same fingerprint. If 5+ accounts share a device fingerprint at claim time, all are flagged for review.

**GPS Scatter Analysis**
In a real flood, 500 workers are stationary at their own homes — coordinates spread naturally across the zone. In a fraud ring, coordinates cluster unnaturally at a small number of points or devices show identical GPS trails before going stationary. If claim coordinate density exceeds 3 standard deviations above the zone baseline, the cluster is flagged for manual review — not auto-rejected — to avoid punishing genuine workers.

**Claim Velocity Check**
If claim volume exceeds 2x the historical maximum for a zone and event type within 1 hour of trigger, a circuit breaker activates — payouts pause, manual review queue opens, and the operations team is alerted.

### Layer 3 — Honest Worker Protection

The key design principle: **flag aggressively, auto-reject conservatively.**

- GPS teleportation detected → auto-reject
- Accelerometer mismatch detected → auto-reject
- Mock flag + any secondary signal → auto-reject
- Mock flag alone → manual review
- Order history shows active deliveries during claimed window → auto-reject
- Emulator detected at onboarding → permanent block
- Ring clustering detected → manual review, never auto-reject
- Circuit breaker triggered → payouts paused, reviewed within 4 hours, genuine workers paid retroactively with ₹50 inconvenience credit

### Summary Defense Stack

| Threat | Detection Method | Response |
|---|---|---|
| Mock location spoofing | `isFromMockProvider()` flag | Flag for review |
| Mock + secondary signal | Mock flag + accelerometer or teleportation | Auto-reject |
| GPS teleportation | Implied speed > 200km/h between readings | Auto-reject |
| Sensor mismatch | Accelerometer movement + stationary GPS | Auto-reject |
| Active deliveries during claim | Order history cross-check (platform API / synthetic) | Auto-reject |
| Emulator accounts | Build fingerprint + sensor signature | Block at onboarding |
| Coordinated ring | Account clustering + Android ID dedup | Flag for review |
| Mass fake claims | GPS scatter analysis + claim velocity circuit breaker | Pause + manual review |
| Fake identity | Aadhaar KYC + linked SIM dedup (IDfy) | Block at onboarding |

---

## ✨ Additional Features

### 1. Streak Rewards
- Workers subscribed continuously for 4+ weeks without claims get a premium discount the following week
- 4 weeks = 5% off, 8 weeks = 10% off, 12+ weeks = 15% off (capped)
- Resets to zero if a valid claim is paid out

### 2. Zone Safety Score (Worker-Facing)
- Live risk score displayed on app home screen every morning
- Score computed from: today's IMD forecast, current AQI, NDMA active alerts, historical disruption frequency
- Three levels: 🟢 Safe / 🟡 Caution / 🔴 High Risk
- Example: *"Your zone (Lajpat Nagar) is 🔴 High Risk today — IMD Yellow Alert active. You are covered."*

---

## 📄 Demo Policy — GigShield Standard Plan

**GIGSHIELD INCOME PROTECTION POLICY**
**Policy Type:** Parametric Weekly Income Protection

| Field | Details |
|---|---|
| **Policyholder** | Raju Verma |
| **Aadhaar (masked)** | XXXX-XXXX-4521 |
| **Platform** | Swiggy + Zomato |
| **Operating Zone** | Lajpat Nagar / Greater Kailash, South Delhi |
| **Zone Risk Tier** | High |
| **Plan** | Standard |
| **Policy Period** | Mon 17 Mar 2026 – Sun 23 Mar 2026 |
| **Weekly Premium** | ₹38 |
| **Max Weekly Payout** | ₹1,200 |
| **Covered Weekly Earnings** | ₹5,500 |
| **Waiting Period** | 2 weeks from first activation (completed) |
| **Payment Method** | UPI — raju.verma@okaxis |
| **Policy ID** | GS-DL-2026-003847 |

### Terms & Conditions

**1. Eligibility**<br>
1.1 Policyholder must be an active gig delivery partner on at least one registered platform.<br>
1.2 Valid Aadhaar-based KYC must be completed at onboarding.<br>
1.3 GigShield mobile app must remain installed and active throughout the policy period.<br>

**2. Premium & Payment**<br>
2.1 Premium is charged on a strictly weekly basis, debited every Monday at 12:00 AM IST.<br>
2.2 If the weekly premium payment fails, coverage lapses immediately for that week.<br>
2.3 Premium amounts are dynamic and may be revised each week based on the ML risk model, communicated at least 24 hours before debit.<br>

**3. Coverage & Payouts**<br>
3.1 GigShield provides parametric income protection only.<br>
3.2 Full day payout (1/7th of covered weekly earnings) triggered when GPS inactivity confirmed for 6+ hours.<br>
3.3 Partial day payout (proportional) triggered when GPS shows reduced movement of 2–5 hours.<br>
3.4 Total payouts capped at plan's maximum weekly payout.<br>
3.5 Payout transferred to UPI within 24 hours of trigger verification.<br>

**4. Waiting Period**<br>
4.1 Mandatory 2-week waiting period from first policy activation.<br>
4.2 Exception: flood and cyclone triggers have 1-week waiting period.<br>

**5. Exclusions**
- Health, medical, or hospitalisation expenses<br>
- Life insurance or death benefits<br>
- Accident, injury, or disability claims<br>
- Vehicle repair, damage, or theft<br>
- Income loss due to personal reasons<br>
- Platform-side issues (app downtime, account suspension)<br>
- Pre-planned events announced > 48 hours in advance<br>
- War, civil unrest, riots, or acts of terrorism<br>
- Pandemic or epidemic declared by WHO or Government of India<br>
- Government-imposed lockdowns, curfews, or economic sanctions not covered under social triggers<br>
- Nuclear, biological, or chemical disasters<br>
- Acts of God beyond the parametric triggers defined in this policy<br>

**6. Fraud & Misrepresentation**<br>
6.1 False zone information at signup = immediate cancellation without refund.<br>
6.2 GPS spoofing detected = permanent ban and claim rejection.<br>
6.3 Multiple accounts under same Aadhaar = all policies cancelled.<br>
6.4 GigShield reserves the right to flag any claim for manual review if anomaly detection raises a fraud signal.<br>

**7. Claim Process**<br>
7.1 Fully automated — no manual filing required.<br>
7.2 Payout dispatched within 24 hours of clean fraud check.<br>
7.3 Flagged claims resolved within 72 hours.<br>

**8. Governing Law**<br>
8.1 Governed by laws of India. Jurisdiction: Delhi.<br>
8.2 This is a hackathon prototype and does not constitute a legally binding insurance contract.<br>

---

## 📱 Platform Choice — Mobile (React Native)

GigShield is built as a **mobile-first Android/iOS app** using React Native.

Justification:
- Gig workers operate entirely on mobile — no access to desktops during work
- Background GPS logging requires a persistent mobile process
- Push notifications for instant payout alerts are native to mobile
- UPI payment integration is seamless on mobile
- Aadhaar OTP and camera-based document upload works best on mobile
- React Native enables single codebase for Android + iOS

---

## 📊 Analytics Dashboard

### Worker Dashboard (In-App)
- Active policy status and coverage period
- Weekly premium paid and next debit date
- Total earnings protected (lifetime)
- Disruption alerts active in their zone
- Payout history

### Insurer / Admin Dashboard (Web)
- Total active policies by zone and city
- Live disruption trigger map
- Claims initiated vs paid vs flagged for review
- Loss ratio per zone (payouts ÷ premiums)
- Predictive analytics: next week's likely claim volume based on weather forecast
- Fraud flagging queue

---

## 🔌 Tech Stack

### Mobile App
- **Framework:** React Native (Android + iOS, single codebase)
- **Background Services:** React Native background fetch / Expo background tasks

### Backend
- **Language:** Python (FastAPI)
- **Database:** MongoDB (worker profiles, policies, claims, GPS heatmap — GeoJSON support)
- **Cache:** Redis (session management, real-time trigger state)
- **ML Pipeline:** Python (XGBoost), retrained weekly

### External APIs
| Purpose | API | Cost |
|---|---|---|
| Weather triggers | IMD Mausam API | Free |
| Disaster/flood alerts | NDMA SACHET API | Free |
| Air quality triggers | AQICN (WAQI) API | Free |
| Supplementary weather | Tomorrow.io | Free tier |
| KYC / Identity | IDfy or Karza | Paid (per-call) |
| Payments | Razorpay / UPI | Per-transaction fee |

### Infrastructure
- **Hosting:** Railway / Render / AWS / Self-hosted via ngrok (TBD)

---

## 📵 Platform API Limitation & Workaround

Major platforms (Zomato, Swiggy, Zepto) do not expose public APIs for gig worker earnings or order history. For this hackathon, **synthetic data** simulating realistic delivery patterns, zones, and order histories is used.

**Production path:** Direct platform partnership agreements or driver-consent OAuth-based data sharing via India's Account Aggregator framework.

---

## 🚫 Exclusions
This platform explicitly **does not cover:**
- Health or medical expenses
- Life insurance or death benefits
- Accident or injury claims
- Vehicle repair or damage
- War, civil unrest, or acts of terrorism
- Pandemic or epidemic declared events
- Government-imposed lockdowns or economic sanctions
- Nuclear, biological, or chemical disasters
- Acts of God beyond covered parametric triggers

---

## 🚧 Phase 2 Scope & Implementation Status

This submission focuses on delivering a working prototype of core system flows. Some advanced components are intentionally scoped for Phase 3.

### ✅ Implemented in Phase 2
- User onboarding and KYC flow
- Policy creation and management
- Dynamic premium calculation (ML model via API)
- Trigger simulation (weather, AQI, disruption events)
- Automated claim creation and payout simulation
- Worker and admin dashboards (basic)

### ⚠️ Partially Implemented / Simulated
- External API integrations (IMD, NDMA, AQI) are simulated where required
- Order history and delivery activity use synthetic data
- Instant payouts are demonstrated using test/sandbox environments
- Frontend is currently operating on mocked data; full frontend-backend integration is pending

### 🚀 Planned for Phase 3
- Full fraud detection system (GPS spoofing, emulator detection, anomaly ML)
- Real-time API integrations and live trigger ingestion
- Full frontend-backend integration (real-time data sync and API connectivity)
- Production-grade ML retraining pipelines
- Payment gateway production integration (Razorpay/UPI live)

---

## 📅 Development Plan

| Phase | Theme | Key Deliverables | Deadline |
|---|---|---|---|
| Phase 1 | Ideate & Know Your Worker | README, repo setup, 2-min strategy video | March 20 |
| Phase 2 | Protect Your Worker | Registration, policy management, dynamic premium calculation, claims management, 2-min demo video | April 4 |
| Phase 3 | Perfect for Your Worker | Advanced fraud detection, instant payout simulation (Razorpay sandbox), intelligent dashboard, 5-min demo video, final pitch deck (PDF) | April 17 |

---


## 📁 Repository Structure
```
Guidewire-DEVTrails/
├── README.md
├── .gitignore
│
├── Backend/
│   ├── main.py                  # FastAPI entry point
│   ├── models.py                # Pydantic models
│   ├── constants.py             # Enums (Plan, ClaimStatus, EventType etc.)
│   ├── requirements.txt
│   ├── mock-data.py             # Database seeding script
│   │
│   ├── database/                # MongoDB CRUD operations
│   │   ├── Database.py          # Connection singleton
│   │   ├── workers.py
│   │   ├── auth.py
│   │   ├── policies.py
│   │   ├── claims.py
│   │   ├── plan_tiers.py
│   │   ├── trigger_events.py
│   │   ├── gps_logs.py
│   │   └── api_cache.py
│   │
│   ├── routes/                  # FastAPI route handlers
│   │   ├── auth.py              # Login, register, reset password
│   │   ├── workers.py           # Worker profile endpoints
│   │   ├── claims.py            # Claims fetch endpoints
│   │   ├── policy.py            # Policy endpoints
│   │   ├── plantiers.py         # Plan tier endpoints
│   │   ├── premium.py           # Premium calculation
│   │   ├── gps.py               # GPS log upload
│   │   └── triggers.py          # Trigger simulation
│   │
│   ├── services/                # Business logic
│   │   ├── claim_service.py     # Claim creation and bulk processing
│   │   ├── trigger_service.py   # Trigger event handling
│   │   ├── gps_service.py       # GPS inactivity checks
│   │   ├── ml_service.py        # ML model integration
│   │   └── worker_service.py
│   │
│   └── API/                     # External API clients
│       ├── base_client.py
│       ├── weather_client.py    # IMD integration
│       ├── aqi_client.py        # AQICN integration
│       ├── disaster_client.py   # NDMA SACHET integration
│       └── tomorrow.py          # Tomorrow.io integration
│
├── frontend/                    # React Native (Expo) mobile app
│   ├── App.tsx
│   ├── src/
│   │   ├── screens/             # App screens
│   │   ├── components/          # Reusable components
│   │   ├── navigation/          # Tab and stack navigation
│   │   └── services/            # API service layer
│   └── android/                 # Android build files
│
├── ml
│   ├── app.py                   # ML model and api endpoint
│   ├── Dockerfile
│   ├── fraud_model.pkl
│   ├── requirements.txt
│   ├── risk_model.pkl
│
└── Phase1 Prototype/
    └── gigshield-prototype.html # Phase 1 web prototype
```
## 🔗 Repository

**Team:** AFK <br>
**Team Leader:** Sarthak Kalyani <br>
**Members:** Sachin Bisht, Sahil Vishwakarma, Saket Kumar, Samdarsh Mahajan
