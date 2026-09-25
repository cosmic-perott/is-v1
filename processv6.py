import os
import subprocess
import time
from datetime import datetime
from pynput import keyboard
from pynput.keyboard import Controller, Key
import pyautogui

file_path = "/Users/kimjunyoung/Desktop/COSMOS/SCOTT FREE/colors.txt"
raw_path = "/Users/kimjunyoung/Desktop/COSMOS/SCOTT FREE/raw.txt"
kb = Controller()
pyautogui.FAILSAFE = True

def run_native_automation(screenshot_path):
    print("🤖 Controlling your active Chrome browser...")
    
    # 1. Copy the screenshot image to the macOS clipboard as a TIFF picture
    abs_path = os.path.abspath(screenshot_path)
    applescript_copy = f'''
    set the clipboard to (read (POSIX file "{abs_path}") as TIFF picture)
    '''
    subprocess.run(["osascript", "-e", applescript_copy])
    
    # 2. Bring Google Chrome to the front and open your specific Gemini URL directly
    applescript_navigate = '''
    tell application "Google Chrome"
        activate
        if (count of windows) = 0 then
            make new window
        end if
        set URL of active tab of front window to "https://gemini.google.com/app/583345bccab410b9?hl=ko"
    end tell
    '''
    subprocess.run(["osascript", "-e", applescript_navigate])
    time.sleep(3.0) # Give the page a solid moment to fully load your specific chat session
    
    # 3. Focus Gemini's text box via JavaScript
    applescript_focus_box = '''
    tell application "Google Chrome"
        execute active tab javascript "
            let textBox = document.querySelectorAll('div[contenteditable=\\'true\\']');
            if (textBox.length > 0) {
                textBox[textBox.length - 1].focus();
            }
        "
    end tell
    '''
    subprocess.run(["osascript", "-e", applescript_focus_box])
    time.sleep(0.5)
    
    # 4. Paste the screenshot image into the chat box
    print("Pasting screenshot into Gemini...")
    with kb.pressed(Key.cmd):
        kb.press('v')
        kb.release('v')
    
    time.sleep(2) # Give image preview time to attach
    
    # 5. Type prompt and hit enter
    print("Typing prompt...")
    prompt_text = "SOLVE THE QUESTION. solve this multiple choice question. at the end of your answer just simply reply using A, B, C, or D\n"
    for char in prompt_text:
        kb.type(char)
        time.sleep(0.01)
        
    print("Waiting for Gemini's response (15 seconds)...")
    time.sleep(15) # Wait time
    
    # 6. Use PyAutoGUI to click the center of the window and do Cmd + A / Cmd + C
    print("Clicking center of window and copying raw page text via PyAutoGUI...")
    screen_width, screen_height = pyautogui.size()
    pyautogui.click(screen_width / 2, screen_height / 2)
    time.sleep(0.3)
    
    pyautogui.hotkey('command', 'a')
    time.sleep(0.3)
    pyautogui.hotkey('command', 'c')
    time.sleep(0.8)
    
    # 7. Read clipboard, write raw.txt (minus last line), and find the *most recent* A/B/C/D line for colors.txt
    clipboard_result = subprocess.run(["pbpaste"], capture_output=True, text=True)
    raw_text = clipboard_result.stdout.strip()
    
    if raw_text:
        lines = raw_text.splitlines()
        if lines:
            # Remove the last line for raw.txt
            raw_lines_to_write = lines[:-1]
            with open(raw_path, "w") as f:
                f.write("\n".join(raw_lines_to_write))
            print(f"✅ Raw webpage text written to raw.txt (last line omitted)!")
            
            # Search from the bottom up for the most recent single-letter line (A, B, C, or D)
            answer_found = None
            for line in reversed(lines):
                cleaned = line.strip().replace(".", "")
                if cleaned.upper() in ["A", "B", "C", "D"] and len(cleaned) == 1:
                    answer_found = cleaned.upper()
                    break
            
            if answer_found:
                with open(file_path, "w") as f:
                    f.write(answer_found + "\n")
                print(f"✅ Found most recent answer option '{answer_found}' and wrote to colors.txt!\n")
            else:
                print("⚠️ Could not find an isolated A, B, C, or D letter in the text.")
    else:
        print("⚠️ Could not read clipboard content.")

def take_screenshot():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshot_{timestamp}.png"
    
    subprocess.run(["screencapture", "-x", filename])
    print(f"Screenshot saved: {filename}")
    
    run_native_automation(filename)

def on_press(key):
    try:
        if key.char == 'm':
            take_screenshot()
    except AttributeError:
        pass

if __name__ == "__main__":
    print("Background PyAuto-Grabber active! Press 'm' anywhere to trigger. Press Ctrl+C to stop.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
