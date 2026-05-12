# Chaos Chess Server

Run the API/WebSocket server:

```bash
cd server
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

WebSocket endpoint: ws://localhost:8000/ws
