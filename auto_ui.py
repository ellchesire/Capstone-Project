import tkinter as tk
from PIL import Image, ImageTk
import cv2
import keyboard
from autoCamera import capture
import os
import time
from depth_map import calculate_depth_map
import threading
from tkinter import messagebox

class SimpleVideoImageDisplayApp:
    def __init__(self, root, filename):
        self.root = root
        self.root.title("Structured 3D Light Scanner")

        self.filename = filename

        #events
        self.process_event = threading.Event()
        self.stop_event = threading.Event()

        # Styling
        self.root.configure(bg='black')  # Background color of the window
        frame_style = {'relief': 'sunken', 'borderwidth': 5, 'bg': 'darkgray'}
        title_font = ("Arial", 18, "bold")
        title_bg = "gray"
        title_fg = "white"

        # Set up the layout: two panels side by side
        self.video_panel = tk.Label(root, **frame_style)
        self.video_panel.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        self.image_panel = tk.Label(root, **frame_style)
        self.image_panel.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

        #adding a button
        self.button = tk.Button(root,
                           text="Save Plot",
                           command=self.button_clicked,
                           activebackground="green",
                           activeforeground="white",
                           anchor="center",
                           bd=3,
                           bg="lightgray",
                           cursor="hand2",
                           disabledforeground="gray",
                           fg="black",
                           font=("Arial", 12),
                           height=2,
                           highlightbackground="black",
                           highlightcolor="green",
                           highlightthickness=2,
                           justify="center",
                           overrelief="raised",
                           padx=10,
                           pady=5,
                           width=15,
                           wraplength=100)

        self.button.grid(row=2, column=1, sticky="se", padx=20, pady=20)


        # Adding titles
        self.video_title = tk.Label(root, text="Video", font=title_font, bg=title_bg, fg=title_fg)
        self.video_title.grid(row=0, column=0, sticky="ew")

        self.image_title = tk.Label(root, text="Depth Map", font=title_font, bg=title_bg, fg=title_fg)
        self.image_title.grid(row=0, column=1, sticky="ew")


        # Configure columns and rows to take equal space
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.graycode_files = []

        # Load video and image
        self.image_path = "depth_map_output.jpg"
        self.load_video()
        self.load_image()


        self.capture_thread = threading.Thread(target=self.capture_photos, daemon= True)
        self.process_thread = threading.Thread(target=self.process_images, daemon= True)

        # Start threads
        self.capture_thread.start()
        self.process_thread.start()



    def load_video(self):
        self.cap = cv2.VideoCapture(0)
        self.play_video()

    def play_video(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(frame, (600, 400))  # Resize to fit the UI
            cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv_image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_panel.imgtk = imgtk
            self.video_panel.configure(image=imgtk)
            self.root.after(33, self.play_video)  # Continue to the next frame


    def load_image(self):
        image = Image.open(self.image_path)
        image = image.resize((600, 400))  # Resize to fit the UI
        photo = ImageTk.PhotoImage(image)
        self.image_panel.photo = photo
        self.image_panel.configure(image=photo)

    def capture_photos(self):
        while not self.stop_event.is_set():
            print("Capturing")
            capture(self.cap)
            self.process_event.set()
            self.graycode_files = [os.path.join(self.filename, img) for img in os.listdir(self.filename) if img.endswith(".jpg")]
            if len(self.graycode_files) == 16:
                print("16 images captured, setting process event.")
                self.process_event.set()
                time.sleep(6)

    def process_images(self):
        while not self.stop_event.is_set():
            self.process_event.wait(timeout=1)

            if len(self.graycode_files) == 16:
                print("Processing")
                now = time.time()
                calculate_depth_map(self.graycode_files)
                end = time.time()
                elapsed_time = end - now
                print(elapsed_time)
                print("Done Processing")

                # for name in os.listdir(self.filename):
                #     if name.endswith('.jpg'):
                #         os.remove(os.path.join(self.filename, name))
                #         print(f"Deleted: {name}")

                self.load_image()
                self.process_event.clear()

    def button_clicked(self):

        img = Image.open(self.image_path)
        user_dir = os.path.expanduser("~")
        save_path = os.path.join(user_dir, f"Downloads/SavedPlot_{time.time()}.jpg")


        try:
            img.save(save_path, "JPEG")
            messagebox.showinfo("Success", f"Plot saved at:\n{save_path}")

        except Exception as e:
            # Show an error message if something goes wrong
            messagebox.showerror("Error", f"Could not save Plot:\n{str(e)}")


def main():
    filename = "PHOTOS"

    root = tk.Tk()
    root.geometry("1280x600")  # Adjust the size of the window as needed
    app = SimpleVideoImageDisplayApp(root, filename)

    root.mainloop()


if __name__ == "__main__":
    main()
