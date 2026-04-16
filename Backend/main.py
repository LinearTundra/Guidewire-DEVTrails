from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import db
import uvicorn
from services.scheduler_service import run_scheduler
from asyncio import create_task


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application startup and shutdown.
    Scheduler starts on startup and closes on shutdown.
    Database connection opens on startup and closes on shutdown.
    """
    scheduler_task = create_task(run_scheduler())
    await db.create_gps_index()
    
    yield
    
    scheduler_task.cancel()
    try :
        scheduler_task
    except :
        pass
    await db.close()


app = FastAPI(
    title="GigShield API",
    description="Parametric Income Protection for Gig Delivery Workers",
    version="0.0.1",
    lifespan=lifespan
)

# ── Routers ───────────────────────────────────────────────────────────────────
# from routes import workers, auth, policies, claims, webhooks
from routes import workers, auth, claims, gps, plantiers, policy, premium, triggers
app.include_router(auth.router)
app.include_router(workers.router)
app.include_router(gps.router)
app.include_router(claims.router)
app.include_router(policy.router)
app.include_router(plantiers.router)
app.include_router(premium.router)
app.include_router(triggers.router)


@app.get("/")
async def root():
    return {"status": "GigShield API running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)