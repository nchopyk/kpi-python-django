import tkinter.ttk as s
from tkinter import *
from data import *
from Lab1.Server.sqlite_db import DateBase
from Lab1.Server.postgres_db import PostgresDb
from Lab1.Server.mysql_db import MysqlDb

# ------window settings--------
root = Tk()
root.configure(bg=header_bg, width=500, height=700)
root.title("Window1")
root.resizable(width=False, height=False)
canvas = Canvas(root, height=600, width=890, bg=header_bg, highlightthickness=0)
canvas.pack()
canvas1 = Canvas(canvas, height=500, width=654, bg=content_bg, highlightthickness=0)
window1 = canvas.create_window(220, 345, window=canvas1, anchor=W)

# -----Custom scroll-bar settings--------
style = s.Style()
style.theme_use('clam')
style.configure("My.Vertical.TScrollbar", style.configure("Vertical.TScrollbar"))
style.configure("My.Vertical.TScrollbar", troughcolor=content_bg, background=accent_color, arrowcolor=header_bg, bordercolor=content_bg)
canvas_scroll = Canvas(canvas1, height=500, width=654, bg=content_bg, bd=0, highlightthickness=0)
scroll_y = s.Scrollbar(canvas1, orient="vertical", command=canvas_scroll.yview, style="My.Vertical.TScrollbar")

# Creating widgets to display main content
frame = Frame(canvas_scroll, bg=content_bg)
frame.pack(expand=True, fill='both')
canv_frame = Canvas(frame, bg=content_bg, bd=0, highlightthickness=0, width=654, height=500)
canv_frame.pack()

canvas_scroll.create_window(0, 0, anchor='nw', window=frame)
canvas_scroll.update_idletasks()
canvas_scroll.configure(scrollregion=canvas_scroll.bbox('all'), yscrollcommand=scroll_y.set)
canvas_scroll.grid(column=1, row=5)
scroll_y.grid(column=2, row=5, sticky=NS)


def delete_technique():
    """A function to switch each device object
    into delete mode"""
    for device in all_devices:
        device.update(True, False)


def edit_technique():
    """A function to switch each device object
    into edit mode"""
    for device in all_devices:
        device.update(False, True)


def show_technique():
    """A function to display each device object
    without any mode"""
    for device in all_devices:
        device.update(False, False)


def add():
    """A function to create device object
    in add mode"""
    canv_frame.delete("all")
    canv_frame.config(height=475)
    Device("", "", "", "", "", "", "", 200, 100, canv_frame, db, update_canvas, True)


def update_canvas(delete, edit, d_b2=False, d_b3=False):
    """A function to update the content on the canvas"""

    if (not d_b2 and not d_b3):
        all_technique = db.get_all_technique()
    elif (d_b2):
        all_technique = db2.get_all_records()
    else:
        all_technique = db3.get_all_records()
    all_devices.clear()
    canv_frame.delete("all")
    print(all_technique)
    show_all_devices(all_technique, d_b2, d_b3)
    print("updated")
    if (all_technique):
        canv_frame.config(height=(165 + ((all_technique.index(all_technique[-1])) // 3) * 155))
    if (delete):
        delete_technique()
    if (edit):
        edit_technique()
    canvas_scroll.update_idletasks()
    canvas_scroll.configure(scrollregion=canvas_scroll.bbox('all'), yscrollcommand=scroll_y.set)


def show_all_devices(all_technique, db2, db3):
    """A function to show each device object
    """
    if (not db2 and not db3):
        for technique in all_technique:
            all_devices.append(Device(technique[0], technique[1], technique[2], technique[3], technique[4], technique[5], technique[6],
                                      10 + ((all_technique.index(technique)) % 3) * 215, 10 + ((all_technique.index(technique)) // 3) * 155,
                                      canv_frame, db, update_canvas))
    elif (db2):
        for technique in all_technique:
            all_devices.append(Db2_Device(technique[1], technique[2], technique[4], technique[6],
                                          10 + ((all_technique.index(technique)) % 3) * 215, 10 + ((all_technique.index(technique)) // 3) * 155,
                                          canv_frame))
    else:
        for technique in all_technique:
            all_devices.append(Db2_Device(technique[1], technique[2], technique[3], technique[4],
                                          10 + ((all_technique.index(technique)) % 3) * 215, 10 + ((all_technique.index(technique)) // 3) * 155,
                                          canv_frame))


# ---------------Task Realizations----------------
db = DateBase("sqlite.db")
db2 = PostgresDb()
db3 = MysqlDb()

all_devices = list()
# -----------Creating User Interface Objects-----------
canvas.create_line(0, 68, 362, 68, 393, 36, 900, 36, fill=accent_color, width=3)
canvas.create_text(20, 35, anchor=W, font=('Helvetica', '22', 'bold'), text="Бригада №27", fill=accent_color)
btn2 = Custom_Button(["Додати техніку", "Вся наявна техніка", "Видалення техніки", "Редагування", "Експорт до БД2", "Експорт до БД3"], 10, 120, canvas,
                     [add, show_technique, delete_technique, edit_technique, db.export_to_database2, db.export_to_database3], update_canvas)

update_canvas(False, False)

root.mainloop()
