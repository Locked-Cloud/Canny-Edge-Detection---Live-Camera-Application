import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time

class EnhancedCannyCameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Live Camera - Canny Edge Detection")
        self.root.geometry("1200x700")
        self.root.configure(bg="#1a1a1a")
        self.root.resizable(True, True)

        self.running = False
        self.cap = None
        self.frame = None
        self.fps = 0

        # ---------------- GUI Layout ----------------
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Arial", 12), padding=6)
        style.configure("TScale", background="#1a1a1a")

        # Frame for video previews
        preview_frame = tk.Frame(self.root, bg="#1a1a1a")
        preview_frame.pack(pady=10)

        # Live camera display
        self.original_label = tk.Label(preview_frame, bg="#1a1a1a")
        self.original_label.grid(row=0, column=0, padx=20)

        # Canny edge display
        self.edge_label = tk.Label(preview_frame, bg="#1a1a1a")
        self.edge_label.grid(row=0, column=1, padx=20)

        # FPS Display
        self.fps_label = tk.Label(self.root, text="FPS: 0", fg="white", bg="#1a1a1a", font=("Arial", 12))
        self.fps_label.pack(pady=5)

        # Controls Frame
        controls = tk.Frame(self.root, bg="#1a1a1a")
        controls.pack()

        self.start_btn = ttk.Button(controls, text="Start Camera", command=self.start_camera)
        self.start_btn.grid(row=0, column=0, padx=10, pady=10)

        self.stop_btn = ttk.Button(controls, text="Stop Camera", command=self.stop_camera)
        self.stop_btn.grid(row=0, column=1, padx=10, pady=10)

        # Threshold sliders
        self.th1 = tk.IntVar(value=100)
        self.th2 = tk.IntVar(value=200)

        tk.Label(controls, text="Threshold 1", fg="white", bg="#1a1a1a").grid(row=1, column=0)
        self.slider1 = ttk.Scale(controls, from_=0, to=255, variable=self.th1, orient="horizontal")
        self.slider1.grid(row=2, column=0, padx=10, pady=5)

        tk.Label(controls, text="Threshold 2", fg="white", bg="#1a1a1a").grid(row=1, column=1)
        self.slider2 = ttk.Scale(controls, from_=0, to=255, variable=self.th2, orient="horizontal")
        self.slider2.grid(row=2, column=1, padx=10, pady=5)

    # ---------------- Camera Thread ----------------
    def camera_loop(self):
        prev_time = time.time()

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            # Resize for performance
            frame = cv2.resize(frame, (640, 480))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Apply Canny
            edges = cv2.Canny(gray, self.th1.get(), self.th2.get())

            # Update FPS
            now = time.time()
            self.fps = round(1 / (now - prev_time), 1)
            prev_time = now

            # Convert to Tkinter images
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)

            self.frame_original = ImageTk.PhotoImage(Image.fromarray(rgb))
            self.frame_edges = ImageTk.PhotoImage(Image.fromarray(edges_rgb))

            # Update GUI
            self.original_label.configure(image=self.frame_original)
            self.edge_label.configure(image=self.frame_edges)
            self.fps_label.configure(text=f"FPS: {self.fps}")

        # Cleanup after stop
        self.cap.release()

    # ---------------- Start Camera ----------------
    def start_camera(self):
        if not self.running:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Error: Camera not found")
                return

            self.running = True
            threading.Thread(target=self.camera_loop, daemon=True).start()

    # ---------------- Stop Camera ----------------
    def stop_camera(self):
        self.running = False

# ----------------------------------------------------
# Main App
# ----------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedCannyCameraApp(root)
    root.mainloop()
