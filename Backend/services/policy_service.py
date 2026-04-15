from database import policies
import asyncio

async def get_worker_active_policy(worker_id: str) :
    return await policies.get_active_policy(worker_id)

async def is_policy_eligible(policy: dict) -> bool:
    if not policy:
        return False

    if not policy.get("is_active", False):
        return False

    if not policy.get("waiting_period_complete", False):
        return False

    return True

def compute_claim_amount(policy: dict, claim_type: str, activity_hours: float = 0) -> float:
    weekly = policy.get("covered_earnings", 0)

    if weekly <= 0:
        return 0

    per_day = weekly / 7

    if claim_type == "FULL_DAY":
        return per_day

    if claim_type == "PARTIAL":
        # scale between 2–5 hrs → 0–1
        ratio = min(max(activity_hours / 6, 0), 1)
        return per_day * ratio

    return 0

async def process_claim_payout(policy_id: str, claim_type: str, activity_hours: float = 0) -> float:
    """
    End-to-end payout logic.

    Returns:
        actual payout credited (after cap)
    """

    policy = await policies.get_policy(policy_id)

    if not await is_policy_eligible(policy):
        return 0.0

    amount = compute_claim_amount(policy, claim_type, activity_hours)

    if amount <= 0:
        return 0.0

    # capped + persisted
    allowed = await policies.add_payout(policy_id, amount)

    return allowed

async def process_bulk_payout(claims: list[dict]) -> list[float]:
    tasks = [
        process_claim_payout(
            c["policy_id"],
            c["claim_type"],
            c.get("activity_hours", 0)
        )
        for c in claims
    ]

    return await asyncio.gather(*tasks, return_exceptions=True)