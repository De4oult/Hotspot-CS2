# server.py
import asyncio
import socketio
import uvicorn
from fastapi import FastAPI

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")
app = FastAPI()
app.mount("/", socketio.ASGIApp(sio, static_files={"": "static"}))

maps = [
    {'id': 1, 'title': 'Inferno', 'previewUrl': 'https://ukocgukpmdoflluaaiob.supabase.co/storage/v1/object/public/maps/inferno.png', 'banned': False, 'picked': False},
    {'id': 2, 'title': 'Vertigo', 'previewUrl': 'https://ukocgukpmdoflluaaiob.supabase.co/storage/v1/object/public/maps/vertigo.png', 'banned': False, 'picked': False},
    {'id': 3, 'title': 'Nuke', 'previewUrl': 'https://ukocgukpmdoflluaaiob.supabase.co/storage/v1/object/public/maps/nuke.png', 'banned': False, 'picked': False},
    {'id': 4, 'title': 'Overpass', 'previewUrl': 'https://ukocgukpmdoflluaaiob.supabase.co/storage/v1/object/public/maps/overpass.png', 'banned': False, 'picked': False},
    {'id': 5, 'title': 'Assembly', 'previewUrl': 'https://ukocgukpmdoflluaaiob.supabase.co/storage/v1/object/public/maps/assembly.png', 'banned': False, 'picked': False},
    {'id': 6, 'title': 'Memento', 'previewUrl': 'https://ukocgukpmdoflluaaiob.supabase.co/storage/v1/object/public/maps/memento.png', 'banned': False, 'picked': False}
]

current_stage = 'ban'  # 'ban' or 'pick'
current_turn = 0  # индекс текущей команды

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit('initialData', {'maps': maps, 'currentStage': current_stage, 'currentTurn': current_turn}, room=sid)

@sio.event
async def banMap(sid, data):
    global current_turn
    mapId = data['mapId']
    for map in maps:
        if map['id'] == mapId:
            map['banned'] = True
            current_turn = (current_turn + 1) % 2  # смена очереди
            await sio.emit('updateData', {'maps': maps, 'currentTurn': current_turn})
            break

@sio.event
async def pickMap(sid, data):
    global current_turn
    mapId = data['mapId']
    for map in maps:
        if map['id'] == mapId:
            map['picked'] = True
            current_turn = (current_turn + 1) % 2  # смена очереди
            await sio.emit('updateData', {'maps': maps, 'currentTurn': current_turn})
            break

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
