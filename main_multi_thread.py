
import time
import threading
import keyboard
import matplotlib.pyplot as plt
from autoCamera import capture
import os
from depth_map import calculate_depth_map

# getting the images
filename = "PHOTOS"
graycode_files = [os.path.join(filename, img) for img in os.listdir(filename) if img.endswith(".jpg")]
graycode_lock = threading.Lock()
process_event = threading.Event()
stop_event = threading.Event()

def capture_images():
    global graycode_files
    while not stop_event.is_set() and not process_event.is_set():
            print("Capturing")
            capture()
            time.sleep(1)

            with graycode_lock:
                graycode_files = [os.path.join(filename, img) for img in os.listdir(filename) if img.endswith(".jpg")]
                print(f"Captured {len(graycode_files)} images.")
            if len(graycode_files) == 16:
                print("16 images captured, setting process event.")
                process_event.set()  # Signal that processing can start



def process_depth_map():
    global graycode_files
    while not stop_event.is_set():
        process_event.wait()
        with graycode_lock:
            if len(graycode_files) == 16:
                print("Processing")
                process_event.clear()

        time.sleep(0.1)


if __name__ == "__main__":
    # Start capturing and processing in separate threads
    capture_thread = threading.Thread(target=capture_images)
    process_thread = threading.Thread(target=process_depth_map)

    # Start threads
    capture_thread.start()
    process_thread.start()

    # Main loop to keep the program running
    while True:
        if keyboard.is_pressed('s'):
            print("Stopping program...")
            stop_event.set()

            break
        time.sleep(0.1)
    capture_thread.join()  # Wait for the capture thread to finish
    process_thread.join()



