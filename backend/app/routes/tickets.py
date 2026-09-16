from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.auth import verify_credentials

from backend.app.database.tickets import (
    create_ticket,
    get_ticket,
    get_all_tickets,
    search_tickets,
    update_ticket,
    delete_ticket,
)

from backend.app.models.ticket import (
    TicketCreate,
    TicketUpdate,
    TicketPriority,
    TicketStatus,
)


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
    dependencies=[Depends(verify_credentials)],
)


def serialize_ticket(ticket: dict):
    if ticket:
        ticket["_id"] = str(ticket["_id"])

    return ticket


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_ticket_route(ticket: TicketCreate):
    existing_ticket = get_ticket(ticket.ticket_id)

    if existing_ticket:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ticket already exists",
        )

    result = create_ticket(
        ticket.model_dump()
    )

    return serialize_ticket(result)


@router.get("/")
def get_tickets():
    tickets = get_all_tickets()

    return [
        serialize_ticket(ticket)
        for ticket in tickets
    ]


@router.get("/search")
def search_tickets_route(
    priority: TicketPriority | None = None,
    status: TicketStatus | None = None,
    category: str | None = None,
    employee_id: str | None = None,
):
    query = {}

    if priority:
        query["priority"] = priority

    if status:
        query["status"] = status

    if category:
        query["category"] = category

    if employee_id:
        query["employee_id"] = employee_id

    tickets = search_tickets(query)

    return [
        serialize_ticket(ticket)
        for ticket in tickets
    ]


@router.get("/{ticket_id}")
def get_ticket_route(ticket_id: str):
    ticket = get_ticket(ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    return serialize_ticket(ticket)


@router.put("/{ticket_id}")
def update_ticket_route(
    ticket_id: str,
    ticket: TicketUpdate,
):
    existing_ticket = get_ticket(ticket_id)

    if not existing_ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    updated_ticket = update_ticket(
        ticket_id,
        ticket.model_dump(exclude_unset=True),
    )

    return serialize_ticket(updated_ticket)


@router.delete("/{ticket_id}")
def delete_ticket_route(ticket_id: str):
    deleted = delete_ticket(ticket_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    return {
        "message": "Ticket deleted successfully"
    }