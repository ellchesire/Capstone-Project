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
graycode_files = [os.path.join(filename, img) for img in os.listdir(filename) if img.endswith(".jpg")]

f = open('camera_calibration', 'rb')
cam_mtx = pickle.load(f)
f.close()

f = open('projector_calibration', 'rb')
proj_mtx = pickle.load(f)
f.close()

f = open('extrinsic_matrix', 'rb')
R_saved = pickle.load(f)
T_saved = pickle.load(f)
f.close()

R_saved = np.ascontiguousarray(R_saved, dtype=np.float32)
T_saved = np.ascontiguousarray(T_saved, dtype=np.float32)


if __name__ == "__main__":

    while True:

        if keyboard.is_pressed('c'):
            print("Capturing")
            capture()
            graycode_files = [os.path.join(filename, img) for img in os.listdir(filename) if img.endswith(".jpg")]
            time.sleep(0.5)

        elif len(os.listdir(filename)) != 0:

            points = calculate_depth_map(graycode_files)
            depth_map = points[:, :, 2]

            plt.figure(figsize=(8, 6))
            plt.imshow(depth_map, cmap='jet', interpolation='nearest')
            plt.colorbar(label="depth")
            plt.title("depth map")
            plt.savefig("depth_map_output.jpg")
            plt.show()

            for name in os.listdir(filename):
                if name.endswith('.jpg'):
                    os.remove(os.path.join(filename, name))
                    print(f"Deleted: {name}")
        else:
            print("Capture More Images")

        time.sleep(0.1)