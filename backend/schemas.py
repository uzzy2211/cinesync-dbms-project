from typing import Any

from pydantic import BaseModel, Field


class SeatLockRequest(BaseModel):
    """Opaque request envelope pending Member 1's seat-lock SQL contract."""

    payload: dict[str, Any] = Field(
        description="Request data to be specified after the SQL contract is available."
    )

    class Config:
        extra = "forbid"


class BookingConfirmationRequest(BaseModel):
    """Opaque request envelope pending Member 1's booking SQL contract."""

    payload: dict[str, Any] = Field(
        description="Request data to be specified after the SQL contract is available."
    )

    class Config:
        extra = "forbid"