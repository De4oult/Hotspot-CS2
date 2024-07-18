// server.js
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

const maps = [
    { 'id': 1, 'title': 'inferno', 'previewUrl': 'https://ukocgukpmdoflluaaiob.supabase.co/storage/v1/object/public/maps/inferno.png', 'banned': false, 'picked': false },
    { 'id': 2, 'title': 'vertigo', 'previewUrl': 'https://ukocgukpmdoflluaaiob.supabase.co/storage/v1/object/public/maps/vertigo.png', 'banned': false, 'picked': false },
    { 'id': 3, 'title': 'nuke', 'previewUrl': 'https://ukocgukpmdoflluaaiob.supabase.co/storage/v1/object/public/maps/nuke.png', 'banned': false, 'picked': false },
    { 'id': 4, 'title': 'overpass', 'previewUrl': 'https://ukocgukpmdoflluaaiob.supabase.co/storage/v1/object/public/maps/overpass.png', 'banned': false, 'picked': false },
    { 'id': 5, 'title': 'assembly', 'previewUrl': 'https://ukocgukpmdoflluaaiob.supabase.co/storage/v1/object/public/maps/assembly.png', 'banned': false, 'picked': false },
    { 'id': 6, 'title': 'memento', 'previewUrl': 'https://ukocgukpmdoflluaaiob.supabase.co/storage/v1/object/public/maps/memento.png', 'banned': false, 'picked': false }
];

let currentStage = 'ban';  // 'ban' or 'pick'
let currentTurn = 0;  // индекс текущей команды

io.on('connection', (socket) => {
    console.log(`Client connected: ${socket.id}`);
    socket.emit('initialData', { maps, currentStage, currentTurn });

    socket.on('banMap', (data) => {
        const mapId = data.mapId;
        for (const map of maps) {
            if (map.id === mapId) {
                map.banned = true;
                currentTurn = (currentTurn + 1) % 2;  // смена очереди
                io.emit('updateData', { maps, currentTurn });
                break;
            }
        }
    });

    socket.on('pickMap', (data) => {
        const mapId = data.mapId;
        for (const map of maps) {
            if (map.id === mapId) {
                map.picked = true;
                currentTurn = (currentTurn + 1) % 2;  // смена очереди
                io.emit('updateData', { maps, currentTurn });
                break;
            }
        }
    });
});

const PORT = 8000;
server.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
