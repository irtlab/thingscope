import socket_io from 'socket.io';
import http from 'http';
import abort from './abort';
import { getAmazonDocumentDB } from './db';
import { hasKey, sleep } from './utils/utils';


// Global variables for storing socket session.
const socket_data = {};


async function sendData(db: any) {
  const prev_minute = 0;
  while (1) {
    // TODO
    await sleep(3000);
  }
}


function handleWsConnections(db: any, socket_server: any) {
  socket_server.of('/api').on('connection', (socket: any) => {
    socket_data[socket.id] = socket;

    // When user disconnects we must delete/clean socket session.
    socket.on('disconnect', () => {
      if (socket.id && socket_data && socket_data[socket.id]) {
        delete socket_data[socket.id];
      }
    });
  });
}


(async () => {
  const amazon_document_db = await getAmazonDocumentDB();

  const port_number = 5001;
  const socket_server = http.createServer();
  socket_server.listen(port_number);
  const socket_io_server = socket_io(socket_server);

  handleWsConnections(amazon_document_db, socket_io_server);

  // sendData(amazon_document_db);
})().catch(abort);
