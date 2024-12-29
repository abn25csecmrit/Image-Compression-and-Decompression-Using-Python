import os
import PIL.Image
import PIL.ImageTk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import webbrowser

# The CompressorDecompressor class
class CompressorDecompressor:
    def __init__(self, root):
        self.window = root
        self.window.geometry("600x600")
        self.window.title("Image Compressor & Decompressor")
        self.window.configure(bg="white")
        self.window.resizable(width=True, height=True)

        # Center the window on the screen
        self.center_window()

        # Setting the image path Null initially
        self.imagePath = ''

        # Main frame to hold all widgets and center them
        main_frame = Frame(self.window, bg="white")
        main_frame.pack(expand=True, fill=BOTH)

        # Header Label
        headingLabel = Label(main_frame, text="Image Compressor & Decompressor", 
                             font=("Kokila", 18, "bold"), bg="white")
        headingLabel.pack(pady=20)

        # Frame for buttons and options
        button_frame = Frame(main_frame, bg="white")
        button_frame.pack(pady=10)

        # Button to select the Image
        selectButton = Button(button_frame, text="Select Image", 
                              font=("Helvetica", 10), bg="green", fg="white", command=self.Open_Image)
        selectButton.grid(row=0, column=0, padx=10)

        # Label for Image Quality
        imageQuality = Label(button_frame, text="Image Quality", 
                             font=("Times New Roman", 12), bg="white")
        imageQuality.grid(row=0, column=1, padx=10)

        # Image quality options
        imageQualityList = [10, 20, 30, 40, 50, 60, 70, 80]

        # Dropdown menu for image quality
        self.clicked = StringVar()
        self.clicked.set(80)
        qualityMenu = OptionMenu(button_frame, self.clicked, *imageQualityList)
        qualityMenu.config(width=2, font=("Helvetica", 9, "bold"), bg="gray50", fg="white")
        qualityMenu.grid(row=0, column=2, padx=10)

        # Frame for compress and decompress buttons
        action_frame = Frame(main_frame, bg="white")
        action_frame.pack(pady=10)

        # Button to compress the selected image
        compressButton = Button(action_frame, text="Compress Image", 
                                font=("Helvetica", 10), bg="yellow", fg="black", command=self.Compress_Image)
        compressButton.grid(row=0, column=0, padx=10)

        # Button to decompress the selected image
        decompressButton = Button(action_frame, text="Decompress Image", 
                                  font=("Helvetica", 10), bg="orange", fg="black", command=self.Decompress_Image)
        decompressButton.grid(row=0, column=1, padx=10)

        # Button to compress x-axis of the image
        compress_x_axis_button = Button(action_frame, text="Compress X-Axis", 
                                        font=("Helvetica", 10), bg="blue", fg="white", command=self.Compress_X_Axis)
        compress_x_axis_button.grid(row=0, column=2, padx=10)

        # Button to compress y-axis of the image
        compress_y_axis_button = Button(action_frame, text="Compress Y-Axis", 
                                        font=("Helvetica", 10), bg="purple", fg="white", command=self.Compress_Y_Axis)
        compress_y_axis_button.grid(row=0, column=3, padx=10)

        # Button to download the original image
        downloadButton = Button(action_frame, text="Download Original Image", 
                                font=("Helvetica", 10), bg="cyan", fg="black", command=self.Download_Original_Image)
        downloadButton.grid(row=0, column=4, padx=10)

        # Frame to display selected image and details
        self.frame = Frame(main_frame, bg="white", width=520, height=300)
        self.frame.pack(pady=20, expand=True, fill=BOTH)

        self.image_label = None
        self.size_label = None

    # Center the window on the screen
    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    # Open an Image through the filedialog widget
    def Open_Image(self):
        self.imagePath = filedialog.askopenfilename(initialdir="/", 
                                                    title="Select an Image", 
                                                    filetypes=(("Image files", "*.jpg *.jpeg *.png"),))

        # Display selected image and its size
        if len(self.imagePath) != 0:
            for widget in self.frame.winfo_children():
                widget.destroy()

            # Load and display the image
            img = PIL.Image.open(self.imagePath)
            img.thumbnail((250, 250))  # Resize for display
            img_tk = PIL.ImageTk.PhotoImage(img)
            
            self.image_label = Label(self.frame, image=img_tk)
            self.image_label.image = img_tk  # Keep a reference to avoid garbage collection
            self.image_label.pack()

            # Display the size of the image
            img_size_kb = os.path.getsize(self.imagePath) / 1024
            size_label_text = f"Size: {img_size_kb:.2f} KB"
            self.size_label = Label(self.frame, text=size_label_text, 
                                    font=("Times New Roman", 12), bg="white", fg="red")
            self.size_label.pack(pady=10)

    # Function to Compress the chosen image
    def Compress_Image(self):
        if len(self.imagePath) == 0:
            messagebox.showerror("Error", "Please Select an Image first")
        else:
            img = PIL.Image.open(self.imagePath)
            width, height = img.size
            img = img.resize((width, height), PIL.Image.LANCZOS)
            filename, extension = os.path.splitext(os.path.basename(self.imagePath))
            savetoPath = filedialog.askdirectory()
            resultFilename = f"{savetoPath}/{filename}-compressed.jpg"

            try:
                img = img.convert("RGB")
                img.save(resultFilename, quality=int(self.clicked.get()), optimize=True)
                messagebox.showinfo("Done!", "The Image has been compressed.")
                self.reset()

            except Exception as es:
                messagebox.showerror("Error", f"Error due to {es}")

    # Function to Decompress the chosen image
    def Decompress_Image(self):
        if len(self.imagePath) == 0:
            messagebox.showerror("Error", "Please Select an Image first")
        else:
            img = PIL.Image.open(self.imagePath)
            savetoPath = filedialog.askdirectory()
            resultFilename = f"{savetoPath}/{os.path.basename(self.imagePath).replace('-compressed', '')}"

            try:
                img.save(resultFilename, quality=100)  # Save the image with maximum quality
                messagebox.showinfo("Done!", "The Image has been decompressed.")
                self.reset()

            except Exception as es:
                messagebox.showerror("Error", f"Error due to {es}")

    # Function to compress the image along the x-axis
    def Compress_X_Axis(self):
        if len(self.imagePath) == 0:
            messagebox.showerror("Error", "Please Select an Image first")
        else:
            img = PIL.Image.open(self.imagePath)
            width, height = img.size
            new_width = width // 2  # Compress x-axis by half; adjust as needed
            img = img.resize((new_width, height), PIL.Image.LANCZOS)
            filename, extension = os.path.splitext(os.path.basename(self.imagePath))
            savetoPath = filedialog.askdirectory()
            resultFilename = f"{savetoPath}/{filename}-compressed-x.jpg"

            try:
                img = img.convert("RGB")
                img.save(resultFilename, quality=int(self.clicked.get()), optimize=True)
                messagebox.showinfo("Done!", "The Image has been compressed along the x-axis.")
                self.reset()

            except Exception as es:
                messagebox.showerror("Error", f"Error due to {es}")

    # Function to compress the image along the y-axis
    def Compress_Y_Axis(self):
        if len(self.imagePath) == 0:
            messagebox.showerror("Error", "Please Select an Image first")
        else:
            img = PIL.Image.open(self.imagePath)
            width, height = img.size
            new_height = height // 2  # Compress y-axis by half; adjust as needed
            img = img.resize((width, new_height), PIL.Image.LANCZOS)
            filename, extension = os.path.splitext(os.path.basename(self.imagePath))
            savetoPath = filedialog.askdirectory()
            resultFilename = f"{savetoPath}/{filename}-compressed-y.jpg"

            try:
                img = img.convert("RGB")
                img.save(resultFilename, quality=int(self.clicked.get()), optimize=True)
                messagebox.showinfo("Done!", "The Image has been compressed along the y-axis.")
                self.reset()

            except Exception as es:
                messagebox.showerror("Error", f"Error due to {es}")

    # Function to open the directory containing the original image
    def Download_Original_Image(self):
        if len(self.imagePath) == 0:
            messagebox.showerror("Error", "Please Select an Image first")
        else:
            directory = os.path.dirname(self.imagePath)
            webbrowser.open(f'file:///{directory}')

    # Reset function
    def reset(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.imagePath = ''
        self.image_label = None
        self.size_label = None

# Main function
if __name__ == "__main__":
    root = Tk()
    obj = CompressorDecompressor(root)
    root.mainloop()