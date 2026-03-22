from database.Database import db
from models import PlanTiers
from constants import Plan, EventType


async def get_all_plan_tiers() -> list[dict]:
    """
    Fetches all available plan tiers from the plan_tiers collection.
    Used on the subscription/onboarding screen to display plan options.
    Only 3 documents exist — Basic, Standard, Premium.
    Seeded once at startup, never updated during runtime.
    
    Returns:
        List of all plan tier documents
    """
    return await db.get_database().plan_tiers.find().to_list(length=None)


async def get_plan_tier(plan: Plan) -> dict | None:
    """
    Fetches a single plan tier by plan name.
    Used during policy creation to get max_payout and weekly_premium
    for the selected plan.
    
    Args:
        plan: Plan enum value — Basic, Standard, Premium
        
    Returns:
        Plan tier document as dict or None if not found
    """
    return await db.get_database().plan_tiers.find_one({"name": plan.value})


# async def _seed_plan_tiers() -> None:
#     """
#     Seeds the plan_tiers collection with the three base plans.
#     Only call this once during initial setup — running again will
#     insert duplicates.
#     Internal function — not exported via __init__.py.
#     Call directly from seed.py only.
#     """
#     plans = [
#         PlanTiers(
#             name=Plan.BASIC,
#             weekly_premium=25.0,
#             max_payout=700.0,
#             max_streak_discount=15.0,
#             covers=[
#                 EventType.RAINFALL,
#                 EventType.FLOOD
#             ]
#         ),
#         PlanTiers(
#             name=Plan.STANDARD,
#             weekly_premium=38.0,
#             max_payout=1200.0,
#             max_streak_discount=15.0,
#             covers=[
#                 EventType.RAINFALL,
#                 EventType.FLOOD,
#                 EventType.AQI
#             ]
#         ),
#         PlanTiers(
#             name=Plan.PREMIUM,
#             weekly_premium=55.0,
#             max_payout=2000.0,
#             max_streak_discount=15.0,
#             covers=[
#                 EventType.RAINFALL,
#                 EventType.FLOOD,
#                 EventType.AQI,
#                 EventType.HEAT,
#                 EventType.BANDH,
#                 EventType.CURFEW
#             ]
#         )
#     ]
#     await db.get_database().plan_tiers.insert_many(
#         [plan.model_dump() for plan in plans]
#     )