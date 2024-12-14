from flask_socketio import emit
from . import socketio

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

def emit_status_update(message, title):
    print(f'Emitting status update: {message} - {title}')
    socketio.emit('status_update', {'message': message, 'title': title})
