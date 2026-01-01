import requests
import websocket
import json
import threading
import keyboard

class monitoring:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.ws = None
        self.thread = None

        keyboard.add_hotkey('esc', self.stop_monitoring)

    def on_open(self, ws):
        print("WebSocket connection opened")

        enable_page_events = {
            "id": 1,
            "method": "Target.setDiscoverTargets",
            "params": {"discover": True}
        }
        self.ws.send(json.dumps(enable_page_events))

    def on_error(self, ws, error):
        print(f"WebSocket error: {error}")

    def on_message(self, ws, message):
        res_json = json.loads(message)
        print(f"Received message: {res_json}")

    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket connection closed")

    def server_connecting(self):
        res = requests.get(f'http://{self.host}:{self.port}/json/version', timeout=5)
        res_json = res.json()
        
        webSocket_debugger_url = res_json.get("webSocketDebuggerUrl")
        if not webSocket_debugger_url:
            print("Error: webSocketDebuggerUrl not found")
            return

        self.ws = websocket.WebSocketApp(webSocket_debugger_url,
                                            on_open=self.on_open,
                                            on_message=self.on_message,
                                            on_error=self.on_error,
                                            on_close=self.on_close)
        
        print("Connecting to WebSocket...")
        self.ws.run_forever()

    def start_monitoring(self):
        print("Starting monitoring...")
        self.thread = threading.Thread(target=self.server_connecting)
        self.thread.daemon = True
        self.thread.start()

        keyboard.wait()

    def stop_monitoring(self):
        if self.ws:
            self.ws.close()
        
        if self.thread:
            self.thread = None

    def close_youtube_tub(self, url, targetId):
        if not "youtube.com" in url:
            return
        
        close_command = {
            "id": 2,
            "method": "Target.closeTarget",
            "params": {"targetId": targetId}
        }
        self.ws.send(json.dumps(close_command))

