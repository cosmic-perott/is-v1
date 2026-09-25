import socket
import time

esp32_ip = ""  
port = 8888

file_path = ""

try:
  print(f"Connecting wirelessly to ESP32 at {esp32_ip}:{port}...")
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((esp32_ip, port))
  print("Connected!")

  with open(file_path, "r") as file:
    for line in file:
      clean_line = line.strip()
      if clean_line:
        print(f"Sending wirelessly: {clean_line}")
        s.sendall((clean_line + "\n").encode("utf-8"))
        time.sleep(1)  # 1-second delay between letters

  s.close()

except Exception as e:
  print(f" Error: {e}")
