
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
    global graycode_filess
    while not stop_event.is_set():
            print("Capturing")
            capture()

            with graycode_lock:
                graycode_files = [os.path.join(filename, img) for img in os.listdir(filename) if img.endswith(".jpg")]
                print(f"Captured {len(graycode_files)} images.")
            if len(graycode_files) == 16:
                print("16 images captured, setting process event.")
                process_event.set()
                time.sleep(5)



def process_depth_map():
    global graycode_files
    while not stop_event.is_set():
        process_event.wait(timeout=1)
        with graycode_lock:
            if len(graycode_files) == 16:
                print("Processing")
                calculate_depth_map(graycode_files)
                print("Done Processing")
                process_event.clear()

        time.sleep(0.1)



if __name__ == "__main__":

    capture_thread = threading.Thread(target=capture_images)
    process_thread = threading.Thread(target=process_depth_map)

    # Start threads
    capture_thread.start()
    process_thread.start()


    keyboard.wait('s')
    stop_event.set()

    capture_thread.join()
    process_thread.join()


    print("Exiting...")


