import { io, Socket } from 'socket.io-client';

const SOCKET_URL = process.env.REACT_APP_SOCKET_URL || 'http://localhost:8000';

export const connectToProjectRoom = (
  projectId: string, 
  callback: (data: { type: string; data: unknown }) => void
): Socket => {
  const socket = io(SOCKET_URL);
  
  socket.on('connect', () => {
    socket.emit('join-project-room', projectId);
  });

  socket.on('alert', (data) => {
    callback({ type: 'alert', data });
  });

  return socket;
};

export const disconnectFromServer = (socket?: Socket) => {
  if (socket) {
    socket.disconnect();
  }
};
