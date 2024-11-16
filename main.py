import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageOps
import os

window_title = "ImageViewer"
window_size = "640x480"
window_icon_path = "icon.ico"
file_types = [("JPG", ".jpg"), ("BMP", ".bmp")]
thumbnail_size = (1024, 768)
load_text = " — Загрузка"

img_scale = 1.0
multiplier = 2
img_title = ""
img = None
img_path = None

def load_img(canvas, scrollbar_x, scrollbar_y):
    global img, img_path
    img_path = filedialog.askopenfilename(title="Выберите изображение", filetypes=file_types)
    if not img_path == "":
        try:
            img = Image.open(img_path)
            img.thumbnail(thumbnail_size)
            scale_func("drop")
            canvas_upd(canvas, scrollbar_x, scrollbar_y)
        except:
            messagebox.showerror("Ошибка", "Файл повреждён или имеет неизвестный формат.")

def canvas_upd(canvas, scrollbar_x, scrollbar_y):
    global img, img_path
    img_title = os.path.basename(img_path)
    title_text = f"{window_title} — {img_title} ({img_scale}x){load_text}"
    window.title(title_text)

    scaled_img = ImageOps.scale(img, img_scale)
    canvas.delete("all")
    canvas.img = ImageTk.PhotoImage(scaled_img)
    canvas.create_image(0, 0, anchor="nw", image=canvas.img)

    canvas.config(
        width=img.size[0],
        height=img.size[1],
        scrollregion=(0, 0, scaled_img.size[0], scaled_img.size[1])
    )

    scrollbar_x.config(command=canvas.xview)
    scrollbar_y.config(command=canvas.yview)
    window.title(title_text.replace(load_text, ""))
    canvas.pack(fill=BOTH)

def scale_func(func):
    global img_scale
    previous_scale = img_scale

    if func == "*":
        img_scale *= multiplier
        if img_scale > 10.0:
            img_scale = 10.0
    elif func == "/":
        img_scale /= multiplier
        if img_scale < 0.0625:
            img_scale = 0.0625
    elif func == "drop":
        img_scale = 1.0

    if img_scale != previous_scale:
        scale_apply()

def scale_apply():
    global img
    if img is not None:
        canvas_upd(canvas, scrollbar_x, scrollbar_y)

def btn_exit(window):
    window.destroy()

def btn_help():
    messagebox.showinfo("Справка", "Поддерживаемые форматы изображений: jpg, bmp.\nНажмите кнопку \"Приблизить\", чтобы увеличить текущий размер изображения вдвое. Кнопка \"Отдалить\" имеет обратный эффект. Максимальный коэффициент приближения = 10.\nПриближение и отдаление доступно также и через комбинацию Control и колеса мыши.\nСкроллить изображение можно при помощи колёсика мыши (прокрутка по горизонтали производится при помощи зажатой клавиши Alt и колеса мыши).\n\nИспользуемые технологии: Python 3.10.5, Pillow, Tkinter.")

def on_control_mouse_wheel(event):
    if not img == None:
        if event.delta > 0:
            scale_func("*")
        else:
            scale_func("/")

def on_mouse_wheel(event, dir):
    if not img == None:
        if dir == "y":
            if event.delta > 0:
                canvas.yview_scroll(-1, "units")
            else:
                canvas.yview_scroll(1, "units")
        elif dir == "x":
            if event.delta > 0:
                canvas.xview_scroll(-1, "units")
            else:
                canvas.xview_scroll(1, "units")

def main():
    global canvas, scrollbar_x, scrollbar_y, window
    window = Tk()
    window.title(window_title)
    window.geometry(window_size)
    try:
        window.iconbitmap(window_icon_path)
    except:
        print("Иконка не найдена.")

    window.bind('<Control-MouseWheel>', on_control_mouse_wheel)
    window.bind('<MouseWheel>', lambda event: on_mouse_wheel(event, "y"))
    window.bind('<Alt-MouseWheel>', lambda event: on_mouse_wheel(event, "x"))

    menu = Menu()
    options = Menu(tearoff=0)
    scale = Menu(tearoff=0)
    menu.add_cascade(label="Файл", menu=options)
    options.add_command(label="Открыть изображение", command=lambda:load_img(canvas, scrollbar_x, scrollbar_y))
    options.add_separator()
    options.add_command(label="Выйти", command=lambda:btn_exit(window))
    menu.add_cascade(label="Масштаб", menu=scale)
    scale.add_command(label="Приблизить", command=lambda:scale_func("*"))
    scale.add_command(label="Отдалить", command=lambda:scale_func("/"))
    scale.add_separator()
    scale.add_command(label="Исходный размер", command=lambda:scale_func("drop"))
    menu.add_cascade(label="Справка", command=btn_help)
    window.config(menu=menu)
    
    scrollbar_x = Scrollbar(window, orient="horizontal")
    scrollbar_x.pack(side=BOTTOM, fill=X)
    scrollbar_y = Scrollbar(window, orient="vertical")
    scrollbar_y.pack(side=RIGHT, fill=Y)

    canvas = tk.Canvas(
        window,
        xscrollcommand = scrollbar_x.set,
        yscrollcommand = scrollbar_y.set,
    )
    canvas.pack(fill=BOTH)

    window.mainloop()

main()