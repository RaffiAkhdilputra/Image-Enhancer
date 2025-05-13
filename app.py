import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2 as cv
from tkinter import filedialog
import customtkinter as ctk

class App:
    def __init__(self, master):
        self.brightness_after_id = None
        self.sharpness_after_id = None
        self.MAX_STEPS = 5
        self.brightness_step = 1
        self.sharpness_step = 1
        self.brightness_animation_label = None
        self.sharpness_animation_label = None
        self.brightness_canvas = None
        self.sharpness_canvas = None
        self._brightness_proccess = []
        self._sharpness_proccess = []

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

        btn_frame = ctk.CTkFrame(self.frame_1, fg_color="transparent")
        btn_frame.pack(pady=20)

        self.button3 = ctk.CTkButton(btn_frame, text="Crop Image", command=self.crop_image)
        self.button3.grid(row=0, column=0, padx=10)

        self.button4 = ctk.CTkButton(btn_frame, text="Reset", command=self.reset)
        self.button4.grid(row=0, column=1, padx=10)

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

        self.output_brightness_frame = ctk.CTkFrame(output_tab_1)
        self.output_brightness_frame.pack(pady=20)

        self.view_brightness_frame = ctk.CTkFrame(view_tab_1)
        self.view_brightness_frame.pack(pady=20)

        output_tab_2 = self.tab_2.tab("Output")
        view_tab_2 = self.tab_2.tab("View Transformation")

        self.output_sharpness_frame = ctk.CTkFrame(output_tab_2)
        self.output_sharpness_frame.pack(pady=20)

        self.view_sharpness_frame = ctk.CTkFrame(view_tab_2)
        self.view_sharpness_frame.pack(pady=20)

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

            if len(self._brightness_proccess) != 0:
                self._brightness_proccess[:].pop()
                self._sharpness_proccess[:].pop()

            self._brightness_proccess = [self.image.copy()]
            self._sharpness_proccess = [self.image.copy()]

            if hasattr(self, 'brightness_canvas') and self.brightness_canvas is not None:
                self.brightness_canvas.get_tk_widget().destroy()
                self.brightness_canvas = None
                self.brigthness_histogram_btn.destroy()
                self.brightness_download_btn.destroy()

                self.tf_brigthness_canvas.get_tk_widget().destroy()
                self.tf_brigthness_canvas = None
                self.stop_brightness_slideshow()

            if hasattr(self, 'sharpness_canvas') and self.sharpness_canvas is not None:
                self.sharpness_canvas.get_tk_widget().destroy()
                self.sharpness_canvas = None
                self.sharpness_histogram_btn.destroy()
                self.sharpness_download_btn.destroy()

                self.tf_sharpness_canvas.get_tk_widget().destroy()
                self.tf_sharpness_canvas = None
                self.stop_sharpness_slideshow()

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

                if len(self._brightness_proccess) != 1:
                    self._brightness_proccess[:].pop()
                    self._sharpness_proccess[:].pop()
                
                self._brightness_proccess = [self.image.copy()]
                self._sharpness_proccess = [self.image.copy()]

                self.ax.clear()
                self.ax.imshow(self.image)
                self.image_plot.draw()
            except Exception as e:
                print("Error during cropping:", e)

    def reset(self):
        if hasattr(self, 'image'):
            self.image = cv.imread(self.input_path)
            self.image = cv.cvtColor(self.image, cv.COLOR_BGR2RGB)

            self.ax.clear()
            self.ax.imshow(self.image)
            self.image_plot.draw()

            if len(self._brightness_proccess) != 0:
                self._brightness_proccess[:].pop()
                self._sharpness_proccess[:].pop()

            self._brightness_proccess = [self.image.copy()]
            self._sharpness_proccess = [self.image.copy()]

        if hasattr(self, 'brightness_canvas') and self.brightness_canvas is not None:
            self.brightness_canvas.get_tk_widget().destroy()
            self.brightness_canvas = None
            self.brigthness_histogram_btn.destroy()
            self.brightness_download_btn.destroy()

            self.stop_brightness_slideshow()
            self.tf_brigthness_canvas.get_tk_widget().destroy()
            self.tf_brigthness_canvas = None

        if hasattr(self, 'sharpness_canvas') and self.sharpness_canvas is not None:
            self.sharpness_canvas.get_tk_widget().destroy()
            self.sharpness_canvas = None
            self.sharpness_histogram_btn.destroy()
            self.sharpness_download_btn.destroy()

            self.stop_sharpness_slideshow()
            self.tf_sharpness_canvas.get_tk_widget().destroy()
            self.tf_sharpness_canvas = None

    def enhance_image(self):
        for i in range(self.MAX_STEPS):
            bright_img = self.brightness_enhancement(self.image.copy(), i)
            sharp_img = self.sharpness_enhancement(self.image.copy(), i)

            self._brightness_proccess.append(bright_img)
            self._sharpness_proccess.append(sharp_img)

        if isinstance(self.brightness_canvas, FigureCanvasTkAgg):
            self.brightness_canvas.get_tk_widget().destroy()
            self.brightness_canvas = None

        if isinstance(self.sharpness_canvas, FigureCanvasTkAgg):
            self.sharpness_canvas.get_tk_widget().destroy()
            self.sharpness_canvas = None

        # Brightness canvas
        self.brightness_canvas = FigureCanvasTkAgg(plt.Figure(figsize=(3, 3), dpi=100), master=self.output_brightness_frame)
        self.brightness_canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        self.brightness_ax = self.brightness_canvas.figure.add_subplot(111)
        self.brightness_ax.set_title("Brightness Enhancement")
        self.brightness_ax.imshow(self._brightness_proccess[4])
        self.brightness_ax.axis("off")
        self.brightness_canvas.draw()

        frame = ctk.CTkFrame(self.output_brightness_frame, fg_color="transparent")
        frame.pack(pady=20)
        self.brigthness_histogram_btn = ctk.CTkButton(frame, text="Show Histogram", command=lambda:self.show_histogram(self._brightness_proccess[self.MAX_STEPS-1]))
        self.brigthness_histogram_btn.grid(row=0, column=0, padx=10)
        self.brightness_download_btn = ctk.CTkButton(frame, text="Download", command=lambda:self.download_image(self._brightness_proccess[self.MAX_STEPS-1]))
        self.brightness_download_btn.grid(row=0, column=1, padx=10)

        # Sharpness canvas
        self.sharpness_canvas = FigureCanvasTkAgg(plt.Figure(figsize=(3, 3), dpi=100), master=self.output_sharpness_frame)
        self.sharpness_canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        self.sharpness_ax = self.sharpness_canvas.figure.add_subplot(111)
        self.sharpness_ax.set_title("Sharpness Enhancement")
        self.sharpness_ax.imshow(self._sharpness_proccess[4])
        self.sharpness_ax.axis("off")
        self.sharpness_canvas.draw()

        frame = ctk.CTkFrame(self.output_sharpness_frame, fg_color="transparent")
        frame.pack(pady=20)
        self.sharpness_histogram_btn = ctk.CTkButton(frame, text="Show Histogram", command=lambda:self.show_histogram(self._sharpness_proccess[self.MAX_STEPS-1]))
        self.sharpness_histogram_btn.grid(row=0, column=0, padx=10)

        self.sharpness_download_btn = ctk.CTkButton(frame, text="Download", command=lambda:self.download_image(self._sharpness_proccess[self.MAX_STEPS-1]))
        self.sharpness_download_btn.grid(row=0, column=1, padx=10)

        # print(self._brightness_proccess)
        # print(self._sharpness_proccess)

        # View Transformation
        # Brigthness
        self.tf_brigthness_canvas = FigureCanvasTkAgg(plt.Figure(figsize=(3, 3), dpi=100), master=self.view_brightness_frame)
        self.tf_brigthness_canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        self.tf_brightness_ax = self.tf_brigthness_canvas.figure.add_subplot(111)
        self.tf_brightness_ax.set_title("Brightness Transformation")

        self.start_brightness_slideshow()

        # Sharpness
        self.tf_sharpness_canvas = FigureCanvasTkAgg(plt.Figure(figsize=(3, 3), dpi=100), master=self.view_sharpness_frame)
        self.tf_sharpness_canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        self.tf_sharpness_ax = self.tf_sharpness_canvas.figure.add_subplot(111)
        self.tf_sharpness_ax.set_title("Sharpness Transformation")

        self.start_sharpness_slideshow()

    def brightness_enhancement(self, base_img, step:int):
        alpha = 1.0
        beta = step * 25
        return cv.convertScaleAbs(base_img, alpha=alpha, beta=beta)
        
    def sharpness_enhancement(self, base_img, step:int):
        # factor = 1.0 + (step * 0.2)
        # return cv.addWeighted(base_img, factor, base_img, -0.5, 0)
        
        blurred = cv.GaussianBlur(base_img, (3, 3), 0)

        amount = 0.5 + (step * 2)
        sharpened = cv.addWeighted(base_img, 1 + amount, blurred, -amount, 0)

        sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
        return sharpened

    def start_brightness_slideshow(self, step=0):
        if not self._brightness_proccess:
            return

        step %= self.MAX_STEPS
        self.tf_brightness_ax.clear()
        self.tf_brightness_ax.set_title("Brightness Transformation")
        self.tf_brightness_ax.axis("off")
        self.tf_brightness_ax.imshow(self._brightness_proccess[step])
        self.tf_brigthness_canvas.draw()

        self.brightness_after_id = self.master.after(500, lambda: self.start_brightness_slideshow(step + 1))


    def start_sharpness_slideshow(self, step=0):
        if not self._sharpness_proccess:
            return

        step %= self.MAX_STEPS
        self.tf_sharpness_ax.clear()
        self.tf_sharpness_ax.set_title("Sharpness Transformation")
        self.tf_sharpness_ax.axis("off")
        self.tf_sharpness_ax.imshow(self._sharpness_proccess[step])
        self.tf_sharpness_canvas.draw()

        self.sharpness_after_id = self.master.after(1000, lambda: self.start_sharpness_slideshow(step + 1))

    def stop_brightness_slideshow(self):
        if self.brightness_after_id is not None:
            self.master.after_cancel(self.brightness_after_id)
            self.brightness_after_id = None

    def stop_sharpness_slideshow(self):
        if self.sharpness_after_id is not None:
            self.master.after_cancel(self.sharpness_after_id)
            self.sharpness_after_id = None

    def show_histogram(self, image):
        if hasattr(self, 'histogram_canvas') and self.histogram_canvas is not None:
            widget = self.histogram_canvas.get_tk_widget()
            if widget.winfo_exists():
                widget.destroy()
            self.histogram_canvas = None

        fig, ax = plt.subplots(1, 2, figsize=(10, 5), dpi=100, tight_layout=True)

        ax[0].set_title("Original Histogram")
        ax[0].hist(self.image.ravel(), bins=256, range=[0, 256], color='blue')

        ax[1].set_title("Result Histogram")
        ax[1].hist(image.ravel(), bins=256, range=[0, 256], color='gray')

        new_window = ctk.CTkToplevel(self.master)
        new_window.title("Histogram")

        self.histogram_canvas = FigureCanvasTkAgg(fig, master=new_window)
        self.histogram_canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        self.histogram_canvas.draw()

    def download_image(self, image):
        try:
            download_path = filedialog.asksaveasfilename(
                defaultextension=".png", 
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")]
            )
            if download_path:
                cv.imwrite(download_path, cv.cvtColor(image, cv.COLOR_RGB2BGR))
        except Exception as e:
            print("Error during download:", e)

if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()