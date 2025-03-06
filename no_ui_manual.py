import cv2
import time
import numpy as np
import pickle

from isapi.simple import SimpleExtension

from decode_gray import  decoding_main
import keyboard
import matplotlib.pyplot as plt
from autoCamera import capture
import os
from depth_map import triangulate_points
from depth_map import calculate_depth_map
from ui import SimpleVideoImageDisplayApp
import tkinter as tk

#getting the images
#filename = "old_pictures/feb_12th"
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
            now = time.time()
            points = calculate_depth_map(graycode_files)
            elapstedtime = time.time() - now
            print(elapstedtime)

            img = cv2.imread(graycode_files[0])
            cv2.imwrite(real_filename,img)

            for name in os.listdir(filename):
                if name.endswith('.jpg'):
                    os.remove(os.path.join(filename, name))
                    print(f"Deleted: {name}")
        else:
            print("No Images in Folder")

        app.load_image()

        time.sleep(0.1)