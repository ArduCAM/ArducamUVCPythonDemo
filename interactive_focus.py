import subprocess
import time
import sys
import termios
import tty
import re

device = "/dev/video0"
focus = 300
step = 50
min_focus = 1
max_focus = 1023

def set_focus(focus_val):
    subprocess.run(f"v4l2-ctl -d {device} -c focus_automatic_continuous=0", shell=True)
    subprocess.run(f"v4l2-ctl -d {device} -c focus_absolute={focus_val}", shell=True)

def get_focus():
    # Run the command to get current focus value
    result = subprocess.run(f"v4l2-ctl -d {device} --get-ctrl=focus_absolute",
                            shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        match = re.search(r"focus_absolute:\s*(\d+)", result.stdout)
        if match:
            return int(match.group(1))
    return None

def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch += sys.stdin.read(2)
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def main():
    global focus, step
    print("Manual Focus Control Tool")
    print("w: Increase | s: Decrease | t: Set step | c: Check current focus | q: Quit")

    set_focus(focus)

    while True:
        print(f"\rCurrent Focus: {focus:>4d} | Step: {step:>2d}   ", end='', flush=True)
        key = get_key()

        if key == 'w':  # Increase
            focus = min(focus + step, max_focus)
            set_focus(focus)
        elif key == 's':  # Decrease
            focus = max(focus - step, min_focus)
            set_focus(focus)
        elif key.lower() == 't':  # Set new step
            try:
                new_step = int(input("\nEnter new step size (integer): "))
                if new_step > 0:
                    step = new_step
            except ValueError:
                print("Invalid step size.")
        elif key.lower() == 'c':  # Show current focus
            current = get_focus()
            if current is not None:
                print(f"\nCurrent focus_absolute: {current}")
                focus = current  # update internal value
            else:
                print("\nUnable to read current focus.")
        elif key.lower() == 'q':
            print("\nExiting manual focus control.")
            break

        time.sleep(0.1)

if __name__ == "__main__":
    main()
