#!/usr/bin/env python3
#
#
# Windows to show images in a folder

import sys
import PIL.Image as Image
import tkinter as tk
from tkinter import filedialog, messagebox, Label
from PIL import ImageTk
import os

# show images in a folder with image centered in the window
# allows to navigate through images with left and right arrow keys
def show_images(directory):
    if not os.path.isdir(directory):
        messagebox.showerror("Error", f"Directory '{directory}' does not exist.")
        return
    images = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    if not images:
        messagebox.showerror("Error", f"No images found in directory '{directory}'.")
        return
    images.sort()  # Sort images to have a consistent order
    root = tk.Tk()
    root.title("Image Viewer")
    root.geometry("800x600")
    # window background transparency
    root.wm_attributes('-alpha', 0.3)
    root.configure(background="#0a0a0a")
    current_image_index = 0
    image_label = Label(root)
    image_label.pack(expand=True)
    def load_image(index):
        nonlocal current_image_index
        image_path = os.path.join(directory, images[index])
        img = Image.open(image_path)
        img.thumbnail((800, 600), Image.Resampling.LANCZOS)  # Resize image to fit window
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk  # Keep a reference to avoid garbage collection
        current_image_index = index
    def next_image(event):
        nonlocal current_image_index
        if current_image_index < len(images) - 1:
            load_image(current_image_index + 1)
    def prev_image(event):  
        nonlocal current_image_index
        if current_image_index > 0:
            load_image(current_image_index - 1)
    root.bind("<Right>", next_image)
    root.bind("<Left>", prev_image)
    
    # show the first image
    load_image(current_image_index)
    # start the main loop
    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python getWallpaper.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    show_images(directory)
    sys.exit(0)
# End of getWallpaper.py