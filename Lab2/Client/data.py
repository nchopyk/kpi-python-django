from tkinter import *

#------Colors--------
header_bg = "#0d252f"
menu_bg = "#243035"
content_bg = "#1c333f"
accent_color ="#e6bb0d"
menu_font_color = "#a8b1b5"
header_font_color = "#000000"
info_font_color = "#313131"


class Custom_Button():
    """Class that places a group of
    buttons in the menu section and binds
    them to appropriate functions"""

    def __init__(self, text, x, y, canvas, funk, update_func):
        """:param text: a list of titles for each button
        :param x: coordinate x of the first button
        :param y: coordinate y of the first button
        :param canvas: a canvas to place the buttons
        :param funk: a list of function to each button
        :param update_func: a function to update the canvas"""

        self.update_func = update_func
        self.canvas = canvas
        self.text = text
        self.funk = funk
        self.buttons = list()
        self.underlines = list()
        counter=0

        # Placing all buttons and binding them to their functions
        for button in text:
            self.buttons.append(canvas.create_text(x, y + 40*counter, anchor=W, font="Arial, 15", text=button, fill=menu_font_color))
            self.underlines.append(canvas.create_line(x, y + 14 + 40*counter, x + 166, y + 14 + 40*counter, fill=header_bg, width=2))
            canvas.tag_bind(self.buttons[counter], '<ButtonPress-1>', self.on_press)
            canvas.tag_bind(self.buttons[counter], '<Enter>', self.on_enter)
            canvas.tag_bind(self.buttons[counter], '<Leave>', self.on_leave)
            counter+=1

    def on_press(self, event):
        """A function that creates the underline
        under the pressed button and runs the
        appropriate function"""

        widget = self.canvas.find_withtag("current")[0]
        for underline in self.underlines:
            self.canvas.itemconfig(underline, fill=header_bg)
        self.canvas.itemconfig(widget, fill=accent_color)
        self.canvas.itemconfig(self.underlines[self.buttons.index(widget)], fill=accent_color)
        if self.buttons.index(widget) ==4:
            self.update_func(False, False, d_b2=True)
        elif self.buttons.index(widget) ==5:
            self.update_func(False, False, d_b3=True)
        else:
            self.update_func(False, False)
        if self.funk[self.buttons.index(widget)] != None:
            self.funk[self.buttons.index(widget)]()

    def disable(self, event):
        """A function to get rid of the underline of previously
        chosen button"""

        self.canvas.itemconfig(self.txt, fill=menu_font_color)
        self.canvas.itemconfig(self.underline, fill=header_bg)

    def on_enter(self, event):
        """A function to light up the button when the user
        hovers the cursor on it"""
        widget = self.canvas.find_withtag("current")[0]
        self.canvas.itemconfig(widget, fill=accent_color)

    def on_leave(self, event):
        """A function to return the button it`s normal color
        when the user moves the cursor away"""

        widget = self.canvas.find_withtag("current")[0]
        self.canvas.itemconfig(widget, fill=menu_font_color)


class Device():
    """Class that displays each technique
    with all of it`s parameters and with
    the abilities to add, edit and delete it
    from the database"""

    def __init__(self, id, name, brand, size, en_ef_class, electricity_costs_per_year, price, x, y, canv_frame, db, update_function, add_mode=False):
        """:param id: an id of the current technique
        :param name: a name of the current technique
        :param brand: a brand of the current technique
        :param size: a size of the current technique
        :param en_ef_class: an energy efficiency class of the current technique
        :param electricity_costs_per_year: an electricity costs per year of the current technique
        :param price: a price of the current technique
        :param x: x coordinate of the current technique
        :param y: y coordinate of the current technique
        :param canv_frame: a canvas to place the current technique
        :param db: database
        :param update_function: a function to update the canvas
        :param add_mode: allows adding new technique to database"""

        self.canv_frame = canv_frame
        self.update_function = update_function
        self.id = id
        self.name = name
        self.size = size
        self.brand = brand
        self.price = price
        self.price_num = str(price)
        self.en_ef_class = en_ef_class
        self.electricity_costs_per_year = str(electricity_costs_per_year)
        self.db = db
        self.x = x
        self.y = y
        # getting the width, length and height from the size
        if(size):
            self.size_arr = size.split('х')
        else:
            self.size_arr = ['','','']
        print(self.size_arr)

        # creating texts and polygons to display the current technique
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
        self.header = canv_frame.create_text(x + 10, y + 105, text="Витрати за рік: " + str(electricity_costs_per_year)+"грн", anchor=W,
                                             fill=info_font_color, font=('Helvetica', '8'))
        self.header = canv_frame.create_text(x + 10, y + 120, text="Ціна: " + str(price) + "грн", anchor=W, fill=info_font_color,
                                             font=('Helvetica', '8'))
        self.underline = canv_frame.create_polygon(x + 10, y + 40, x + 170, y + 40, x + 172, y + 42, x + 70, y + 42,
                                                   x + 66, y + 46, x + 16, y + 46, fill=header_font_color)



        self.delete_button = canv_frame.create_polygon(x + 205, y + 145, x + 135, y + 145, x + 135, y + 130,
                                                            x + 140, y + 125, x + 205, y + 125, fill="red", width=2)
        self.delete_cross = canv_frame.create_text(x + 140, y + 135, text="Видалити", anchor=W, fill="black",
                                             font=('Helvetica', '8'))
        canv_frame.itemconfig(self.delete_button, state="hidden")
        canv_frame.itemconfig(self.delete_cross, state="hidden")
        # binding to the functions
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
        # binding to the functions
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
        self.entry_electricity_costs_per_year = Entry(canv_frame, borderwidth=0, fg="black", bg=accent_color, width=15, font=("", 7),
                                       bd=1,
                                       highlightcolor=header_bg)
        self.entry_electricity_costs_per_year.insert(END, self.electricity_costs_per_year.split("грн")[0])

        # entry to edit price
        self.entry_price = Entry(canv_frame, borderwidth=0, fg="black", bg=accent_color, width=10, font=("", 7),
                                    bd=1,
                                    highlightcolor=header_bg)
        self.entry_price.insert(END, self.price_num)
        self.edit_accept_button = canv_frame.create_polygon(x + 205, y + 145, x + 135, y + 145, x + 135, y + 130,
                                                            x + 140, y + 125, x + 205, y + 125, fill="green", width=2)
        self.edit_accept_text = canv_frame.create_text(x + 140, y + 135, text="Підтвердити", anchor=W, fill="white",
                                             font=('Helvetica', '8'))
        # binding to the functions
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
        self.window_entry_electricity_costs_per_year = self.canv_frame.create_window(self.x + 128, self.y + 105, window=self.entry_electricity_costs_per_year)
        self.window_entry_price = self.canv_frame.create_window(self.x + 63, self.y + 120, window=self.entry_price)

        if(add_mode):
            # creating widgets to add new technique
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
            # binding to the functions
            canv_frame.tag_bind(self.button_add, '<ButtonPress-1>', self.on_add_press)
            canv_frame.tag_bind(self.button_add_text, '<ButtonPress-1>', self.on_add_press)
            canv_frame.tag_bind(self.button_add, '<Enter>', self.on_add_enter)
            canv_frame.tag_bind(self.button_add, '<Leave>', self.on_add_leave)
            canv_frame.tag_bind(self.button_add_text, '<Enter>', self.on_add_enter)
            canv_frame.tag_bind(self.button_add_text, '<Leave>', self.on_add_leave)

        else:
            # hiding the additional widgets
            self.canv_frame.itemconfig(self.window_entry_size_height, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_size_length, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_size_width, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_brand, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_en_ef_class, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_electricity_costs_per_year, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_price, state="hidden")
            canv_frame.itemconfig(self.size_width_text, state="hidden")
            canv_frame.itemconfig(self.size_length_text, state="hidden")
            canv_frame.itemconfig(self.size_height_text, state="hidden")


    def update(self, delete, edit):
        """A function to display the abilities
        to delete, edit or to just view the technique"""
        if(delete):
            self.canv_frame.itemconfig(self.frame, outline="")

            self.canv_frame.itemconfig(self.window_entry_size_height, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_size_length, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_size_width, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_brand, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_en_ef_class, state="hidden")
            self.canv_frame.itemconfig(self.window_entry_electricity_costs_per_year, state="hidden")
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
            self.canv_frame.itemconfig(self.window_entry_electricity_costs_per_year, state="hidden")
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
        new_electricity_costs_per_year = self.entry_electricity_costs_per_year.get()
        new_price = self.entry_price.get()
        if(new_brand and new_size_width and new_size_length and new_size_height and new_en_ef_class and new_electricity_costs_per_year and new_price):
            if (new_size_height.isdigit() and new_size_length.isdigit() and new_size_width.isdigit()):
                if(new_electricity_costs_per_year.isdigit()):
                    if(new_price.isdigit()):
                        self.db.edit_technique(self.id, self.name, new_brand, new_size_width+"х"+new_size_length+"х"+new_size_height, new_en_ef_class, int(new_electricity_costs_per_year), int(new_price))
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
        new_electricity_costs_per_year = self.entry_electricity_costs_per_year.get()
        new_price = self.entry_price.get()
        if(new_name and new_brand and new_size_width and new_size_length and new_size_height and new_en_ef_class and new_electricity_costs_per_year and new_price):
            if (new_size_height.isdigit() and new_size_length.isdigit() and new_size_width.isdigit()):
                if(new_electricity_costs_per_year.isdigit()):
                    if(new_price.isdigit()):
                        self.db.add_technique(new_name, new_brand, new_size_width+"х"+new_size_length+"х"+new_size_height, new_en_ef_class, int(new_electricity_costs_per_year), int(new_price))
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
        self.canv_frame.itemconfig(self.window_entry_electricity_costs_per_year, state="normal")
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



class Db2_Device():
    """Class that displays each technique
    from db2"""

    def __init__(self, name, brand, en_ef_class, price, x, y, canv_frame):
        """
        :param name: a name of the current technique
        :param brand: a brand of the current technique
        :param size: a size of the current technique
        :param en_ef_class: an energy efficiency class of the current technique
        :param x: x coordinate of the current technique
        :param y: y coordinate of the current technique
        :param canv_frame: a canvas to place the current technique
        :param db: database"""

        self.canv_frame = canv_frame

        self.name = name
        self.price = price
        self.brand = brand
        self.en_ef_class = en_ef_class
        self.x = x
        self.y = y

        # creating texts and polygons to display the current technique
        self.frame = canv_frame.create_polygon(x, y, x + 190, y, x + 205, y + 15, x + 205, y + 145, x + 15, y + 145, x,
                                               y + 130, fill=accent_color)
        self.header = canv_frame.create_text(x + 10, y + 30, text=name, anchor=W, fill=header_font_color,
                                             font=('Helvetica', '12', 'bold'))
        self.header = canv_frame.create_text(x + 10, y + 60, text="Марка: " + brand, anchor=W, fill=info_font_color,
                                             font=('Helvetica', '8'))
        self.header = canv_frame.create_text(x + 10, y + 75, text="Ціна: " + str(price)+"грн", anchor=W, fill=info_font_color,
                                             font=('Helvetica', '8'))
        self.header = canv_frame.create_text(x + 10, y + 90, text="Клас ен. еф.: " + en_ef_class, anchor=W,
                                             fill=info_font_color, font=('Helvetica', '8'))
        self.underline = canv_frame.create_polygon(x + 10, y + 40, x + 170, y + 40, x + 172, y + 42, x + 70, y + 42,
                                                   x + 66, y + 46, x + 16, y + 46, fill=header_font_color)
