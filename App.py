import tkinter as tk
from tkinter import filedialog
from reportlab.pdfgen import canvas
from PIL import Image
import os

class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.image_paths = []
        self.output_pdf_name = tk.StringVar()  # Fixed undefined variable
        self.selected_image_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=10)

        self.initialize_ui()

    def initialize_ui(self):
        title_label = tk.Label(self.root, text="Image To PDF Converter", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        select_images_button = tk.Button(self.root, text="Select Images", command=self.select_images)
        select_images_button.pack(pady=(0, 10))

        self.selected_image_listbox.pack(pady=(0, 10), fill=tk.BOTH, expand=True)

        label = tk.Label(self.root, text="Enter output PDF name: ")
        label.pack()

        pdf_name_entry = tk.Entry(self.root, textvariable=self.output_pdf_name, width=40, justify='center')
        pdf_name_entry.pack()

        convert_button = tk.Button(self.root, text="Convert", command=self.convert_images_to_pdf)
        convert_button.pack(pady=(20, 40))

    def select_images(self):
        self.image_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image files", "*.jpg;*.jpeg;*.png;")])
        self.update_selected_images_listbox()

    def update_selected_images_listbox(self):
        self.selected_image_listbox.delete(0, tk.END)

        for image_path in self.image_paths:
            _, import_path = os.path.split(image_path)
            self.selected_image_listbox.insert(tk.END, import_path)

    def convert_images_to_pdf(self):
        if not self.image_paths:
            return

        output_pdf_path = self.output_pdf_name.get() + ".pdf" if self.output_pdf_name.get() else "output.pdf"

        pdf = canvas.Canvas(output_pdf_path, pagesize=(612, 792))

        for image_path in self.image_paths:
            img = Image.open(image_path)
            available_width = 540
            available_height = 792
            scale_factor = min(available_width / img.width, available_height / img.height)
            new_width = int(img.width * scale_factor)
            new_height = int(img.height * scale_factor)
            x_centered = (612 - new_width) / 2
            y_centered = (792 - new_height) / 2  # Fixed y centering

            pdf.setFillColorRGB(255, 255, 255)
            pdf.rect(0, 0, 612, 792, fill=True)
            pdf.drawInlineImage(img, x_centered, y_centered, new_width, new_height)
            pdf.showPage()

        pdf.save()

def main():
    root = tk.Tk()
    root.title("Image To PDF")
    converter = ImageToPDFConverter(root)
    root.geometry("450x600")
    root.mainloop()

if __name__ == "__main__":
    main()
