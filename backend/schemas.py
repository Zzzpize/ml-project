from pydantic import BaseModel

class TicketRequest(BaseModel):
    subject : str
    description : str


class TicketResponse(BaseModel):
    equipment : str
    failure_point : str
    serial_number : str | None