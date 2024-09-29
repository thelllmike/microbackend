from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.ticket import TicketSchema
from crud.ticket import create_ticket, get_tickets, get_ticket_by_id, update_ticket, delete_ticket
from database import get_db
from utils.auth import get_current_user  # Import your token verification function

router = APIRouter()

# Secure the route for adding a ticket with JWT token
@router.post("/tickets/")
def add_ticket(ticket: TicketSchema, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Now current_user contains the authenticated user's information
    return create_ticket(db, ticket)

# Secure the route for reading all tickets with JWT token
@router.get("/tickets/")
def read_tickets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    tickets = get_tickets(db, skip=skip, limit=limit)
    if not tickets:
        raise HTTPException(status_code=404, detail="No tickets found")
    return tickets

# Secure the route for reading a specific ticket with JWT token
@router.get("/tickets/{ticket_id}")
def read_ticket(ticket_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    ticket = get_ticket_by_id(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

# Secure the route for updating a ticket with JWT token
@router.put("/tickets/{ticket_id}")
def update_ticket_endpoint(ticket_id: int, ticket: TicketSchema, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    updated_ticket = update_ticket(db, ticket_id, ticket)
    if not updated_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return updated_ticket

# Secure the route for deleting a ticket with JWT token
@router.delete("/tickets/{ticket_id}")
def delete_ticket_endpoint(ticket_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    deleted_ticket = delete_ticket(db, ticket_id)
    if not deleted_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"detail": "Ticket deleted"}
