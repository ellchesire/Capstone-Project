import cv2
import time
import numpy as np
import pickle
from decode_gray import  decoding_main
import keyboard
import matplotlib.pyplot as plt
from autoCamera import capture
import os
from depth_map import triangulate_points
from depth_map import calculate_depth_map

#getting the images
filename = "PHOTOS"
real_filename = "real_images/first.jpg"
graycode_files = [os.path.join(filename, img) for img in os.listdir(filename) if img.endswith(".jpg") or img.endswith(".JPG")]


if __name__ == "__main__":

    while True:

        if keyboard.is_pressed('c'):
            print("Capturing")
            capture()
            graycode_files = [os.path.join(filename, img) for img in os.listdir(filename) if img.endswith(".jpg")]
            time.sleep(0.5)
        if keyboard.is_pressed('s'):
            print("Goodbye!")
            break

        elif len(os.listdir(filename)) != 0:
            print("Processing")
            points = calculate_depth_map(graycode_files)
            # depth_map = points[:, :, 2]
            #
            # plt.figure(figsize=(8, 6))
            # plt.imshow(depth_map, cmap='jet', interpolation='nearest')
            # plt.colorbar(label="depth")
            # plt.title("depth map")
            # plt.savefig("depth_map_output.jpg")
            # plt.show()
            img = cv2.imread(graycode_files[0])
            cv2.imwrite(real_filename,img)

            for name in os.listdir(filename):
                if name.endswith('.jpg'):
                    os.remove(os.path.join(filename, name))
                    print(f"Deleted: {name}")
        else:
            print("No Images in Folder")

        time.sleep(0.1)