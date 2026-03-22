import asyncio
import sys
from datetime import datetime, timezone, timedelta

from database import db, workers, auth, policies
from database.plan_tiers import get_plan_tier
from models import Worker, Auth, Policies, PlanTiers
from constants import Plan, EventType


async def _seed_plan_tiers() -> None:
    """
    Seeds the plan_tiers collection with the three base plans.
    Only call this once during initial setup — running again will
    insert duplicates.
    Internal function — not exported via __init__.py.
    Call directly from seed.py only.
    """
    plans = [
        PlanTiers(
            name=Plan.BASIC,
            weekly_premium=25.0,
            max_payout=700.0,
            max_streak_discount=15.0,
            covers=[
                EventType.RAINFALL,
                EventType.FLOOD
            ]
        ),
        PlanTiers(
            name=Plan.STANDARD,
            weekly_premium=38.0,
            max_payout=1200.0,
            max_streak_discount=15.0,
            covers=[
                EventType.RAINFALL,
                EventType.FLOOD,
                EventType.AQI
            ]
        ),
        PlanTiers(
            name=Plan.PREMIUM,
            weekly_premium=55.0,
            max_payout=2000.0,
            max_streak_discount=15.0,
            covers=[
                EventType.RAINFALL,
                EventType.FLOOD,
                EventType.AQI,
                EventType.HEAT,
                EventType.BANDH,
                EventType.CURFEW
            ]
        )
    ]
    await db.get_database().plan_tiers.insert_many(
        [plan.model_dump() for plan in plans]
    )


async def seed():
    """
    Seeds the database with initial mock data for the GigShield platform.
    Run once during initial setup only.
    Aborts if workers collection already has documents to prevent duplicates.
    """
    try:

        print("Seeding plan tiers...")
        existing = await db.get_database().plan_tiers.count_documents({})
        if existing > 0 :
            print("Plan already tiers seeded")
        else :
            await _seed_plan_tiers()
            print("Plan tiers seeded")

        # ── Workers ──────────────────────────────────────────────────────────
        print("Seeding workers...")

        raju = Worker(
            name="Raju Verma",
            age=28,
            state="Delhi",
            city="Delhi",
            zone="Lajpat Nagar",
            platform=["Swiggy", "Zomato"],
            weekly_earnings=5500.0,
            upi_id="raju.verma@okaxis",
            plan=Plan.STANDARD,
            mobile="9876543210",
            aadhaar_masked="XXXX-XXXX-4521",
            streak=4,
            kyc_verified=True
        )

        meena = Worker(
            name="Meena Devi",
            age=34,
            state="Delhi",
            city="Delhi",
            zone="Dwarka",
            platform=["Swiggy"],
            weekly_earnings=4750.0,
            upi_id="meena.devi@okaxis",
            plan=Plan.STANDARD,
            mobile="9876543211",
            aadhaar_masked="XXXX-XXXX-7832",
            streak=2,
            kyc_verified=True
        )

        arjun = Worker(
            name="Arjun Singh",
            age=24,
            state="Delhi",
            city="Delhi",
            zone="Karol Bagh",
            platform=["Zomato"],
            weekly_earnings=6000.0,
            upi_id="arjun.singh@okaxis",
            plan=Plan.PREMIUM,
            mobile="9876543212",
            aadhaar_masked="XXXX-XXXX-1947",
            streak=6,
            kyc_verified=True
        )

        raju_id = await workers.get_worker_by_mobile(raju.mobile)
        if raju_id is None :
            raju_id = await workers.create_worker(raju)
        else :
            raju_id = str(raju_id["_id"])
        meena_id = await workers.get_worker_by_mobile(meena.mobile)
        if meena_id is None :
            meena_id = await workers.create_worker(meena)
        else :
            meena_id = str(meena_id["_id"])
        arjun_id = await workers.get_worker_by_mobile(arjun.mobile)
        if arjun_id is None :
            arjun_id = await workers.create_worker(arjun)
        else :
            arjun_id = str(arjun_id["_id"])
        print(f"Workers seeded — Raju: {raju_id}, Meena: {meena_id}, Arjun: {arjun_id}")

        # ── Auth ─────────────────────────────────────────────────────────────
        print("Seeding auth...")

        if await auth.get_auth(raju.mobile) is None :
            await auth.create_auth(Auth(
                worker_id=raju_id,
                mobile=raju.mobile,
                password="raju@123"      # auto hashed by Auth model
            ))

        if await auth.get_auth(meena.mobile) is None :
            await auth.create_auth(Auth(
                worker_id=meena_id,
                mobile=meena.mobile,
                password="meena@123"
            ))

        if await auth.get_auth(arjun.mobile) is None :
            await auth.create_auth(Auth(
                worker_id=arjun_id,
                mobile=arjun.mobile,
                password="arjun@123"
            ))

        print("Auth seeded")

        # ── Policies ─────────────────────────────────────────────────────────
        print("Seeding policies...")

        # get current Monday as policy start date
        today = datetime.now(timezone.utc)
        days_since_monday = today.weekday()
        monday = (today - timedelta(days=days_since_monday)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        sunday = monday + timedelta(days=6, hours=23, minutes=59, seconds=59)

        raju_plan = await get_plan_tier(Plan.STANDARD)
        meena_plan = await get_plan_tier(Plan.STANDARD)
        arjun_plan = await get_plan_tier(Plan.PREMIUM)

        if await policies.get_active_policy(raju_id) is None :
            await policies.create_policy(Policies(
                worker_id=raju_id,
                plan=Plan.STANDARD,
                weekly_premium=raju_plan["weekly_premium"],
                max_payout=raju_plan["max_payout"],
                start_date=monday,
                end_date=sunday,
                is_active=True,
                waiting_period_complete=True,
                streak_week=raju.streak
            ))

        if await policies.get_active_policy(meena_id) is None :
            await policies.create_policy(Policies(
                worker_id=meena_id,
                plan=Plan.STANDARD,
                weekly_premium=meena_plan["weekly_premium"],
                max_payout=meena_plan["max_payout"],
                start_date=monday,
                end_date=sunday,
                is_active=True,
                waiting_period_complete=True,
                streak_week=meena.streak
            ))

        if await policies.get_active_policy(arjun_id) is None :
            await policies.create_policy(Policies(
                worker_id=arjun_id,
                plan=Plan.PREMIUM,
                weekly_premium=arjun_plan["weekly_premium"],
                max_payout=arjun_plan["max_payout"],
                start_date=monday,
                end_date=sunday,
                is_active=True,
                waiting_period_complete=True,
                streak_week=arjun.streak
            ))
        print("Policies seeded")

        print("\nSeeding complete.")

    except Exception as e:
        print(f"Seeding failed: {e}")
        raise

    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(seed())