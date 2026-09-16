from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr


class EmployeeStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class EmployeeCreate(BaseModel):
    employee_id: str
    first_name: str
    last_name: str
    email: EmailStr
    department: str
    role: str
    manager_id: str | None = None
    status: EmployeeStatus = EmployeeStatus.ACTIVE


class EmployeeUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    department: str | None = None
    role: str | None = None
    manager_id: str | None = None
    status: EmployeeStatus | None = None


class EmployeeInDB(EmployeeCreate):
    created_at: datetime
    updated_at: datetime