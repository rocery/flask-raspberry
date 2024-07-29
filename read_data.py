import csv
import socket

def read_csv(file_path):
    data = []
    with open(file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            data.append(row)
    # Ambil 5 data terakhir
    return data[-3:]

def read_csv_group(file_path):
    data = []
    with open(file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            data.append(row)
    # Ambil 5 data terakhir
    return data[-5:]

def get_external_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't have to be reachable
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "Unable to get IP address"
    finally:
        s.close()
    return ip