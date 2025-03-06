import tkinter as tk
from PIL import Image, ImageTk
import cv2

class SimpleVideoImageDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video and Image Viewer")

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

        # Adding titles
        self.video_title = tk.Label(root, text="Original Video", font=title_font, bg=title_bg, fg=title_fg)
        self.video_title.grid(row=0, column=0, sticky="ew")

        self.image_title = tk.Label(root, text="Depth Map", font=title_font, bg=title_bg, fg=title_fg)
        self.image_title.grid(row=0, column=1, sticky="ew")

        # Configure columns and rows to take equal space
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        # Load video and image
        self.video_path = "real_images/gymnasts.mp4"
        self.image_path = "depth_map_output.jpg"
        self.load_video()
        self.load_image()

    def load_video(self):
        self.cap = cv2.VideoCapture(self.video_path)
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
        else:
            self.cap.release()  # Release the capture when video is over but keep last frame displayed

    def load_image(self):
        image = Image.open(self.image_path)
        image = image.resize((600, 400))  # Resize to fit the UI
        photo = ImageTk.PhotoImage(image)
        self.image_panel.photo = photo
        self.image_panel.configure(image=photo)

def main():
    root = tk.Tk()
    root.geometry("1280x720")  # Adjust the size of the window as needed
    app = SimpleVideoImageDisplayApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
