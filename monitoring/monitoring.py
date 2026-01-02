import requests
import websocket
import json
import threading
from enum import Enum, auto

class monitoring:
    class State(Enum):
        RUNNING=auto()
        PAUSED=auto()
        STOPPED=auto()

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.ws = None
        self.thread = None
        self.state = monitoring.State.STOPPED

    def on_open(self, ws):
        print("WebSocket connection opened")

        enable_page_events = {
            "id": 1,
            "method": "Target.setDiscoverTargets",
            "params": {"discover": True}
        }
        self.ws.send(json.dumps(enable_page_events))
        self.state = monitoring.State.RUNNING

    def on_error(self, ws, error):
        print(f"WebSocket error: {error}")
        self.state = monitoring.State.STOPPED

    def on_message(self, ws, message):
        if self.state == monitoring.State.PAUSED:
            print("Monitoring is paused. Ignoring message.")
            return

        res_json = json.loads(message)
        method = res_json.get('method')
        if not method == 'Target.targetInfoChanged':
            return
        
        param = res_json.get('params')
        type = param.get('targetInfo', {}).get('type')

        if not type == 'page':
            return
        
        url = param.get('targetInfo', {}).get('url')
        targetId = param.get('targetInfo', {}).get('targetId')

        if not (url and targetId):
            print("URL or Target ID not found in message")
            return

        self.close_youtube_tub(url, targetId)

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

    def stop_monitoring(self):
        if self.ws:
            self.ws.close()
        
        if self.thread:
            self.thread = None

    def pause_monitoring(self):
        if self.state == monitoring.State.RUNNING:
            self.state = monitoring.State.PAUSED
            print('Pausing monitoring...')
        elif self.state == monitoring.State.PAUSED:
            self.state = monitoring.State.RUNNING
            print('Resuming monitoring...')

    def close_youtube_tub(self, url, targetId):
        if not "youtube.com" in url:
            return
        
        close_command = {
            "id": 2,
            "method": "Target.closeTarget",
            "params": {"targetId": targetId}
        }
        self.ws.send(json.dumps(close_command))

