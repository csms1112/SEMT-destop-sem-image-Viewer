import tkinter as tk
import sys
import os
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import messagebox

#ファイル選択ダイアログ用関数
def file_select(image_path):
    global img_files, multi_mode, pixelsize, file_path
    img_files = []
    
    ftyp = [("Image files (png, jpg, bmp)","*.png;*.jpeg;*.jpg;*.bmp"), ("All files","*.*")]
    file_path = filedialog.askopenfilename(filetypes=ftyp)
    if os.path.exists(file_path):
        image_path.set(file_path)
        try:
            text_file = file_path[:-4] + ".txt"
            with open(text_file, "r") as f:
                lines = f.readlines()
                
            for line in lines:
                if line.startswith("PixelSize"):
                    pixelsize = float(line.split("=")[1]) #nm
            
            #print(pixelsize)
            f.close()
        except Exception as e:
            messagebox.showerror("ERROR!",e)
            sys.exit()

def Quit():
    root.withdraw()
    root.quit()
    sys.exit()
    
def store_file_path():
    if os.path.exists(image_path.get()):    
        root.withdraw()
        root.quit()
    else:
        messagebox.showinfo("Info","Select the valid file path.")

#ファイル選択ダイアログ
multi_mode = 0
select_flag = 0
root = tk.Tk()
root.title("SEMT")
icon_image = tk.PhotoImage(file="SEMT_icon.png")
root.iconphoto(True, icon_image)

logo = Image.open("SEMT logo.png")

resized_width = 300
aspect_ratio = float(logo.height)/float(logo.width)
resized_height = int(resized_width * aspect_ratio)

resized_logo = logo.resize((resized_width, resized_height), Image.ANTIALIAS)
PIlogo = ImageTk.PhotoImage(resized_logo, master=root)
logo_label = ttk.Label(root, text="Desktop SEM image viewer ver. 2.1.1 beta",
                       font=("Times New Roman",15),
                       image=PIlogo,
                       compound="top")

image_label = ttk.Label(root, text="SEM image path:")
image_path = tk.StringVar()
image_entry = ttk.Entry(root, textvariable = image_path, width=50)
select_btn = ttk.Button(root, text="select...", command=lambda:file_select(image_path))

copyright_label = ttk.Label(root, text="© 2023 Nao Harada All rights reserved.")

start_btn = ttk.Button(root, text="start", command=lambda:store_file_path())
clear_btn = ttk.Button(root, text="clear", command=lambda:image_path.set(""))
quit_btn = ttk.Button(root, text="quit", command=lambda:Quit())

#layout
logo_label.grid(row=0, column=1,pady=20)

image_label.grid(row=1, column=0,padx=20, pady=20)
image_entry.grid(row=1, column=1)
select_btn.grid(row=1, column=2,padx=20)

start_btn.grid(row=2, column=0,padx=10, pady=10)
clear_btn.grid(row=2, column=1)
quit_btn.grid(row=2, column=2,padx=10)

copyright_label.grid(row=3, column=1)

root.mainloop()