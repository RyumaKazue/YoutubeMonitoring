from monitoring.monitoring import monitoring
from gui.main_window import main_window

class controller:
    def __init__(self):
        host = "localhost"
        port = 9222
        self.monitoring = monitoring(host, port)
        self.window = main_window("ui/main_window.ui")

        self.set_up()

    def on_start_and_pause_clicked(self):
        self.window.setStartAndPauseButtonHandler(self.monitoring.pause_monitoring)

    def on_stop_clicked(self):
        self.window.setStopButtonHandler(self.monitoring.stop_monitoring)

    def set_up(self):
        self.monitoring.appStateUpdateHandler = self.window.buttonTextUpdate
        self.monitoring.start_monitoring()
        
        self.on_start_and_pause_clicked()
        self.on_stop_clicked()

    def run(self):
        self.window.show()
        self.window.run()

