import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk, Image
import pandas as pd
from exporters.pdf import PDFExporter
from exporters.excel import ExcelExporter
from loaders import FileLoader
from preprocessing import DataProcessor


class ComparativeStatementApp:
    """
    A class representing the main application window for the Comparative Statement tool.
    """

    def __init__(self, root):
        """
        Initialize the application window.

        Args:
            root (tk.Tk): The root window of the application.
        """
        self.root = root
        self.root.geometry("700x500")
        self.root.minsize(700, 500)
        self.root.maxsize(700, 500)
        self.root.title('Comparative Statement')

        self.create_widgets()

        self.pb = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=250, mode="determinate")
        self.pb.pack(pady=10)

    def create_widgets(self):
        """
        It creates the main elements of the UI
        """
        self.create_frames()
        self.load_images()
        self.create_labels()
        self.create_buttons()
        self.create_radiobuttons()

    def create_frames(self):
        """
        We create 3 frames for our position and orientation needs
        """
        self.frame1 = tk.Frame(self.root, relief='sunken')
        self.frame1.pack(fill=tk.BOTH, pady=30)
        
        self.frame2 = tk.Frame(self.root, relief='sunken')
        self.frame2.pack(fill=tk.BOTH, pady=30)
        
        self.frame3 = tk.Frame(self.root, relief='sunken')
        self.frame3.pack(fill=tk.BOTH, pady=30)
        
    def load_images(self):
        """
        it just loads branding information from the filesystem
        """
        self.img1 = Image.open("branding/logo1.png")
        self.resized_image1 = self.img1.resize((100, 100), Image.Resampling.LANCZOS)
        self.new_image1 = ImageTk.PhotoImage(self.resized_image1)

        self.img2 = Image.open("branding/logo2.png")
        self.resized_image2 = self.img2.resize((100, 100), Image.Resampling.LANCZOS)
        self.new_image2 = ImageTk.PhotoImage(self.resized_image2)
        
    def create_labels(self):
        """
        It creates the labels for the main window and pack them
        """
        label1 = tk.Label(self.frame1, image=self.new_image1)
        label1.pack(side='left', padx=30)

        label2 = tk.Label(self.frame1, text="COMPARATIVE STATEMENT TABLE", font="Helvetica 14 bold")
        label2.pack(side='left', padx=15)

        label3 = tk.Label(self.frame1, image=self.new_image2)
        label3.pack(side='left', padx=15)
        
        label4 = tk.Label(self.frame2, text="Click the Button to browse the Files", font=('Georgia 8'))
        label4.pack(pady=10)

    def create_buttons(self):
        open_button = ttk.Button(self.frame2, text="Open Files", cursor="hand2", command=self.open_file)
        open_button.pack(pady=20)

    def create_radiobuttons(self):
        self.var = tk.IntVar()

        excel_radio = tk.Radiobutton(self.frame3, text="Excel File", variable=self.var, value=1, command=self.show_excel_button)
        excel_radio.pack(anchor='center')

        pdf_radio = tk.Radiobutton(self.frame3, text="PDF File", variable=self.var, value=2, command=self.show_pdf_button)
        pdf_radio.pack(anchor='center')

        self.save_excel_button = tk.Button(self.frame3, text='Save As Excel', cursor="hand2", command=self.save_into_file)
        self.save_pdf_button = tk.Button(self.frame3, text='Save As PDF', cursor="hand2", command=self.save_into_file)

    def show_excel_button(self):
        """
        it toggles the save file button, hiding pdf and showing excel button
        """
        self.save_pdf_button.pack_forget()
        self.save_excel_button.pack()

    def show_pdf_button(self):
        """
        it toggles the save file button, hiding excel and showing pdf button
        """
        self.save_excel_button.pack_forget()
        self.save_pdf_button.pack()

    def open_file(self):
        """
        Open and process selected files.
        """
        files = filedialog.askopenfilenames()
        file_loader = FileLoader()
        try:
            df_dict = file_loader.load(files)
            self.output = DataProcessor().process_data(df_dict)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
        self.pb["value"] = 100
        messagebox.showinfo("Show Info", "Processing Completed!")
        
    def save_into_file(self):
        """
        It handles the file save related logic for both pdf & excel files
        """
        filename = "output"
        exporter = ExcelExporter(filename)
        if self.var.get() == 2:
            filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], initialfile=filename)
            exporter = PDFExporter(filename)
        else:
            filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")], initialfile=filename)
            exporter = ExcelExporter(filename)

        if not filename:
            messagebox.showwarning("cancelled", "File save operation cancelled")
            return

        exporter.export(self.output) 
        
        messagebox.showinfo("showinfo", "File Created Successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = ComparativeStatementApp(root)
    root.mainloop()
