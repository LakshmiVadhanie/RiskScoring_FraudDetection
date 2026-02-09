from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List
import asyncio
import uuid
from datetime import datetime

from database.connection import init_db
from utils.redis_client import RedisClient
from api.routes.routes import transactions, analytics

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    app.state.redis = RedisClient()
    await app.state.redis.connect()
    yield
    await app.state.redis.close()

app = FastAPI(
    title="Fraud Detection API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["Transactions"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])

@app.get("/")
async def root():
    return {"message": "Fraud Detection API", "status": "operational"}

@app.get("/api/v1/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

app.state.ws_manager = manager