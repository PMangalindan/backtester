from datetime import datetime

def log_to_file(message):
    filename = "targetedLogs.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a") as file:
        file.write(f"[{timestamp}] {message}\n")




dictio = {'x':1, 'y':2}

log_to_file(dictio)
