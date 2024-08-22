import time
import threading

def display_loading_indicator(message, stop_event):
    print(message, end="", flush=True)
    while not stop_event.is_set():
        for dot in [".", ".", "."]:
            print(dot, end="", flush=True)
            if stop_event.wait(0.5):
                break
        print("\b\b\b   \b\b\b", end="", flush=True)
    print("\n")

def start_loading_indicator(message):
    stop_event = threading.Event()
    loading_thread = threading.Thread(target=display_loading_indicator, args=(message, stop_event))
    loading_thread.start()
    return stop_event, loading_thread

