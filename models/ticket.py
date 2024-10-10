from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)  # ForeignKey to users table
    name = Column(String, index=True)
    email = Column(String, index=True)
    subject = Column(String, index=True)
    description = Column(Text, nullable=False)
    attachment_url = Column(String, nullable=True)  # URL for the attachment


