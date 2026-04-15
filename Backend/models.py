from pydantic import BaseModel, Field, field_validator
from typing import Optional, Union, Literal, Any
from datetime import datetime, timezone
from constants import *
import bcrypt


class Auth(BaseModel) :
    """
    Stores authentication credentials for a worker.
    Kept separate from Worker to isolate auth concerns from profile data.

    Password is automatically bcrypt hashed when the Auth object is instantiated.
    Pass the plain password to password — the class intercepts and hashes
    it automatically via field_validator before storing.

    Attributes:
        worker_id: References Worker._id
        username: Unique login identifier
        password: Auto-hashed via bcrypt on instantiation — pass plain password
        last_login: UTC timestamp of last successful login, None if never logged in
    """
    worker_id: str
    mobile: str
    email: Optional[str] = None
    password: str    # pass plain password — hashed automatically on instantiation
    last_login: Optional[datetime] = None

    @field_validator("password")
    @classmethod
    def hash_password(cls, v: str) -> str:
        """
        Intercepts the plain password value before it is stored.
        Hashes it using bcrypt with an auto-generated salt.

        Args:
            cls: The Auth class itself — required by Pydantic for field validators
            v: The plain password string passed in by the caller

        Returns:
            bcrypt hash string containing version, cost, salt and hash
        """
        return bcrypt.hashpw(v.encode(), bcrypt.gensalt()).decode()

class Worker(BaseModel) :
    """
    Represents a registered gig delivery worker on the platform.
    One document per worker. Claims and policies reference this via worker_id.
    
    Attributes:
        name: Full name of the worker
        age: Age of the worker
        state: State of operation
        city: City of operation
        zone: Primary operating zone e.g. "Lajpat Nagar"
        platform: List of platforms worker is registered on e.g. ["Swiggy", "Zomato"]
        weekly_earnings: Approximate weekly earnings used for payout calculation
        upi_id: UPI ID for payout destination
        plan: Current active plan tier
        mobile: Mobile number as string to preserve leading zeros
        aadhaar_masked: Masked Aadhaar number e.g. "XXXX-XXXX-4521"
        streak: Consecutive weeks subscribed without a claim
        kyc_verified: Whether KYC verification is complete
        created_at: UTC timestamp of account creation
    """
    name: str
    age: int
    state: str
    city: str
    zone: str
    platform: list[str]
    weekly_earnings: float
    upi_id: str
    plan: Optional[Plan] = None
    mobile: str
    email: Optional[str] = None
    aadhaar_masked: str
    streak: int = 0
    kyc_verified: bool
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ExternalAPIResponse(BaseModel) :
    """
    Stores API responses to avoid redundant external calls.
    Before hitting IMD/AQICN/NDMA, check here first.
    
    Attributes:
        source: API that was called e.g. "IMD", "AQICN", "NDMA", "Tomorrow.io"
        city: City the data is for
        zone: Zone the data is for
        event_type: Type of event that has occured
        severity: How severe the event is
        is_trigger: If the event validates the need to activate claim cycle
        raw: Original response of the api
        fetched_at: When the API was actually called
    """
    source: str                # "AQICN", "NDMA", "TOMORROW"
    city: Optional[str]
    zone: Optional[str]
    event_type: Optional[EventType]  # "AQI", "FLOOD", "RAIN", etc
    severity: Optional[float]  # AQI value, rainfall mm, etc
    is_trigger: bool           # CRITICAL → your system uses this
    raw: dict[str, Any]        # original response
    fetched_at: datetime


class PlanTiers(BaseModel) :
    """
    Static lookup table for the three coverage plan tiers.
    Only three documents — Basic, Standard, Premium.
    Seed once at startup, never updated during runtime.
    
    Attributes:
        name: Plan name from Plan enum
        weekly_premium: Base premium before zone risk adjustment
        max_payout: Maximum payout allowed per week
        max_streak_discount: Maximum discount percentage from streak rewards
        covers: List of trigger event types this plan covers
    """
    name: Plan
    weekly_premium: float
    max_payout: float
    max_streak_discount: float
    covers: list[EventType]


class Policies(BaseModel) :
    """
    Represents a weekly insurance policy for a worker.
    One document per worker per week. New policy created each Monday.
    
    Attributes:
        policy_id: Unique policy identifier
        worker_id: References Worker._id
        plan: Plan tier selected by worker
        weekly_premium: Actual premium after streak discount applied
        max_payout: Maximum payout for this policy week
        current_payout: Current payout for this policy week
        created_at: UTC timestamp of policy creation
        start_date: Policy coverage start date
        end_date: Policy coverage end date, None if not yet set
        is_active: Whether policy is currently active
        waiting_period_complete: Whether 2-week waiting period has passed
        streak_week: Worker streak count at time of policy creation
    """
    worker_id: str
    plan: Plan
    weekly_premium: float
    max_payout: float
    current_payout: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    start_date: datetime
    end_date: Optional[datetime] = None
    is_active: bool
    waiting_period_complete: bool
    streak_week: int


class Claims(BaseModel) :
    """
    Represents an insurance claim created automatically when a trigger fires.
    Claims are never filed manually — always system-generated.
    
    Attributes:
        claim_id: Unique claim identifier
        worker_id: References Worker._id
        policy_id: References Policies._id
        trigger_event_id: References TriggerEvents._id
        claim_amount: Calculated payout amount in INR
        claim_type: Full day or partial day loss
        status: Current claim status — monitoring → approved/flagged/rejected
        fraud_checks: Result of each individual fraud check as key-value pairs
                      e.g. {"gps_inactive": True, "mock_location": False}
        created_at: UTC timestamp of claim creation
        resolved_at: UTC timestamp of resolution, None until terminal status reached
    """
    worker_id: str
    policy_id: str
    trigger_event_id: list[str]
    trigger_events: list[EventType]
    claim_amount: float
    claim_type: ClaimType
    status: ClaimStatus
    fraud_checks: dict[str, bool]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: Optional[datetime] = None


class TriggerEvents(BaseModel) :
    """
    Represents a disruption event detected by external API threshold crossing.
    Created automatically when IMD/AQICN/NDMA reports exceed defined thresholds.
    
    Attributes:
        event_id: Unique event identifier
        event_type: Type of disruption from EventType enum
        source: API that reported the event
        state: Affected state
        city: Affected city
        zone: Affected zone
        threshold_value: Actual value that triggered the event e.g. "82mm/hr" or "AQI 412"
        severity: Event severity level — yellow, orange, red
        created_at: UTC timestamp of event detection
        start_time: When the event started
        end_time: When the event ended, None if still active
        is_active: Whether the event is currently ongoing
        affected_workers: List of worker_ids operating in this zone
    """
    event_type: EventType
    source: str
    state: str
    city: str
    zone: str
    threshold_value: str
    severity: Severity
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    start_time: datetime
    end_time: Optional[datetime] = None
    is_active: bool
    affected_workers: list[str]


class Location(BaseModel) :
    """
    Stores location type and coordinates for GpsLogs.
    
    Attributes:
        worker_id: References Worker._id
        latitude: GPS latitude coordinate
        longitude: GPS longitude coordinate
        accuracy: GPS accuracy in meters — lower is better
        timestamp: UTC timestamp of the reading
        is_mocked: Whether reading was flagged by Android LocationManagerCompat.isMockLocationEnabled()
    """
    type: Literal["Point"] = "Point"
    coordinates: list[float]


class GpsLogs(BaseModel) :
    """
    Stores individual GPS readings for each active worker.
    High volume collection — one document per reading per worker.
    Used for fraud detection (inactivity check) and operating zone heatmap generation.
    
    Attributes:
        worker_id: References Worker._id
        latitude: GPS latitude coordinate
        longitude: GPS longitude coordinate
        accuracy: GPS accuracy in meters — lower is better
        timestamp: UTC timestamp of the reading
        is_mocked: Whether reading was flagged by Android LocationManagerCompat.isMockLocationEnabled()
    """
    worker_id: str
    location: Location
    accuracy: float
    timestamp: datetime
    is_mocked: bool

class ApiResponse(BaseModel) :
    """
    Response model for the backend.
    
    Attributes:
        success: Whether the response was generated or an error occurred.
        data: Response data that was generated, if any.
    """
    success: bool
    data: Optional[Union[list, dict, str]] = None