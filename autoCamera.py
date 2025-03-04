import cv2
import time
import os

def capture_images(cap, num_photos=16, interval=0, folder='captures'):
    os.makedirs(folder, exist_ok=True)  # Create folder if it doesn't exist
    
    for i in range(num_photos):
        ret, frame = cap.read()
        if not ret:
            print(f"Error: Could not capture image {i+1}")
            break
        
        filename = f"{folder}_b{i+1}.jpg"
        cv2.imwrite(f"{folder}//{filename}", frame)
        print(f"Captured {filename}")
        
        time.sleep(interval)

def capture():
    bits = 16
    interval = 0
    second_interval = 8

    # Open the default camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit

    time_start = time.time()
    capture_images(cap, bits, interval, "PHOTOS")
    #capture_images(cap, bits, second_interval, "PHOTOS")
    time_end = time.time()

    elapsed_time = time_end - time_start
    print("Elapased Time: " + str(elapsed_time))

    # Free Camera Resources
    cap.release()
    cv2.destroyAllWindows()


# MAIN FUNCTION
# if __name__ == "__main__":
#
#     bits = 8
#     interval = 0
#
#     # Open the default camera
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         print("Error: Could not open camera.")
#         exit
#
#     time_start = time.time()
#     capture_images(cap, bits, interval, "GCV")
#     capture_images(cap, bits, interval, "GCH")
#     time_end = time.time()
#
#     elapsed_time = time_end - time_start
#     print("Elapased Time: " + str(elapsed_time))
#
#     # Free Camera Resources
#     cap.release()
#     cv2.destroyAllWindows()