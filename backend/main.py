from fastapi import FastAPI
from pydantic import BaseModel
from backend.classifier import classify_intent
from backend.responder import generate_response
from backend.responder import conversation_state
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer, util
import json

app = FastAPI()

origins = [
    "http://localhost:3000",
  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CustomerQuery(BaseModel):
    email : str
    message: str

@app.post("/query")
async def handle_query(query: CustomerQuery):
    global conversation_state
    intent = conversation_state.get("active_intent")
    if intent is None:
        intent = classify_intent(query.message)
    response, conversation_state = generate_response(query.message,query.email,intent)
    return {"response": response}