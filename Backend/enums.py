from enum import Enum


class Plan(str, Enum):
    """
    Coverage plan tiers available to workers.
    Inherits from str to serialize as plain string in MongoDB.
    
    Values:
        BASIC: Entry level plan covering rain and flood only
        STANDARD: Mid tier plan covering rain, flood and severe AQI
        PREMIUM: Full coverage including heat, strike and curfew
    """
    BASIC = "Basic"
    STANDARD = "Standard"
    PREMIUM = "Premium"


class ClaimStatus(str, Enum):
    """
    Lifecycle status of an insurance claim.
    Claims always start at MONITORING and move to a terminal status.
    
    Values:
        MONITORING: Trigger detected, system watching situation before deciding
        AUTO_APPROVED: All fraud checks passed, payout initiated
        FLAGGED: One or more fraud signals detected, sent to manual review
        REJECTED: Claim denied after manual review or hard fraud signal
        MANUAL_REVIEW: Under human review, not yet resolved
    """
    MONITORING = "monitoring"
    AUTO_APPROVED = "auto_approved"
    FLAGGED = "flagged"
    REJECTED = "rejected"
    MANUAL_REVIEW = "manual_review"


class ClaimType(str, Enum):
    """
    Type of income loss being claimed.
    Determines payout calculation method.
    
    Values:
        FULL_DAY: GPS inactive 6+ hours — pays 1/7th of weekly covered earnings
        PARTIAL_DAY: GPS active but reduced 2-5 hours — proportional payout
    """
    FULL_DAY = "full_day"
    PARTIAL_DAY = "partial_day"


class Severity(str, Enum):
    """
    Severity level of a trigger event as reported by the source API.
    Maps to IMD alert color codes and AQI severity bands.
    
    Values:
        YELLOW: Moderate disruption, coverage monitoring begins
        ORANGE: Significant disruption, high likelihood of payout
        RED: Severe disruption, payout highly likely
    """
    YELLOW = "yellow"
    ORANGE = "orange"
    RED = "red"


class EventType(str, Enum):
    """
    Type of external disruption event that can trigger a claim.
    Each plan tier covers a subset of these event types.
    
    Values:
        FLOOD: Active flooding in worker zone — NDMA SACHET
        RAINFALL: Extreme rainfall exceeding threshold — IMD
        AQI: Dangerous air quality levels — AQICN
        HEAT: Extreme heat index — Tomorrow.io
        BANDH: Unplanned local market or traders strike
        CURFEW: Government imposed curfew in district
    """
    FLOOD = "flood"
    RAINFALL = "rainfall"
    AQI = "aqi"
    HEAT = "heat"
    BANDH = "bandh"
    CURFEW = "curfew"