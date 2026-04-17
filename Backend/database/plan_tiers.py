from database.Database import db
from constants import Plan


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

