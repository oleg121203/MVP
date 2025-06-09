import { io } from 'socket.io-client';

// Initialize Socket.IO client
const socket = io('http://localhost:8000', {
  path: '/socket.io',
  autoConnect: false
});

// Function to connect to a project room for real-time updates
export const connectToProjectRoom = (projectId, callback) => {
  if (!socket.connected) {
    socket.connect();
  }
  
  socket.on('connect', () => {
    console.log('Connected to Socket.IO server');
    socket.emit('join_project', { project_id: projectId });
  });
  
  socket.on('join_confirmation', (data) => {
    console.log('Joined project room:', data.project_id);
    callback(data);
  });
  
  socket.on('analytics_update', (data) => {
    console.log('Received analytics update:', data);
    callback(data);
  });
  
  socket.on('error', (error) => {
    console.error('Socket.IO error:', error);
  });
  
  socket.on('disconnect', () => {
    console.log('Disconnected from Socket.IO server');
  });
};

// Function to disconnect from the Socket.IO server
export const disconnectFromServer = () => {
  if (socket.connected) {
    socket.disconnect();
  }
};

export default socket;
