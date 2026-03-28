from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import db
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application startup and shutdown.
    Database connection opens on startup and closes on shutdown.
    """
    await db.create_gps_index()
    yield
    await db.close()


app = FastAPI(
    title="GigShield API",
    description="Parametric Income Protection for Gig Delivery Workers",
    version="0.0.1",
    lifespan=lifespan
)

# ── Routers ───────────────────────────────────────────────────────────────────
# from routes import workers, auth, policies, claims, webhooks
from routes import workers, auth, claims, gps
app.include_router(auth.router)
app.include_router(workers.router)
app.include_router(gps.router)
app.include_router(claims.router)
# app.include_router(policies.router)
# app.include_router(webhooks.router)


@app.get("/")
async def root():
    return {"status": "GigShield API running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)