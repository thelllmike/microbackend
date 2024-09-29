from sqlalchemy.orm import Session
from models.ticket import Ticket
from schemas.ticket import TicketSchema

def create_ticket(db: Session, ticket: TicketSchema):
    db_ticket = Ticket(
        user_id=ticket.user_id,
        name=ticket.name,
        email=ticket.email,
        subject=ticket.subject,
        description=ticket.description,
        attachment_url=ticket.attachment_url
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_tickets(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Ticket).offset(skip).limit(limit).all()

def get_ticket_by_id(db: Session, ticket_id: int):
    return db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()

def update_ticket(db: Session, ticket_id: int, ticket: TicketSchema):
    db_ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if db_ticket:
        db_ticket.user_id = ticket.user_id
        db_ticket.name = ticket.name
        db_ticket.email = ticket.email
        db_ticket.subject = ticket.subject
        db_ticket.description = ticket.description
        db_ticket.attachment_url = ticket.attachment_url
        db.commit()
        db.refresh(db_ticket)
    return db_ticket

def delete_ticket(db: Session, ticket_id: int):
    db_ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if db_ticket:
        db.delete(db_ticket)
        db.commit()
    return db_ticket
