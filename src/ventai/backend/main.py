from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from socketio import AsyncServer
from socketio.asgi import ASGIApp
from ventai.backend.routers import analytics_router, price_intelligence_router

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Create and mount Socket.IO
sio = AsyncServer(async_mode='asgi', cors_allowed_origins="*")
socketio_app = ASGIApp(sio)
app.mount("/socket.io", socketio_app)

# Include routers
app.include_router(analytics_router)
app.include_router(price_intelligence_router)

@app.get("/")
def read_root():
    return {"message": "VentAI API is working"}

@app.get("/api/v1/analytics/projects/{project_id}")
def get_project_analytics(project_id: int):
    return {
        "metrics": {
            "completion_rate": 0.75,
            "budget_compliance": 0.9
        },
        "insights": "Test insights"
    }
