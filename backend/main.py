import uvicorn

from urllib import request
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.ml.inference import TicketPredictor
from backend.schemas import TicketRequest, TicketResponse

app = FastAPI()
predictor: TicketPredictor = None

@app.on_event("startup")
async def startup_event():
    global predictor
    predictor = TicketPredictor()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/api/predict", response_model=TicketResponse)
async def predict_ticket(ticket: TicketRequest) -> TicketResponse:
    equipment, failure_point, serial_number = predictor.predict(
        ticket.subject,
        ticket.description
    )

    return TicketResponse(
        equipment=equipment,
        failure_point=failure_point,
        serial_number=serial_number
    )

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
