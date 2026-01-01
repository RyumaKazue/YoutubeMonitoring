from monitoring.monitoring import monitoring

if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 9222

    monitor = monitoring(HOST, PORT)
    monitor.start_monitoring()