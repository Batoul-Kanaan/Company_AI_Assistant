from datetime import datetime

from pydantic import BaseModel


class PolicyCreate(BaseModel):
    policy_id: str
    title: str
    description: str
    category: str
    content: str
    status: str = "active"


class PolicyUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    content: str | None = None
    status: str | None = None


class PolicyInDB(PolicyCreate):
    created_at: datetime
    updated_at: datetime