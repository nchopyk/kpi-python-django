
import tkinter.ttk as s
from tkinter import *
from data import *
from Lab1.Server.sqllite_db import DateBase

# ------window settings--------
root = Tk()
root.configure(bg=header_bg, width=500, height=700)
root.title("Window1")
root.resizable(width=False, height=False)
canvas = Canvas(root, height=600, width=890, bg=header_bg, highlightthickness=0)
canvas.pack()
canvas1 = Canvas(canvas, height=500, width=654, bg=content_bg, highlightthickness=0)
canvas2 = Canvas(canvas, height=0, width=0, bg=header_bg, highlightthickness=0)
window1 = canvas.create_window(220, 345, window=canvas1, anchor=W)
window2 = canvas.create_window(410, 186, window=canvas2, anchor=W)

# -----Custom scroll-bar settings--------
style = s.Style()
style.theme_use('clam')
style.configure("My.Vertical.TScrollbar", style.configure("Vertical.TScrollbar"))
style.configure("My.Vertical.TScrollbar", troughcolor=content_bg, background=accent_color,arrowcolor=header_bg, bordercolor=content_bg)
canvas_scroll = Canvas(canvas1, height=500, width=654, bg=content_bg, bd=0, highlightthickness=0)
scroll_y = s.Scrollbar(canvas1, orient="vertical", command=canvas_scroll.yview, style="My.Vertical.TScrollbar")

frame = Frame(canvas_scroll, bg=content_bg)
frame.pack(expand=True, fill='both')
canv_frame =Canvas(frame, bg=content_bg, bd=0, highlightthickness=0, width=654, height=500)
canv_frame.pack()

canvas_scroll.create_window(0, 0, anchor='nw', window=frame)
canvas_scroll.update_idletasks()
canvas_scroll.configure(scrollregion=canvas_scroll.bbox('all'), yscrollcommand=scroll_y.set)
canvas_scroll.grid(column=1, row=5)
scroll_y.grid(column=2, row=5, sticky=NS)

# -----------Creating User Interface Objects-----------

def delete_technique():
    for device in all_devices:
        device.update(True, False)

def edit_technique():
    for device in all_devices:
        device.update(False, True)

def show_technique():
    for device in all_devices:
        device.update(False, False)
def add():
    canv_frame.delete("all")
    canv_frame.config(height=475)
    Device("","","","","","","", 200, 100, canv_frame, db, update_canvas, True)






# ---------------Task Realizations----------------
db = DateBase("sqlite.db")

# db.add_technique("Холодильник","1","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","2","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","3","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","4","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","5","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","LG","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","LG","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","LG","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","LG","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","LG","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","LG","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","LG","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","LG","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","LG","100х200х30", "еконмний", "2000грн", "3000грн")

# db.add_technique("Холодильник","1","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","2","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","3","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","4","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","5","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","LG","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","LG","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","LG","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","LG","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","LG","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","LG","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","LG","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","LG","100х200х30", "еконмний", "2000грн", "3000грн")
# db.add_technique("Холодильник","LG","100х200х30", "еконмний", "2000грн", "3000грн")



print(0//3)
print(1//3)
print(2//3)
print(3%3)

all_devices = list()
def update_canvas(delete, edit):
    all_technique = db.get_all_technique()
    all_devices.clear()
    canv_frame.delete("all")
    print(all_technique)
    show_all_devices(db.get_all_technique())
    print("updated")

    if(all_technique):
        canv_frame.config(height=(165 + ((all_technique.index(all_technique[-1])) // 3) * 155))

    if(delete):
        delete_technique()
    if (edit):
        edit_technique()
    canvas_scroll.update_idletasks()
    canvas_scroll.configure(scrollregion=canvas_scroll.bbox('all'), yscrollcommand=scroll_y.set)

def show_all_devices( all_technique):
    for technique in all_technique:
        all_devices.append(Device(technique[0], technique[1], technique[2], technique[3], technique[4], technique[5], technique[6],
                                  10 + ((all_technique.index(technique)) % 3) * 215, 10 + ((all_technique.index(technique)) // 3) * 155,
                                  canv_frame, db, update_canvas))


canvas.create_line( 0, 68, 362, 68, 393, 36, 900, 36, fill=accent_color, width=3)

canvas.create_text(20, 35, anchor=W, font=('Helvetica','22','bold'), text="Бригада №27", fill=accent_color)
btn = HiTech_Chooser("Категорія", 410, 70, ["ціна", "марка", "витрати за рік", "клас ен.еф."], canvas, canvas2)
btn2 = Custom_Button(["Додати техніку","Вся наявна техніка","Видалення техніки","Редагування"], 10, 120, canvas, [add,show_technique,delete_technique,edit_technique], update_canvas)

update_canvas(False, False)


root.mainloop()