function final() {
    const serializedRoomState = serializeRoomState();
    localStorage.setItem('roomState', serializedRoomState);
    // Draw the room after saving the layout
    drawRoom(room);
}

function serializeRoomState() {
    return JSON.stringify(room);
}

