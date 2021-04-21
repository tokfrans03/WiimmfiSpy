import asyncio
import json
from sys import unraisablehook
from threading import Thread
import threading
from WiimmfiSpy import Room
from pydantic import BaseModel
from typing import List, Optional
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket, WebSocketDisconnect
import uvicorn
from threading import Thread


# run with > uvicorn main:app --reload

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# start with: uvicorn main:app --reload

class string(BaseModel):
    url: str

rooms = []


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()

async def room_updated(room: Room):
    print("updating room.", room)
    await manager.broadcast({
        "type": "update",
        "message": room.dump()
    })

def aloop(loop: asyncio.BaseEventLoop, f, a):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(f(a))

@app.post("/room")
def add_room(url: string):
    r = Room(url.url)
    rooms.append(r)
    thread = Thread(target=aloop, args=(asyncio.new_event_loop(), r.get_forever_async, room_updated), daemon=True)
    thread.start()

    return "added!"

@app.delete("/room")
def remove_room():
    for i, room in enumerate(reversed(rooms)):
        room.stop = True
        rooms.pop(i)
    return f"removed all rooms"


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        await websocket.send_json({
            "type": "info",
            "message": "welcome!"
        })
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            # await manager.broadcast(f"Client says: {data}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # await manager.broadcast(f"Client left the chat")




# @app.get("/", response_class=HTMLResponse)
# def read_root():
#     return open(f"{webroot}index.html").read()

# webroot = "webview/dist/"
# app.mount("/", StaticFiles(directory=webroot), name="static")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)