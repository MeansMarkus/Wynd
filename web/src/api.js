export function sendWsMessage(message) {
  return new Promise((resolve) => {
    const socket = new WebSocket("ws://localhost:8000/ws");
    socket.onopen = () => {
      socket.send(JSON.stringify(message));
      socket.close();
      resolve();
    };
  });
}
