import asyncio
import websockets
import json
import threading
from loopback import start_loopback, stop_loopback

PORT = 8765
CLIENTS = set()

async def handle_connection(websocket):
    print("✅ Client connected")
    CLIENTS.add(websocket)
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                command = data.get("command")
                if command == "start-recording":
                    print("🎙️ Start command received.")
                    threading.Thread(target=start_loopback, daemon=True).start()
                elif command == "stop-recording":
                    print("🛑 Stop command received.")
                    stop_loopback()
                else:
                    print("⚠️ Unknown command.")
            except Exception as e:
                print("❌ Error processing message:", e)
    except websockets.exceptions.ConnectionClosed:
        print("❌ Client disconnected")
    finally:
        CLIENTS.remove(websocket)

async def main():
    print(f"🌐 WebSocket server running on ws://localhost:{PORT}")
    async with websockets.serve(handle_connection, "localhost", PORT):
        await asyncio.Future()  # Keep server alive

if __name__ == "__main__":
    asyncio.run(main())
