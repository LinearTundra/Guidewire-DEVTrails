from database import policies

async def get_worker_active_policy(worker_id: str) :
    return policies.get_active_policy(worker_id)