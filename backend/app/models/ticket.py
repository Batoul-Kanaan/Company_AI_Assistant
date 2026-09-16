from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketCreate(BaseModel):
    ticket_id: str
    employee_id: str
    title: str
    description: str
    category: str
    priority: TicketPriority = TicketPriority.MEDIUM
    status: TicketStatus = TicketStatus.OPEN
    assigned_to: str | None = None


class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    priority: TicketPriority | None = None
    status: TicketStatus | None = None
    assigned_to: str | None = None


class TicketInDB(TicketCreate):
    created_at: datetime
    updated_at: datetime