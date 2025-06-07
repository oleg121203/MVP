from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import ai

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ai.router, prefix="/api/ai")

@app.get("/")
async def root():
    return {"message": "VentAI Backend Service"}
