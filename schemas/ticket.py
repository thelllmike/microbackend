from pydantic import BaseModel

class TicketSchema(BaseModel):
    user_id: int
    name: str
    email: str
    subject: str
    description: str
    attachment_url: str = None

    class Config:
        orm_mode = True
