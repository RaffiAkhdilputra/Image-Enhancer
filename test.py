import numpy as np
import matplotlib.pyplot as plt
import cv2

def get_ax_size(ax, fig):
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height
    width *= fig.dpi
    height *= fig.dpi
    return width, height

def generate_image():
    data = np.arange(9).reshape((3, 3))
    fig = plt.figure(figsize=(8, 6), dpi=80)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(data, aspect='equal')
    plt.close(fig)

# Generate the image
generate_image()

# Load the image using OpenCV
img = cv2.imread('image.jpg', cv2.IMREAD_UNCHANGED)

# Resize to fit smaller screen (optional)
img = cv2.resize(img, (640, 480))

# Show the image
cv2.imshow('Matrix Heatmap', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
