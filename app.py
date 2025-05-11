import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2 as cv
import os
from tkinter import filedialog
import customtkinter as ctk

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Processing App")
        self.master.geometry("1200x800")
        self.master.resizable(False, False)
        self.master.grid_columnconfigure([0, 1], weight=1)
        
        # Frame
        self.frame_1 = ctk.CTkFrame(self.master)
        self.frame_1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.frame_2 = ctk.CTkFrame(self.master)
        self.frame_2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Button Frame
        self.frame = ctk.CTkFrame(self.frame_1, fg_color="transparent")
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame.pack(pady=20)

        # Buttons
        self.button1 = ctk.CTkButton(self.frame, text="Load Image", command=self.load_image)
        self.button1.grid(row=0, column=0, padx=10)

        self.button2 = ctk.CTkButton(self.frame, text="Enhance Image")
        self.button2.grid(row=0, column=1, padx=10)

        # Image display
        self.img_container = ctk.CTkFrame(self.frame_1)
        self.img_container.pack(pady=20)

        self.canvas = ctk.CTkCanvas(self.img_container, width=400, height=400)
        self.canvas.pack()
        
        self.input_frame = ctk.CTkFrame(self.frame_1, fg_color="transparent")
        self.input_frame.pack(pady=20)

        frame_x = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        frame_x.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        frame_y = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        frame_y.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        self.label = ctk.CTkLabel(self.input_frame, text="Enter X Coordinate")
        self.label.grid(row=0, column=0, padx=10)
        self.x_input_1 = ctk.CTkEntry(frame_x, placeholder_text="X1 Coordinate")
        self.x_input_1.grid(row=0, column=0, padx=10)
        self.x_input_2 = ctk.CTkEntry(frame_x, placeholder_text="X2 Coordinate")
        self.x_input_2.grid(row=0, column=1, padx=10)

        self.x_label = ctk.CTkLabel(self.input_frame, text="x")
        self.x_label.grid(row=1, column=1, padx=10)

        self.label2 = ctk.CTkLabel(self.input_frame, text="Enter Y Coordinate")
        self.label2.grid(row=0, column=2, padx=10)

        self.y_input_1 = ctk.CTkEntry(frame_y, placeholder_text="Y1 Coordinate")
        self.y_input_1.grid(row=1, column=2, padx=10)
        self.y_input_2 = ctk.CTkEntry(frame_y, placeholder_text="Y2 Coordinate")
        self.y_input_2.grid(row=1, column=3, padx=10)

        self.button3 = ctk.CTkButton(self.frame_1, text="Crop Image", command=self.crop_image)
        self.button3.pack(pady=20)

    def load_image(self):        
        self.input_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.input_path:
            if hasattr(self, 'image_plot'):
                self.image_plot.get_tk_widget().destroy()
                self.image_plot = None

            self.image = cv.imread(self.input_path)
            self.image = cv.cvtColor(self.image, cv.COLOR_BGR2RGB)

            self.image_plot = FigureCanvasTkAgg(plt.Figure(figsize=(4, 4), dpi=100), master=self.canvas)
            self.image_plot.get_tk_widget().pack(side="top", fill="both", expand=True)
            self.ax = self.image_plot.figure.add_subplot(111)
            self.ax.imshow(self.image)
            self.ax.set_title("Original Image")
            self.ax.set(xlabel="px", ylabel="px")

    def crop_image(self):
        if hasattr(self, 'image'):
            try:
                h, w, _ = self.image.shape

                # Get user input and convert to integers
                x1 = int(self.x_input_1.get())
                y1 = int(self.y_input_1.get())
                x2 = int(self.x_input_2.get())
                y2 = int(self.y_input_2.get())

                # Ensure x1 < x2 and y1 < y2
                x1, x2 = sorted([x1, x2])
                y1, y2 = sorted([y1, y2])

                # Clip values to image bounds
                x1 = max(0, min(x1, w))
                x2 = max(0, min(x2, w))
                y1 = max(0, min(y1, h))
                y2 = max(0, min(y2, h))

                cropped_image = self.image[y1:y2, x1:x2]

                # Update plot
                self.ax.clear()
                self.ax.imshow(cropped_image)
                self.ax.set_title("Cropped Image")
                self.ax.set(xlabel="px", ylabel="px")
                self.image_plot.draw()
            except Exception as e:
                print("Error during cropping:", e)


if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()