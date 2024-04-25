import { Server } from 'socket.io';
import type { PudgelandContent } from '.';

const server = new Server(8080);

server.on('connection', (socket) => {
  socket.on('message', (args) => {
    const content: PudgelandContent = JSON.parse(args);

    socket.broadcast.emit(String(content.code), content.data);
  });
});

console.log('Started');
