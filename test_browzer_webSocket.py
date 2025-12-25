import requests
import websocket
import json
import threading 
import keyboard

class YoutubeMonitor:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.ws = None
        self.thread = None
        self.running = False
        self.pausing = False

    def set_up_key(self):
        keyboard.add_hotkey('esc', self.stop_monitoring)
        keyboard.add_hotkey('space', self.pause)
        keyboard.wait('esc')

    def pause(self):
        self.pausing = not self.pausing

    def start_monitoring(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.connection)
            self.thread.daemon = True
            self.thread.start()

            self.set_up_key()


    def stop_monitoring(self):
        if self.running:
            self.running = False
            if self.ws:
                self.ws.close()
            self.thread.join()

    def connection(self):
        try:
            res = requests.get(f'http://{self.host}:{self.port}/json/version', timeout=5)
            json_data = res.json()
            websocket_url = json_data.get('webSocketDebuggerUrl')
            if websocket_url:
                self.ws = websocket.WebSocketApp(
                    websocket_url,
                    on_message=self.on_message,
                    on_error=self.on_error,
                    on_close=self.on_close,
                    on_open=self.on_open
                )

                self.ws.run_forever()

        except Exception as e:
            print(f"Error connecting to WebSocket: {e}")


    def on_message(self, ws, message):
        json_data = json.loads(message)

        method = json_data.get('method')

        info = json_data.get('params', {}).get('targetInfo')

        if info:
            type = info.get('type')

        if method == "Target.targetInfoChanged" and type == "page":
            url = info.get('url')
            targetId = info.get('targetId')
            print(url)        
            if not self.pausing:
                self.close_youtube_tub(url, targetId)

    def on_error(self, ws, error):
        print(f"WebSocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket connection closed")

    def on_open(self, ws):
        print("WebSocket connection opened")
        enable_page_events = {
            "id": 1,
            "method": "Target.setDiscoverTargets",
            "params": {"discover": True}
        }
        self.ws.send(json.dumps(enable_page_events))

    def close_youtube_tub(self, url, targetId):
        if not "youtube.com" in url:
            return
        
        close_command = {
            "id": 2,
            "method": "Target.closeTarget",
            "params": {"targetId": targetId}
        }
        self.ws.send(json.dumps(close_command))

if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 9222

    monitor = YoutubeMonitor(HOST, PORT)
    monitor.start_monitoring()