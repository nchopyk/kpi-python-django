import random
from Lab1.Server.sqllite_db import DateBase
from tkinter import *
S = list()
#------Colors--------
header_bg = "#0d252f"
menu_bg = "#243035"
content_bg = "#1c333f"
accent_color ="#e6bb0d"
menu_font_color = "#a8b1b5"
header_font_color = "#000000"
info_font_color = "#313131"



class HiTech_Chooser():
    """Class that draws and sets button
       in given self.pyramid_coords and binds it
       to appropriate functions"""


    def __init__(self, text, x, y, items, canvas, canvas2, funk=None):
        self.canvas = canvas
        self.canvas2 = canvas2
        self.text = text
        self.show = False
        self.items = items
        self.itemButtons = list()
        counter = 1
        for item in items:
            self.itemButtons.append(canvas2.create_text(83, 30*counter, anchor=CENTER, font="Arial, 15", text=item, fill=menu_font_color))
            canvas2.tag_bind(self.itemButtons[counter-1], '<ButtonPress-1>', self.on_ItemPress)
            canvas2.tag_bind(self.itemButtons[counter-1], '<Enter>', self.on_enter)
            canvas2.tag_bind(self.itemButtons[counter-1], '<Leave>', self.on_leave)
            counter+=1
            print(item)


        self.underline = canvas.create_line(x, y+14,x+166, y +14, fill=menu_font_color, width=2)
        self.btn = canvas.create_polygon(x + 143, y + 8, x + 153, y-2 , x + 133, y-2,
                                           fill=menu_font_color)
        self.btn2 = canvas.create_polygon(x + 143, y -2, x + 153, y +8, x + 133, y +8,
                                         fill=accent_color)
        canvas.itemconfig(self.btn2, state="hidden")

        self.txt = canvas.create_text(x + 60, y, anchor=CENTER, font="Arial, 15", text=text, fill=menu_font_color)

        self.funk = funk
        canvas.tag_bind(self.btn, '<ButtonPress-1>', self.on_press)
        canvas.tag_bind(self.underline, '<ButtonPress-1>', self.on_press)
        canvas.tag_bind(self.txt, '<ButtonPress-1>', self.on_press)
        canvas.tag_bind(self.btn2, '<ButtonPress-1>', self.on_press)

    def on_press(self, event):
        self.show = not self.show
        if self.show:
            self.canvas.itemconfig(self.btn, state="hidden")
            self.canvas.itemconfig(self.btn2, state="normal")
            self.canvas.itemconfig(self.underline, fill=accent_color)
            self.canvas.itemconfig(self.txt, fill=accent_color)
            self.canvas2.config(height=200, width=166)
        else:
            self.canvas.itemconfig(self.btn2, state="hidden")
            self.canvas.itemconfig(self.btn, state="normal")
            self.canvas.itemconfig(self.underline, fill=menu_font_color)
            self.canvas.itemconfig(self.txt, fill=menu_font_color)
            self.canvas2.config(width=0, height=0)

    def on_ItemPress(self, event):

        widget = self.canvas2.find_withtag("current")[0]
        self.canvas.itemconfig(self.txt, text=self.items[widget-1])
        self.on_press(widget)

    def on_enter(self, event):
        widget = self.canvas2.find_withtag("current")[0]
        self.canvas2.itemconfig(widget, fill=accent_color)

    def on_leave(self, event):
        widget = self.canvas2.find_withtag("current")[0]
        self.canvas2.itemconfig(widget, fill=menu_font_color)


class Custom_Button():
    """Class that draws and sets button
       in given self.pyramid_coords and binds it
       to appropriate functions"""

    def __init__(self, text, x, y, canvas, funk, update_funk):
        self.update_funk = update_funk
        self.canvas = canvas
        self.text = text
        self.funk = funk
        self.buttons = list()
        self.underlines = list()
        counter=0

        for button in text:
            self.buttons.append(canvas.create_text(x, y + 40*counter, anchor=W, font="Arial, 15", text=button, fill=menu_font_color))
            self.underlines.append(canvas.create_line(x, y + 14 + 40*counter, x + 166, y + 14 + 40*counter, fill=header_bg, width=2))
            canvas.tag_bind(self.buttons[counter], '<ButtonPress-1>', self.on_press)
            canvas.tag_bind(self.buttons[counter], '<Enter>', self.on_enter)
            canvas.tag_bind(self.buttons[counter], '<Leave>', self.on_leave)
            counter+=1

    def on_press(self, event):
        widget = self.canvas.find_withtag("current")[0]
        for underline in self.underlines:
            self.canvas.itemconfig(underline, fill=header_bg)
        self.canvas.itemconfig(widget, fill=accent_color)
        self.canvas.itemconfig(self.underlines[self.buttons.index(widget)], fill=accent_color)
        self.update_funk(False, False)
        if self.funk[self.buttons.index(widget)] != None:
            self.funk[self.buttons.index(widget)]()

    def disable(self, event):
        self.canvas.itemconfig(self.txt, fill=menu_font_color)
        self.canvas.itemconfig(self.underline, fill=header_bg)
    def on_enter(self, event):
        widget = self.canvas.find_withtag("current")[0]
        self.canvas.itemconfig(widget, fill=accent_color)

    def on_leave(self, event):
        widget = self.canvas.find_withtag("current")[0]
        self.canvas.itemconfig(widget, fill=menu_font_color)


class Device():
    """Class that draws and sets button
       in given self.pyramid_coords and binds it
       to appropriate functions"""

    def __init__(self, id, name, brand, size, en_ef_class, year_exp, price, x, y, canv_frame, db, update_function, add_mode=False):
        self.canv_frame = canv_frame
        self.update_function = update_function
        self.id = id
        self.name = name
        self.size = size
        self.brand = brand
        self.price = price
        self.price_num = price.split('грн')
        self.en_ef_class = en_ef_class
        self.year_exp = year_exp
        self.db = db
        self.x = x
        self.y = y
        if(size):
            self.size_arr = size.split('х')
        else:
            self.size_arr = ['','','']
        print(self.size_arr)

        self.frame = canv_frame.create_polygon(x, y, x + 190, y, x + 205, y + 15, x + 205, y + 145, x + 15, y + 145, x,
                                               y + 130, fill=accent_color)
        self.header = canv_frame.create_text(x + 10, y + 30, text=name, anchor=W, fill=header_font_color,
                                             font=('Helvetica', '12', 'bold'))
        self.header = canv_frame.create_text(x + 10, y + 60, text="Марка: " + brand, anchor=W, fill=info_font_color,
                                             font=('Helvetica', '8'))
        self.header = canv_frame.create_text(x + 10, y + 75, text="Розміри: " + size, anchor=W, fill=info_font_color,
                                             font=('Helvetica', '8'))
        self.header = canv_frame.create_text(x + 10, y + 90, text="Клас ен. еф.: " + en_ef_class, anchor=W,
                                             fill=info_font_color, font=('Helvetica', '8'))
        self.header = canv_frame.create_text(x + 10, y + 105, text="Витрати за рік: " + year_exp, anchor=W,
                                             fill=info_font_color, font=('Helvetica', '8'))
        self.header = canv_frame.create_text(x + 10, y + 120, text="Ціна: " + price, anchor=W, fill=info_font_color,
                                             font=('Helvetica', '8'))
        self.underline = canv_frame.create_polygon(x + 10, y + 40, x + 170, y + 40, x + 172, y + 42, x + 70, y + 42,
                                                   x + 66, y + 46, x + 16, y + 46, fill=header_font_color)



        self.delete_button = canv_frame.create_polygon(x + 205, y + 145, x + 135, y + 145, x + 135, y + 130,
                                                            x + 140, y + 125, x + 205, y + 125, fill="red", width=2)
        self.delete_cross = canv_frame.create_text(x + 140, y + 135, text="Видалити", anchor=W, fill="black",
                                             font=('Helvetica', '8'))
        canv_frame.itemconfig(self.delete_button, state="hidden")
        canv_frame.itemconfig(self.delete_cross, state="hidden")
        canv_frame.tag_bind(self.delete_button, '<ButtonPress-1>', self.on_delete_press)
        canv_frame.tag_bind(self.delete_cross, '<ButtonPress-1>', self.on_delete_press)
        canv_frame.tag_bind(self.delete_button, '<Enter>', self.on_delete_enter)
        canv_frame.tag_bind(self.delete_button, '<Leave>', self.on_delete_leave)
        canv_frame.tag_bind(self.delete_cross, '<Enter>', self.on_delete_enter)
        canv_frame.tag_bind(self.delete_cross, '<Leave>', self.on_delete_leave)

        self.edit_button = canv_frame.create_polygon(x + 205, y + 145, x + 135, y + 145, x + 135, y + 130,
                                                            x + 140, y + 125, x + 205, y + 125, fill="royal blue", width=2)
        self.edit_sign = canv_frame.create_text(x + 140, y + 135, text="Редагувати", anchor=W, fill="white",
                                             font=('Helvetica', '8'))
        canv_frame.tag_bind(self.edit_button, '<ButtonPress-1>', self.on_edit_press)
        canv_frame.tag_bind(self.edit_sign, '<ButtonPress-1>', self.on_edit_press)
        canv_frame.tag_bind(self.edit_button, '<Enter>', self.on_edit_enter)
        canv_frame.tag_bind(self.edit_button, '<Leave>', self.on_edit_leave)
        canv_frame.tag_bind(self.edit_sign, '<Enter>', self.on_edit_enter)
        canv_frame.tag_bind(self.edit_sign, '<Leave>', self.on_edit_leave)

        canv_frame.itemconfig(self.edit_button, state="hidden")
        canv_frame.itemconfig(self.edit_sign, state="hidden")

        # text coverage
        self.edit_text_cover = canv_frame.create_polygon(x + 43, y + 50, x + 43, y + 70, x + 55, y + 70, x + 55,
                                                     y + 85, x + 80, y + 85, x + 80, y + 100, x + 87, y + 100, x + 87, y + 115, x + 34, y + 115, x + 34, y + 130, x + 200, y + 130, x + 200, y + 50, fill=accent_color, width=2)

        # entry to edit brand
        self.entry_brand = Entry(canv_frame, borderwidth=0, fg="black", bg=accent_color, width=15, font=("", 7), bd=1,
                                highlightcolor=header_bg)
        self.entry_brand.insert(END, self.brand)


        # entry to edit size
        self.size_width_text = canv_frame.create_text(x + 55, y + 75, text="Ш:", anchor=W,
                                             fill=info_font_color, font=('Helvetica', '8'))
        self.size_length_text = canv_frame.create_text(x + 105, y + 75, text="Д:", anchor=W,
                                                      fill=info_font_color, font=('Helvetica', '8'))
        self.size_height_text = canv_frame.create_text(x + 155, y + 75, text="В:", anchor=W,
                                                      fill=info_font_color, font=('Helvetica', '8'))
        self.entry_size_width = Entry(canv_frame,borderwidth=0, fg="black", bg=accent_color,width=5, font=("",7), bd=1, highlightcolor=header_bg)
        self.entry_size_width.insert(END, self.size_arr[0])


        self.entry_size_length = Entry(canv_frame, borderwidth=0, fg="black", bg=accent_color, width=5, font=("", 7), bd=1,
                                highlightcolor=header_bg)
        self.entry_size_length.insert(END, self.size_arr[1])


        self.entry_size_height = Entry(canv_frame, borderwidth=0, fg="black", bg=accent_color, width=5, font=("", 7),
                                       bd=1,
                                       highlightcolor=header_bg)
        self.entry_size_height.insert(END, self.size_arr[2])


        # entry to edit energy efficiency class
        self.entry_en_ef_class = Entry(canv_frame, borderwidth=0, fg="black", bg=accent_color, width=15, font=("", 7), bd=1,
                                 highlightcolor=header_bg)
        self.entry_en_ef_class.insert(END, en_ef_class)



        # entry to edit electricity costs per year
        self.entry_year_exp = Entry(canv_frame, borderwidth=0, fg="black", bg=accent_color, width=15, font=("", 7),
                                       bd=1,
                                       highlightcolor=header_bg)
        self.entry_year_exp.insert(END, self.year_exp.split("грн")[0])


        # entry to edit price
        self.entry_price = Entry(canv_frame, borderwidth=0, fg="black", bg=accent_color, width=10, font=("", 7),
                                    bd=1,
                                    highlightcolor=header_bg)
        self.entry_price.insert(END, self.price_num[0])


        self.edit_accept_button = canv_frame.create_polygon(x + 205, y + 145, x + 135, y + 145, x + 135, y + 130,
                                                            x + 140, y + 125, x + 205, y + 125, fill="green", width=2)

        self.edit_accept_text = canv_frame.create_text(x + 140, y + 135, text="Підтвердити", anchor=W, fill="white",
                                             font=('Helvetica', '8'))

        canv_frame.tag_bind(self.edit_accept_button, '<ButtonPress-1>', self.on_edit_accept_press)
        canv_frame.tag_bind(self.edit_accept_text, '<ButtonPress-1>', self.on_edit_accept_press)
        canv_frame.tag_bind(self.edit_accept_button, '<Enter>', self.on_accept_enter)
        canv_frame.tag_bind(self.edit_accept_button, '<Leave>', self.on_accept_leave)
        canv_frame.tag_bind(self.edit_accept_text, '<Enter>', self.on_accept_enter)
        canv_frame.tag_bind(self.edit_accept_text, '<Leave>', self.on_accept_leave)
        self.error_edit_text = canv_frame.create_text(x + 10, y + 15, text="!!..!!", anchor=W, fill="black",
                                             font=('Helvetica', '8', 'bold'))

        canv_frame.itemconfig(self.error_edit_text, state="hidden")
        canv_frame.itemconfig(self.edit_text_cover, state="hidden")
        canv_frame.itemconfig(self.edit_accept_button, state="hidden")
        canv_frame.itemconfig(self.edit_accept_text, state="hidden")


        self.window_entry_size_height = self.canv_frame.create_window(self.x + 179, self.y + 75, window=self.entry_size_height)
        self.window_entry_size_length = self.canv_frame.create_window(self.x + 132, self.y + 75, window=self.entry_size_length)
        self.window_entry_size_width = self.canv_frame.create_window(self.x + 85, self.y + 75, window=self.entry_size_width)
        self.window_entry_brand = self.canv_frame.create_window(self.x + 85, self.y + 60, window=self.entry_brand)
        self.window_entry_en_ef_class = self.canv_frame.create_window(self.x + 118, self.y + 90, window=self.entry_en_ef_class)
        self.window_entry_year_exp = self.canv_frame.create_window(self.x + 128, self.y + 105, window=self.entry_year_exp)
        self.window_entry_price = self.canv_frame.create_window(self.x + 63, self.y + 120, window=self.entry_price)

        if(add_mode):
            canv_frame.create_text(70, 50, text="Для додавання нової техніки заповніть усі поля \n           та натисніть кнопку \"Додати\"", anchor=W, fill=accent_color,
                                   font=('Helvetica', '18'))
            self.status_text = canv_frame.create_text(300, 290,
                                   text="ERROR",
                                   anchor=CENTER, fill="red",
                                   font=('Helvetica', '18'))
            self.canv_frame.itemconfig(self.status_text, state="hidden")
            self.canv_frame.itemconfig(self.frame, outline="royal blue", width=3)
            self.button_add = canv_frame.create_polygon(x + 205, y + 145, x + 135, y + 145, x + 135, y + 130,
                                                            x + 140, y + 125, x + 205, y + 125, fill="royal blue", width=2)
            self.button_add_text = canv_frame.create_text(x + 140, y + 135, text="Додати", anchor=W, fill="white",
                                             font=('Helvetica', '8'))
            self.name_entry = Entry(canv_frame, borderwidth=0, fg="black", bg=accent_color, width=10, font=("", 10),
                                    bd=1,
                                    highlightcolor=header_bg)
            self.window_entry_name = self.canv_frame.create_window(self.x + 120, self.y + 25,
                                                                          window=self.name_entry)
            self.name_text = canv_frame.create_text(x + 10, y + 25, text="Назава:", anchor=W, fill="black",
                                             font=('Helvetica', '12', 'bold'))

            canv_frame.tag_bind(self.button_add, '<ButtonPress-1>', self.on_add_press)
            canv_frame.tag_bind(self.button_add_text, '<ButtonPress-1>', self.on_add_press)
            canv_frame.tag_bind(self.button_add, '<Enter>', self.on_add_enter)
            canv_frame.tag_bind(self.button_add, '<Leave>', self.on_add_leave)
            canv_frame.tag_bind(self.button_add_text, '<Enter>', self.on_add_enter)
            canv_frame.tag_bind(self.button_add_text, '<Leave>', self.on_add_leave)

        else:
            self.canv_frame.itemconfig(self.window_entry_size_height, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_size_length, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_size_width, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_brand, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_en_ef_class, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_year_exp, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_price, state="hidden")
            canv_frame.itemconfig(self.size_width_text, state="hidden")
            canv_frame.itemconfig(self.size_length_text, state="hidden")
            canv_frame.itemconfig(self.size_height_text, state="hidden")


    def update(self, delete, edit):
        if(delete):
            self.canv_frame.itemconfig(self.frame, outline="")

            self.canv_frame.itemconfig(self.window_entry_size_height, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_size_length, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_size_width, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_brand, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_en_ef_class, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_year_exp, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_price, state="hidden")

            self.canv_frame.itemconfig(self.edit_text_cover, state="hidden")
            self.canv_frame.itemconfig(self.size_height_text, state="hidden")
            self.canv_frame.itemconfig(self.size_length_text, state="hidden")
            self.canv_frame.itemconfig(self.size_width_text, state="hidden")
            self.canv_frame.itemconfig(self.edit_accept_text, state="hidden")
            self.canv_frame.itemconfig(self.edit_accept_button, state="hidden")

            self.canv_frame.itemconfig(self.edit_button, state="hidden")
            self.canv_frame.itemconfig(self.edit_sign, state="hidden")

            self.canv_frame.itemconfig(self.delete_button, state="normal")
            self.canv_frame.itemconfig(self.delete_cross, state="normal")
        elif(edit):
            self.canv_frame.itemconfig(self.edit_button, state="normal")
            self.canv_frame.itemconfig(self.edit_sign, state="normal")

            self.canv_frame.itemconfig(self.delete_button, state="hidden")
            self.canv_frame.itemconfig(self.delete_cross, state="hidden")
        else:
            self.canv_frame.itemconfig(self.frame, outline="")

            self.canv_frame.itemconfig(self.window_entry_size_height, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_size_length, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_size_width, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_brand, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_en_ef_class, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_year_exp, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_price, state="hidden")

            self.canv_frame.itemconfig(self.edit_text_cover, state="hidden")
            self.canv_frame.itemconfig(self.size_height_text, state="hidden")
            self.canv_frame.itemconfig(self.size_length_text, state="hidden")
            self.canv_frame.itemconfig(self.size_width_text, state="hidden")
            self.canv_frame.itemconfig(self.edit_accept_text, state="hidden")
            self.canv_frame.itemconfig(self.edit_accept_button, state="hidden")

            self.canv_frame.itemconfig(self.edit_button, state="hidden")
            self.canv_frame.itemconfig(self.edit_sign, state="hidden")

            self.canv_frame.itemconfig(self.delete_button, state="hidden")
            self.canv_frame.itemconfig(self.delete_cross, state="hidden")

    def on_delete_press(self, event):
        self.db.delete_technique_by_id(self.id)
        print("deleted")
        self.update_function(True, False)

    def on_edit_accept_press(self, event):

        self.canv_frame.itemconfig(self.error_edit_text, state="hidden")
        new_brand = self.entry_brand.get()
        new_size_width = self.entry_size_width.get()
        new_size_length = self.entry_size_length.get()
        new_size_height = self.entry_size_height.get()
        new_en_ef_class = self.entry_en_ef_class.get()
        new_year_exp = self.entry_year_exp.get()
        new_price = self.entry_price.get()
        if(new_brand and new_size_width and new_size_length and new_size_height and new_en_ef_class and new_year_exp and new_price):
            if (new_size_height.isdigit() and new_size_length.isdigit() and new_size_width.isdigit()):
                if(new_year_exp.isdigit()):
                    if(new_price.isdigit()):
                        self.db.edit_technique(self.id, self.name, new_brand, new_size_width+"х"+new_size_length+"х"+new_size_height, new_en_ef_class, new_year_exp+"грн", new_price+"грн")
                        self.update_function(False, True)
                    else:
                        self.canv_frame.itemconfig(self.frame, outline="red", width=3)
                        self.canv_frame.itemconfig(self.error_edit_text, state="normal", text="!!Невірно вказано ціну!!")
                else:
                    self.canv_frame.itemconfig(self.frame, outline="red", width=3)
                    self.canv_frame.itemconfig(self.error_edit_text, state="normal", text="!!Невірно вказано витрати за рік!!")
            else:
                self.canv_frame.itemconfig(self.frame, outline="red", width=3)
                self.canv_frame.itemconfig(self.error_edit_text, state="normal", text="!!Невірно вказано розміри!!")
        else:
            self.canv_frame.itemconfig(self.frame, outline="red", width=3)
            self.canv_frame.itemconfig(self.error_edit_text, state="normal", text="!!Є незаповнені поля!!")

    def on_add_press(self, event):
        new_name =self.name_entry.get()
        new_brand = self.entry_brand.get()
        new_size_width = self.entry_size_width.get()
        new_size_length = self.entry_size_length.get()
        new_size_height = self.entry_size_height.get()
        new_en_ef_class = self.entry_en_ef_class.get()
        new_year_exp = self.entry_year_exp.get()
        new_price = self.entry_price.get()
        if(new_name and new_brand and new_size_width and new_size_length and new_size_height and new_en_ef_class and new_year_exp and new_price):
            if (new_size_height.isdigit() and new_size_length.isdigit() and new_size_width.isdigit()):
                if(new_year_exp.isdigit()):
                    if(new_price.isdigit()):
                        self.db.add_technique(new_name, new_brand, new_size_width+"х"+new_size_length+"х"+new_size_height, new_en_ef_class, new_year_exp+"грн", new_price+"грн")
                        self.canv_frame.itemconfig(self.status_text, state="normal",
                                                   text="    Техніку успішно додано    \n Для перевірки перейдіть у \nрозділ \"Вся наявна техніка\"", fill="green")
                        self.canv_frame.itemconfig(self.frame, outline="green", width=3)
                    else:
                        self.canv_frame.itemconfig(self.frame, outline="red", width=3)
                        self.canv_frame.itemconfig(self.status_text, state="normal",
                                                   text="!!Невірно вказано ціну!!", fill="red")
                else:
                    self.canv_frame.itemconfig(self.frame, outline="red", width=3)
                    self.canv_frame.itemconfig(self.status_text, state="normal",
                                               text="!!Невірно вказано витрати за рік!!", fill="red")
            else:
                self.canv_frame.itemconfig(self.frame, outline="red", width=3)
                self.canv_frame.itemconfig(self.status_text, state="normal",
                                           text="!!Невірно вказано розміри!!", fill="red")
        else:
            self.canv_frame.itemconfig(self.frame, outline="red", width=3)
            self.canv_frame.itemconfig(self.status_text, state="normal",
                                       text="!!Є незаповнені поля!!", fill="red")

    def on_edit_press(self, event):

        self.canv_frame.itemconfig(self.window_entry_size_height, state="normal")
        self.canv_frame.itemconfig(self.window_entry_size_length, state="normal")
        self.canv_frame.itemconfig(self.window_entry_size_width, state="normal")
        self.canv_frame.itemconfig(self.window_entry_brand, state="normal")
        self.canv_frame.itemconfig(self.window_entry_en_ef_class, state="normal")
        self.canv_frame.itemconfig(self.window_entry_year_exp, state="normal")
        self.canv_frame.itemconfig(self.window_entry_price, state="normal")

        self.canv_frame.itemconfig(self.edit_button, state="hidden")
        self.canv_frame.itemconfig(self.edit_sign, state="hidden")

        self.canv_frame.itemconfig(self.edit_text_cover, state="normal")
        self.canv_frame.itemconfig(self.edit_accept_button, state="normal")
        self.canv_frame.itemconfig(self.edit_accept_text, state="normal")

        self.canv_frame.itemconfig(self.size_width_text, state="normal")
        self.canv_frame.itemconfig(self.size_length_text, state="normal")
        self.canv_frame.itemconfig(self.size_height_text, state="normal")

        self.canv_frame.itemconfig(self.frame, outline="green", width=3)

    def on_accept_enter(self, event):
        self.canv_frame.itemconfig(self.edit_accept_button, fill="green yellow")
        self.canv_frame.itemconfig(self.edit_accept_text, fill="black")

    def on_accept_leave(self, event):
        self.canv_frame.itemconfig(self.edit_accept_button, fill="green")
        self.canv_frame.itemconfig(self.edit_accept_text, fill="white")

    def on_delete_enter(self, event):
        self.canv_frame.itemconfig(self.delete_button, fill="orange red")

    def on_delete_leave(self, event):
        self.canv_frame.itemconfig(self.delete_button, fill="red")

    def on_edit_enter(self, event):
        self.canv_frame.itemconfig(self.edit_button, fill="royal blue1")

    def on_edit_leave(self, event):
        self.canv_frame.itemconfig(self.edit_button, fill="royal blue")

    def on_add_enter(self, event):
        self.canv_frame.itemconfig(self.button_add, fill="royal blue1")

    def on_add_leave(self, event):
        self.canv_frame.itemconfig(self.button_add, fill="royal blue")
