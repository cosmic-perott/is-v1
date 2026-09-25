import os
import socket
import time

esp32_ip = ""
port = 8888

file_path = ""

def watch_and_send():
    print(f"Connecting wirelessly to ESP32 at {esp32_ip}:{port}...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((esp32_ip, port))
        print("Connected to ESP32! Monitoring file for changes...")

        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                pass

        last_mtime = os.path.getmtime(file_path)

        while True:
            if os.path.exists(file_path):
                current_mtime = os.path.getmtime(file_path)
                
                if current_mtime > last_mtime:
                    last_mtime = current_mtime
                    
                    # Short pause to let the text editor finish writing completely
                    time.sleep(0.05)
                    
                    with open(file_path, "r") as file:
                        content = file.read()
                        
                    # Send every line found in the file
                    for line in content.splitlines():
                        clean_line = line.strip()
                        if clean_line:
                            print(f"Sending wirelessly: {clean_line}")
                            s.sendall((clean_line + "\n").encode("utf-8"))

            time.sleep(0.3)

    except KeyboardInterrupt:
        print("\n Stopped by user.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            s.close()
            print("Socket closed.")
        except:
            pass

if __name__ == "__main__":
    watch_and_send()
