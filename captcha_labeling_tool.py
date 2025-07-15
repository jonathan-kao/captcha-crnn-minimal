import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import argparse
import shutil


class CaptchaLabelTool:
    def __init__(self, root, input_dir, output_dir):
        self.root = root
        self.input_dir = input_dir
        self.output_dir = output_dir

        self.root.title("Manual CAPTCHA Labeling Tool")

        self.images = self.get_unlabeled_images()
        self.index = 0

        self.image_label = tk.Label(root)
        self.image_label.pack()

        self.entry = tk.Entry(root, font=("Arial", 16), justify='center')
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.save_label)

        self.button = tk.Button(root, text="Save", command=self.save_label)
        self.button.pack()

        self.status = tk.Label(root, text="", font=("Arial", 10))
        self.status.pack(pady=5)

        self.load_image()

    def get_unlabeled_images(self):
        return sorted([f for f in os.listdir(self.input_dir)
                       if f.lower().endswith(".png") and f.split('.')[0].isdigit()])

    def load_image(self):
        if self.index >= len(self.images):
            self.image_label.config(image='')
            self.status.config(text="✅ All images have been labeled")
            self.entry.config(state='disabled')
            self.button.config(state='disabled')
            return

        img_path = os.path.join(self.input_dir, self.images[self.index])
        pil_img = Image.open(img_path)
        pil_img = pil_img.resize((200, 80))

        self.tk_img = ImageTk.PhotoImage(pil_img)
        self.image_label.config(image=self.tk_img)
        self.status.config(text=f"{len(self.images) - self.index} images remaining")
        self.entry.delete(0, tk.END)
        self.entry.focus()

    def save_label(self, event=None):
        label = self.entry.get().strip().lower()
        if len(label) != 4 or not label.isalpha():
            messagebox.showerror("Invalid Input", "Please enter 4 lowercase letters")
            return

        src = os.path.join(self.input_dir, self.images[self.index])
        dst = os.path.join(self.output_dir, f"{label}.png")

        if os.path.exists(dst):
            messagebox.showerror("Filename Conflict", f"A file named '{label}.png' already exists.\nSkipping to the next image.")
            self.index += 1
            self.load_image()
            return

        tmp_path = os.path.join(self.input_dir, f"{label}.png")
        os.rename(src, tmp_path)
        shutil.move(tmp_path, dst)

        print(f"✅ {self.images[self.index]} → {label}.png")
        self.index += 1
        self.load_image()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manual CAPTCHA Labeling Tool")
    parser.add_argument("--input", type=str, required=True, help="Path to the input directory containing unlabeled images")
    parser.add_argument("--output", type=str, required=True, help="Path to the output directory to save labeled images")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    root = tk.Tk()
    app = CaptchaLabelTool(root, args.input, args.output)
    root.mainloop()
