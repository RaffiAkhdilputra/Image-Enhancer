import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2 as cv
from tkinter import filedialog
import customtkinter as ctk

class App:
    def __init__(self, master):
        self.image = None
        self._brightness_proccess = list()
        self._sharpness_proccess = list()

        self.master = master
        self.master.title("Image Enhancer App")
        self.master.geometry("1500x710")
        self.master.resizable(False, False)
        self.master.grid_columnconfigure([0, 1], weight=1)
        
        # Frame
        self.frame_1 = ctk.CTkFrame(self.master)
        self.frame_1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.frame_2 = ctk.CTkScrollableFrame(self.master)
        self.frame_2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # FRAME 1

        # Button Frame
        self.frame = ctk.CTkFrame(self.frame_1, fg_color="transparent")
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame.pack(pady=20)

        # Buttons
        self.button1 = ctk.CTkButton(self.frame, text="Load Image", command=self.load_image)
        self.button1.grid(row=0, column=0, padx=10)

        self.button2 = ctk.CTkButton(self.frame, text="Enhance Image", command=self.enhance_image)
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

        # FRAME 2
        label = ctk.CTkLabel(self.frame_2, text="Image Enhanced with Brightness Method")
        label.pack(pady=20)

        self.tab_1 = ctk.CTkTabview(self.frame_2, width=400, height=400)
        self.tab_1.pack(pady=20, padx=20, fill="both", expand=True)

        label = ctk.CTkLabel(self.frame_2, text="Image Enhaced with Sharpness Method")
        label.pack(pady=20)

        self.tab_2 = ctk.CTkTabview(self.frame_2, width=400, height=400)
        self.tab_2.pack(pady=20, padx=20, fill="both", expand=True)

        self.tab_1.add("View Transformation")
        self.tab_1.add("Output")
        self.tab_2.add("View Transformation")
        self.tab_2.add("Output")

        output_tab_1 = self.tab_1.tab("Output")
        view_tab_1 = self.tab_1.tab("View Transformation")

        self.brightness_frame = ctk.CTkFrame(output_tab_1, fg_color="transparent")
        self.brightness_frame.pack(pady=20)

        self.brightness_canvas = ctk.CTkCanvas(self.brightness_frame, width=300, height=300)
        self.brightness_canvas.pack()

        output_tab_2 = self.tab_2.tab("Output")
        view_tab_2 = self.tab_2.tab("View Transformation")

        self.sharpness_frame = ctk.CTkFrame(output_tab_2, fg_color="transparent")
        self.sharpness_frame.pack(pady=20)

        self.sharpness_canvas = ctk.CTkCanvas(self.sharpness_frame, width=300, height=300)
        self.sharpness_canvas.pack()

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
            self.ax.set_title("Original Image")
            self.ax.imshow(self.image)

            self._brightness_proccess.append(self.image.copy())
            self._sharpness_proccess.append(self.image.copy())

    def crop_image(self):
        if hasattr(self, 'image'):
            try:
                h, w, _ = self.image.shape

                x1 = int(self.x_input_1.get())
                y1 = int(self.y_input_1.get())
                x2 = int(self.x_input_2.get())
                y2 = int(self.y_input_2.get())

                x1, x2 = sorted([x1, x2])
                y1, y2 = sorted([y1, y2])

                x1 = max(0, min(x1, w))
                x2 = max(0, min(x2, w))
                y1 = max(0, min(y1, h))
                y2 = max(0, min(y2, h))

                self.image = self.image[y1:y2, x1:x2]
                self._brightness_proccess[0] = self.image.copy()
                self._sharpness_proccess[0] = self.image.copy()

                # Update plot
                self.ax.clear()
                self.ax.imshow(self.image)
                self.image_plot.draw()
            except Exception as e:
                print("Error during cropping:", e)

    def enhance_image(self):
        base_image = self.image.copy()
        brightness_enhancement = cv.convertScaleAbs(base_image, alpha=1.5, beta=0)
        sharpness_enhancement = cv.addWeighted(base_image, 1.5, base_image, -0.5, 0)

        self._brightness_proccess.append(brightness_enhancement)
        self._sharpness_proccess.append(sharpness_enhancement)
        
        self.brightness_canvas = FigureCanvasTkAgg(plt.Figure(figsize=(3, 3), dpi=100), master=self.brightness_frame)
        self.brightness_canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        self.brightness_ax = self.brightness_canvas.figure.add_subplot(111)
        self.brightness_ax.set_title("Brightness Enhancement")
        self.brightness_ax.imshow(brightness_enhancement)
        self.brightness_canvas.draw()

        self.sharpness_canvas = FigureCanvasTkAgg(plt.Figure(figsize=(3, 3), dpi=100), master=self.sharpness_frame)
        self.sharpness_canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        self.sharpness_ax = self.sharpness_canvas.figure.add_subplot(111)
        self.sharpness_ax.set_title("Sharpness Enhancement")
        self.sharpness_ax.imshow(sharpness_enhancement)
        self.sharpness_canvas.draw()

        print(self._brightness_proccess)
        print(self._sharpness_proccess)
        
if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()