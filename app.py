from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib

app = FastAPI(title="GigShield API 🚀")


# -------- Load Models --------
risk_model = joblib.load("risk_model.pkl")
fraud_model = joblib.load("fraud_model.pkl")


# -------- Input Schema --------
class PredictionInput(BaseModel):
    # Weather
    precip_mm: float = Field(..., ge=0)
    temperature_celsius: float
    humidity: float = Field(..., ge=0, le=100)
    aqi: float = Field(..., ge=0)

    # Worker behavior (REAL INPUT)
    hours_worked: float = Field(..., ge=0, le=24)
    distance_km: float = Field(..., ge=0)
    orders_completed: int = Field(..., ge=0)
    avg_speed: float = Field(..., ge=0)
    claims_last_week: int = Field(..., ge=0)

    # Financial
    weekly_earning: float = Field(..., ge=0)
    hours_inactive: float = Field(..., ge=0, le=24)


# -------- Output Schema --------
class PredictionOutput(BaseModel):
    risk_score: float
    risk_level: str
    fraud_status: str
    premium: int
    payout: float
    claim_status: str


# -------- Feature Conversion (IMPORTANT) --------
def convert_to_model_features(data: PredictionInput):
    """
    Convert user input → 30 features (for fraud model)
    NOTE: This is simplified mapping for demo
    """

    features = [
        data.hours_worked,
        data.distance_km,
        data.orders_completed,
        data.avg_speed,
        data.claims_last_week
    ]

    # pad remaining features (since original model expects 30)
    while len(features) < 30:
        features.append(0)

    return features


# -------- Home Route --------
@app.get("/")
def home():
    return {"message": "GigShield API Running 🚀"}


# -------- Prediction Route --------
@app.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput):

    try:
        # ===== 1. Risk Prediction =====
        risk_input = [[
            data.precip_mm,
            data.temperature_celsius,
            data.humidity,
            data.aqi
        ]]

        risk_score = float(risk_model.predict(risk_input)[0])

        # ===== 2. Fraud Prediction =====
        fraud_features = convert_to_model_features(data)
        fraud_prob = float(fraud_model.predict_proba([fraud_features])[0][1])

        fraud_status = "Fraud" if fraud_prob > 0.3 else "Normal"

        # ===== 3. Premium Logic =====
        if risk_score > 70:
            premium = 55
            risk_level = "High"
        elif risk_score > 40:
            premium = 38
            risk_level = "Medium"
        else:
            premium = 25
            risk_level = "Low"

        # ===== 4. Payout Logic =====
        daily_income = data.weekly_earning / 7

        if fraud_status == "Fraud":
            payout = 0
            claim_status = "Rejected"
        else:
            if data.hours_inactive >= 6:
                payout = daily_income
            elif 2 <= data.hours_inactive < 6:
                payout = daily_income * 0.5
            else:
                payout = 0
            claim_status = "Approved"

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "fraud_status": fraud_status,
            "premium": premium,
            "payout": payout,
            "claim_status": claim_status
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))