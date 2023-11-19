import cv2, sys, io
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
from tkinter import messagebox
import os
import tkinter as tk
from tkinter import filedialog
import math
import UI

def fix_xy_direction(event):
    global fix_flag
    if event.keysym == "Shift_L":
        fix_flag = 1

def start_measurement(event):
    global start_x, start_y, is_measurement_started, current_line
    if current_line:
        canvas.delete(current_line)
    start_x, start_y = event.x, event.y
    is_measurement_started = True
    current_line = None  # 現在の直線を初期化

def update_measurement(event):
    global is_measurement_started, current_line, distance_nm
    global fix_flag
    global end_x, end_y
    global current_x, current_y
    
    current_x, current_y = event.x, event.y
    if is_measurement_started:
        end_x, end_y = event.x, event.y
        distance = 0
        
        if current_line:
            canvas.delete(current_line)
        
        if fix_flag:
            if abs(end_x - start_x) > abs(end_y - start_y):
                # 水平方向の距離を計算
                distance = abs(end_x - start_x)
                current_line = canvas.create_line(start_x, start_y, end_x, start_y, arrow=tk.BOTH, tags="line", fill="cyan")
            else:
                # 垂直方向の距離を計算
                distance = abs(end_y - start_y)
                current_line = canvas.create_line(start_x, start_y, start_x, end_y, arrow=tk.BOTH, tags="line", fill="cyan")
        else:
            distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
            current_line = canvas.create_line(start_x, start_y, end_x, end_y, arrow=tk.BOTH, tags="line", fill="cyan")
            
        try:
            distance_nm = distance*UI.pixelsize*ratio
        except Exception as e:
            print(e)
            print("each aspect ratio for the width and the height does not coincide!")
        
        distance_label.config(text=f"distance: {distance_nm:.2f} nm")
    
    update_mag_image()

def end_measurement(event):
    global is_measurement_started, current_line, fix_flag
    is_measurement_started = False
    fix_flag = 0
    
num = 0
def add_list(event):
    global num, current_line, fix_flag
    global start_x, start_y, end_x, end_y
    
    if not is_measurement_started:
        num = num + 1
        list_box.insert(tk.END,f"{num} : {distance_nm:.2f} nm")
        if fix_flag:
            if abs(end_x - start_x) > abs(end_y - start_y):
                # 水平方向の距離を計算
                canvas.create_line(start_x, start_y, end_x, start_y, arrow=tk.BOTH, tags="line", fill="red")
            else:
                # 垂直方向の距離を計算
                canvas.create_line(start_x, start_y, start_x, end_y, arrow=tk.BOTH, tags="line", fill="red")
        else:
            canvas.create_line(start_x, start_y, end_x, end_y, arrow=tk.BOTH, tags="line", fill="red")
        canvas.create_text((start_x+end_x)/2, (start_y+end_y)/2,text=str(num),anchor="se",fill="yellow")
    
    
mag = 2
def update_mag_image():
    global ori_mag_image, mag_img_label,current_x, current_y, root_sub, mag
    
    #cross
    cross_length = 10
    cross_color = 255
    center_x = 200
    center_y = 200
    
    new_height = int(photo_height*mag)
    new_width = int(photo_width*mag)
    
    ori_mag_image = image_pil.resize((new_width, new_height), Image.LANCZOS)
    new_mag_image = ori_mag_image.crop((int(mag*current_x-200),int(mag*current_y-200),int(mag*current_x+200),int(mag*current_y+200)))
    
    draw = ImageDraw.Draw(new_mag_image)
    draw.line([(center_x - cross_length, center_y), (center_x + cross_length, center_y)], fill=cross_color, width=2)
    draw.line([(center_x, center_y - cross_length), (center_x, center_y + cross_length)], fill=cross_color, width=2)

    new_mag_photo = ImageTk.PhotoImage(new_mag_image ,master=root_sub)
    mag_img_label.config(image=new_mag_photo)
    mag_img_label.image = new_mag_photo
    
def on_mouse_wheel(event):
    global mag
    if event.delta > 0:
        mag += 1
    elif mag > 1:
        mag -= 1
    else:
        mag = 1
    update_mag_image()
    
def save_image():
    postscript_file = canvas.postscript(colormode="color")
    image = Image.open(io.BytesIO(postscript_file.encode("utf-8")))
    ret = filedialog.asksaveasfilename(defaultextension=[".png"],initialdir=os.getcwd())
    image.save(ret, "PNG")
    
def Quit():
    root.withdraw()
    root.quit()
    root_sub.withdraw()
    root_sub.quit()
    sys.exit()

def on_closing():
    root.destroy()
    root_sub.destroy()
    sys.exit()

fix_flag = 0

root = tk.Tk()
root.title("SEMT Desktop SEM image viewer")
image_pil = Image.open(UI.image_path.get())
image_pil_resized = image_pil.resize((640, 480))
ratio_w = image_pil.width/640
ratio_h = image_pil.height/480
if ratio_h == ratio_w:
    ratio = ratio_h
print("ratio_w",ratio_w, "ratio_h",ratio_h) 
photo = ImageTk.PhotoImage(image=image_pil_resized, master=root)
canvas = tk.Canvas(root, width=photo.width(), height=photo.height())
print("width : ", photo.width(), "height : ", photo.height())
canvas.config(cursor="cross")
canvas.create_image(0, 0, anchor=tk.NW, image=photo)

root.bind("<KeyPress>", fix_xy_direction)
canvas.bind("<Button-2>", add_list)
canvas.bind("<Button-1>", start_measurement)
canvas.bind("<Motion>", update_measurement)
canvas.bind("<ButtonRelease-1>", end_measurement)

distance_label = tk.Label(root, text="")
#distance_label.pack()

quit_btn = ttk.Button(root, text="quit",command=lambda:Quit())

#save_btn = tk.Button(root, text="Save data", command=lambda:save_image())
#magnified image
root_sub = tk.Tk()
root_sub.title("SEMT Magnified image")
photo_height = photo.height()
photo_width = photo.width()
new_height = photo_height*mag
new_width = photo_width*mag

ori_mag_image = image_pil.resize((new_width, new_height), Image.LANCZOS)
mag_image = ori_mag_image.crop((0,0,400,400))
mag_photo = ImageTk.PhotoImage(mag_image, master=root_sub)
mag_img_label = ttk.Label(root_sub, image=mag_photo)
mag_img_label.pack()
root.bind("<MouseWheel>", on_mouse_wheel)

list_box = tk.Listbox(root, width=50,height=25)
list_label = ttk.Label(root, text="Measured distances:")

canvas.grid(row=1, column=0)
list_box.grid(row=1, column=1)
list_label.grid(row=0, column=1)
distance_label.grid(row=2, column=0)
quit_btn.grid(row=3, column=0)
#save_btn.grid(row=3, column=1)
is_measurement_started = False  # 測定が開始されているかどうかのフラグ
current_line = None  # 現在の直線を格納する変数

root.protocol("WM_DELETE_WINDOW", on_closing)
root_sub.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
root_sub.mainloop()