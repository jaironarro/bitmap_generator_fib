from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import PIL.ImageGrab as ImageGrab
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Creation of window
def quit_me():
    print('quit')
    WIN.quit()
    WIN.destroy()


WIN = Tk(className='bitmap generator')
WIN.protocol("WM_DELETE_WINDOW", quit_me)

WIN.geometry("1200x650")

# Creation of toolbar
toolbar = Frame(WIN)
toolbar.pack(side=RIGHT, fill='y')
toolbar.config(bg="white")
toolbar.config(width=200, height=600)

# Creation of parameters_bar
parameters_bar = Frame(WIN)
parameters_bar.pack(side=TOP, fill='x')
parameters_bar.config(bg="white")
parameters_bar.config(width=200, height=40)

# Creation of Cross-Section View
cross_view_frame = LabelFrame(WIN, text=" Cross-Section View ", padx=5, pady=5)
cross_view_frame.pack(side=RIGHT, expand=True)

cross_view = Frame(cross_view_frame, width=400, height=400, bg="white")
cross_view.pack()

# Creation of canvas
canvas_frame = LabelFrame(WIN, text=" Bitmap File ", padx=5, pady=5)
canvas_frame.pack(side=LEFT, expand=True)

canvas = Canvas(canvas_frame, width=400, height=400, bg="black", bd=0, highlightthickness=0)
canvas.pack(side=TOP)

show_bitmap_size = Label(canvas_frame, text="Number of Pixels: 400 X 400")
show_bitmap_size.pack(side=TOP, anchor=N)

# ------------------------- Functions -------------------------------------


# Defining bitmap size
def defining_bitmap_size():

    if pitch_x.get() and pitch_y.get() and size_x.get() and size_y.get():
        canvas_width = int(float(size_x.get())/float(pitch_x.get()))
        canvas_height = int(float(size_y.get())/float(pitch_y.get()))
        canvas.config(width=canvas_width, height=canvas_height)
        show_bitmap_size.config(text="Number of Pixels: "
                                + str(canvas_width) + " x " + str(canvas_height))


# Defining grid dimensions
def draw_grid():

    if rows.get() and cols.get():
        w = canvas.winfo_width()
        h = canvas.winfo_height()

        step_1 = w/int(cols.get())
        step_2 = h/int(rows.get())

        my_text = grid_button.cget('text')

        if my_text == 'Grid ON':
            grid_button.config(text='Grid OFF')
            for i in np.arange(0, w+int(cols.get()), float(step_1)):
                canvas.create_line([(i, 0), (i, h)], fill='white', tags='v_line')
            for i in np.arange(0, h+int(rows.get()), float(step_2)):
                canvas.create_line([(0, i), (w, i)], fill='white', tags='h_line')

        elif my_text == 'Grid OFF':
            grid_button.config(text='Grid ON')
            canvas.delete("v_line", "h_line")


# Delete all
def clear_canvas():

    canvas.delete("all")
    grid_button.config(text='Grid ON')


# Color the boxes - 1
def get_pos_from_mouse(event):

    pos_x = event.x
    pos_y = event.y
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    step1 = float(w/int(cols.get()))
    step2 = float(h/int(rows.get()))
    for i in np.arange(0, w+int(cols.get()), step1):
        for j in np.arange(0, h + int(rows.get()), step2):
            if (pos_x >= i) and (pos_x <= i + step1) and (pos_y >= j) and (pos_y <= j+step2):
                canvas.create_rectangle(i, j, i+step1, j+step2, fill=color.get(), outline=color.get())


# Color the boxes - 2
def draw_pixel_grid():

    canvas.bind('<B1-Motion>', get_pos_from_mouse)


# Draw circle in canvas
def draw_circle():

    if circle_radio.get() and circle_center_x.get() and circle_center_y.get():
        # x = float(circle_center_x.get())/float(pitch_x.get()) - 1
        # y = float(circle_center_y.get())/float(pitch_y.get()) - 1
        # r = float(circle_radio.get())/float(pitch_x.get()) - 1
        # px = float(period_x.get()) / float(pitch_x.get()) - 1
        # py = float(period_y.get()) / float(pitch_y.get()) - 1

        x = float(circle_center_x.get())
        y = float(circle_center_y.get())
        r = float(circle_radio.get())

        px = float(period_x.get())
        py = float(period_y.get())

        canvas.create_oval(x - r, y - r, x + r, y + r,
                           fill=color.get(), outline=color.get())

        for i in range(1, int(matrix_row.get())):
            canvas.create_oval(x - r + px * i, y - r,
                               x + r + px * i, y + r,
                               fill=color.get(), outline=color.get())

        for j in range(1, int(matrix_col.get())):
            canvas.create_oval(x - r, y - r + py * j,
                               x + r, y + r + py * j,
                               fill=color.get(), outline=color.get())

        for i in range(1, int(matrix_row.get())):
            for j in range(1, int(matrix_col.get())):
                canvas.create_oval(x - r + px * i, y - r + py * j,
                                   x + r + px * i, y + r + py * j,
                                   fill=color.get(), outline=color.get())


# Draw rectangle in canvas
def draw_rect():

    if rect_pos1.get() and rect_pos2.get() and rect_pos3.get() and rect_pos4.get():
        # x0 = float(rect_pos1.get())/float(pitch_x.get())
        # y0 = float(rect_pos2.get())/float(pitch_y.get())
        # x1 = float(rect_pos3.get())/float(pitch_x.get())
        # y1 = float(rect_pos4.get())/float(pitch_y.get())

        # px = float(period_x.get()) / float(pitch_x.get())
        # py = float(period_y.get()) / float(pitch_y.get())

        x0 = float(rect_pos1.get())
        y0 = float(rect_pos2.get())
        x1 = float(rect_pos3.get())
        y1 = float(rect_pos4.get())

        px = float(period_x.get())
        py = float(period_y.get())

        canvas.create_rectangle(x0, y0, x1, y1, fill=color.get(), outline=color.get())

        for i in range(1, int(matrix_row.get())):
            canvas.create_rectangle(x0 + px * i, y0,
                                    x1 + px * i, y1, fill=color.get(), outline=color.get())

        for j in range(1, int(matrix_col.get())):
            canvas.create_rectangle(x0, y0 + py * j,
                                    x1, y1 + py * j, fill=color.get(), outline=color.get())

        for i in range(1, int(matrix_row.get())):
            for j in range(1, int(matrix_col.get())):
                canvas.create_rectangle(x0 + px * i, y0 + py * j,
                                        x1 + px * i, y1 + py * j,
                                        fill=color.get(), outline=color.get())


# Draw triangle
def draw_triangle():

    if tri_pos_x0.get() and tri_pos_x1.get() and tri_pos_y0.get() and tri_pos_y1.get()\
            and tri_pos_z0.get() and tri_pos_z1.get():

        # x0 = float(tri_pos_x0.get())/float(pitch_x.get())
        # x1 = float(tri_pos_x1.get())/float(pitch_y.get())
        # y0 = float(tri_pos_y0.get()) / float(pitch_x.get())
        # y1 = float(tri_pos_y1.get()) / float(pitch_y.get())
        # z0 = float(tri_pos_z0.get()) / float(pitch_x.get())
        # z1 = float(tri_pos_z1.get()) / float(pitch_y.get())

        # px = float(period_x.get()) / float(pitch_x.get())
        # py = float(period_y.get()) / float(pitch_y.get())

        x0 = float(tri_pos_x0.get())
        x1 = float(tri_pos_x1.get())
        y0 = float(tri_pos_y0.get())
        y1 = float(tri_pos_y1.get())
        z0 = float(tri_pos_z0.get())
        z1 = float(tri_pos_z1.get())

        px = float(period_x.get())
        py = float(period_y.get())

        canvas.create_polygon(x0, x1, y0, y1, z0, z1, fill=color.get(), outline=color.get())

        for i in range(1, int(matrix_row.get())):
            canvas.create_polygon(x0 + px * i, x1,
                                  y0 + px * i, y1,
                                  z0 + px * i, z1, fill=color.get(), outline=color.get())

        for j in range(1, int(matrix_col.get())):
            canvas.create_polygon(x0, x1 + py * j,
                                  y0, y1 + py * j,
                                  z0, z1 + py * j, fill=color.get(), outline=color.get())

        for i in range(1, int(matrix_row.get())):
            for j in range(1, int(matrix_col.get())):
                canvas.create_polygon(x0 + px * i, x1 + py * j,
                                      y0 + px * i, y1 + py * j,
                                      z0 + px * i, z1 + py * j,
                                      fill=color.get(), outline=color.get())


# Shows 3D structure
def show_grayscale_cross_view():

    p_size = canvas.winfo_width()

    if cap_height.get() and radio.get():

        r = float(radio.get())
        c_h = float(cap_height.get())

        x = np.linspace(-1*r, r, p_size)

        profile = (c_h / (r**2)) * (x**2) - c_h
        figure_2 = plt.figure(figsize=(4.5, 4.5))
        figure_2.add_subplot(111).plot(x, profile)
        plt.subplots_adjust(bottom=.25, left=.25)
        chart_2 = FigureCanvasTkAgg(figure_2, cross_view)
        chart_2.get_tk_widget().place(relx=0.5, rely=0.55, anchor="center")

    elif depth.get() and slope.get():
        s = float(slope.get())
        d = float(depth.get())

        r = d / s
        x = np.linspace(-1 * r, r, p_size)

        if p_size % 2 == 0:
            y1 = -1 * s * x[0:int(p_size / 2)] - d
            y2 = s * x[int(p_size / 2 - 1) + 1:p_size] - d
        else:
            y1 = -1 * s * x[0:int(p_size / 2 + 0.5)] - d
            y2 = s * x[int(p_size / 2 + 0.5) + 1:p_size] - d

        profile = np.concatenate([y1, y2])
        figure_2 = plt.figure(figsize=(4.5, 4.5))
        figure_2.add_subplot(111).plot(x, profile)
        plt.subplots_adjust(bottom=.25, left=.25)
        chart_2 = FigureCanvasTkAgg(figure_2, cross_view)
        chart_2.get_tk_widget().place(relx=0.5, rely=0.55, anchor="center")

    plt.grid(True)

    plt.xlabel("width (μm)")
    plt.ylabel("height (μm)")
    plt.title("Cross-Section View")


global grayscale


def show_grayscale_bitmap():

    global grayscale
    p_size = canvas.winfo_width()

    if cap_height.get() and radio.get():

        r = float(radio.get())
        c_h = float(cap_height.get())

        x = np.linspace(-1 * r, r, p_size)

        profile = (c_h / (r ** 2)) * (x ** 2) - c_h
        bitmap_matrix = 255 * np.ones((p_size, p_size))
        new_bitmap_matrix = np.ones((p_size, p_size))

        for i in range(p_size):
            new_bitmap_matrix[i] = bitmap_matrix[i] * (-1) * profile[i] / c_h

        bitmap_file = new_bitmap_matrix.transpose()
        bitmap_file = bitmap_file.astype('uint8')
        grayscale = ImageTk.PhotoImage(image=Image.fromarray(bitmap_file))
        canvas.create_image(0, 0, anchor=NW, image=grayscale)

    elif depth.get() and slope.get():
        s = float(slope.get())
        d = float(depth.get())

        r = d / s
        x = np.linspace(-1 * r, r, p_size)

        if p_size % 2 == 0:
            y1 = -1 * s * x[0:int(p_size / 2)] - d
            y2 = s * x[int(p_size / 2 - 1) + 1:p_size] - d
        else:
            y1 = -1 * s * x[0:int(p_size / 2 + 0.5)] - d
            y2 = s * x[int(p_size / 2 + 0.5) + 1:p_size] - d

        profile = np.concatenate([y1, y2])
        bitmap_matrix = 255 * np.ones((p_size, p_size))
        new_bitmap_matrix = np.ones((p_size, p_size))

        for i in range(p_size):
            new_bitmap_matrix[i] = bitmap_matrix[i] * (profile[i] / min(profile))

        bitmap_file = new_bitmap_matrix.transpose()
        bitmap_file = bitmap_file.astype('uint8')
        grayscale = ImageTk.PhotoImage(image=Image.fromarray(bitmap_file))
        canvas.create_image(0, 0, anchor=NW, image=grayscale)


# Import image on canvas
global new_image


def import_file():

    global new_image

    if img_pos_x.get() and img_pos_y.get():

        file_name = filedialog.askopenfilename(filetypes=[("PNG Image", ".png"),
                                                          ("JPEG Image", ".jpg"),
                                                          ("BITMAP Image", ".bmp")])

        img = Image.open(file_name)

        if img_size_x.get() and img_size_y.get():
            my_image = img.resize((int(img_size_x.get()), int(img_size_y.get())), Image.ANTIALIAS)
            new_image = ImageTk.PhotoImage(my_image)
            canvas.create_image(float(img_pos_x.get()), float(img_pos_y.get()), image=new_image)
        else:
            new_image = ImageTk.PhotoImage(img)
            canvas.create_image(float(img_pos_x.get()), float(img_pos_y.get()), image=new_image)
    else:
        messagebox.showinfo('Import File', 'Set position and size values')


# Saving canvas as a 24-bit bitmap file
def save_file():

    filename = filedialog.asksaveasfilename(defaultextension='.bmp', filetypes=[("BITMAP Image", ".bmp"),
                                                                                ("JPEG Image", ".jpg"),
                                                                                ("PNG Image", ".png")])

    x = canvas.winfo_rootx()
    y = canvas.winfo_rooty()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()

    ImageGrab.grab().crop((x, y, x1, y1)).save(filename)
    messagebox.showinfo('Save Image', 'Image saved in: ' + str(filename))


# Display mouse coordinates
def display_coordinates(event):
    pos_x = event.x
    pos_y = event.y
    label_coordinates.config(text='Coordinates X: ' + str(pos_x) + ' Y: ' + str(pos_y))


label_coordinates = Label(canvas_frame, text="Coordinates X:  Y:")
label_coordinates.pack()
canvas.bind('<Motion>', display_coordinates)
# ------------------------- Buttons -------------------------------------


# Defines Number of Pixel
pitch_x = Entry(toolbar, borderwidth=2)
pitch_x.insert(0, 1)

pitch_y = Entry(toolbar, borderwidth=2)
pitch_y.insert(0, 1)

size_x = Entry(toolbar, borderwidth=2)
size_x.insert(0, 400)

size_y = Entry(toolbar, borderwidth=2)
size_y.insert(0, 400)

pixel_size = Button(toolbar, text='Change Bitmap Size', command=defining_bitmap_size)

# Defines grid system
rows = Entry(toolbar, borderwidth=2)
cols = Entry(toolbar, borderwidth=2)
grid_button = Button(toolbar, text='Grid ON', command=draw_grid)

# Colors box of grid system
paint_button = Button(toolbar, text='Paint', command=draw_pixel_grid)

# Deletes all
clear_button = Button(toolbar, text='Clear', command=clear_canvas)

# Draws a circle
circle_button = Button(toolbar, text='◯', font=40, command=draw_circle)
circle_radio = Entry(toolbar, borderwidth=2)
circle_center_x = Entry(toolbar, borderwidth=2)
circle_center_y = Entry(toolbar, borderwidth=2)

# Draws a rectangle
rect_button = Button(toolbar, text='□', font=80, command=draw_rect)
rect_pos1 = Entry(toolbar, borderwidth=2)
rect_pos2 = Entry(toolbar, borderwidth=2)
rect_pos3 = Entry(toolbar, borderwidth=2)
rect_pos4 = Entry(toolbar, borderwidth=2)

# Draws a triangle
tri_button = Button(toolbar, text='△', font=40, command=draw_triangle)
tri_pos_x0 = Entry(toolbar, borderwidth=2)
tri_pos_x1 = Entry(toolbar, borderwidth=2)
tri_pos_y0 = Entry(toolbar, borderwidth=2)
tri_pos_y1 = Entry(toolbar, borderwidth=2)
tri_pos_z0 = Entry(toolbar, borderwidth=2)
tri_pos_z1 = Entry(toolbar, borderwidth=2)

# Import Image
img_pos_x = Entry(toolbar, borderwidth=2)
img_pos_y = Entry(toolbar, borderwidth=2)
img_size_x = Entry(toolbar, borderwidth=2)
img_size_y = Entry(toolbar, borderwidth=2)

# Saves canvas as a bitmap file
save_button = Button(canvas_frame, text='Save', command=save_file)

# -------------------------- Parameters -------------------------------------

# -------------------------- Beam Diameter ------------------------------------
beam_diameter = Label(parameters_bar, text='Beam Diameter: ', bg='white', fg='black')
beam_diameter.place(x=5, y=10, height=25)

beam_diameter_value = Entry(parameters_bar, borderwidth=2)
beam_diameter_value.place(x=95, y=12.5, width=40, height=20)

beam_unit = Label(parameters_bar, text='nm', bg='white', fg='black')
beam_unit.place(x=135, y=10, height=25)

# ------------------------------ Overlap --------------------------------------
overlap = Label(parameters_bar, text='Overlap: ', bg='white', fg='black')
overlap.place(x=160, y=10, height=25)

overlap_value = Entry(parameters_bar, borderwidth=2)
overlap_value.place(x=210, y=12.5, width=40, height=20)

percent = Label(parameters_bar, text='%', bg='white', fg='black')
percent.place(x=250, y=10, height=25)
# ----------------------- Show Milling Parameters -------------------------------


def pitch_value():
    if overlap_value.get() and beam_diameter_value:
        ov = float(overlap_value.get())/100
        bd = float(beam_diameter_value.get())
        pitch = bd*ov
        pitch_x.delete(0, END)
        pitch_y.delete(0, END)
        pitch_x.insert(0, pitch)
        pitch_y.insert(0, pitch)


calculate_pitch = Button(parameters_bar, text='Calculate Pitch', command=pitch_value)
calculate_pitch.place(x=290, y=10, height=25, width=100)

# ----------------------- Show Milling Parameters -------------------------------


def open_new_window():

    new_window = Toplevel(WIN)
    new_window.title("Milling Parameters")
    new_window.geometry("500x400")
    new_window.minsize(500, 400)
    new_window.maxsize(500, 400)

    my_notebook = ttk.Notebook(new_window)
    my_notebook.pack(pady=15)

    table = ttk.Treeview(my_notebook, height=14)
    table.pack()
    table['columns'] = "#1"
    table.heading("#0", text="Beam Current")
    table.heading("#1", text="Beam Diameter (nm)")
    table.column("#0", width=250, anchor=CENTER)
    table.column("#1", width=250, anchor=CENTER)
    table.insert("", END, text="90 pA", values="20.4 nm")
    table.insert("", END, text="41 pA", values="15 nm")
    table.insert("", END, text="26 pA", values="12.5 nm")
    table.insert("", END, text="7 pA", values="9.5 nm")
    table.insert("", END, text="1 pA", values="5.3 nm")
    table.insert("", END, text="0.26 nA", values="36.6 nm")
    table.insert("", END, text="0.44 nA", values="50.4 nm")
    table.insert("", END, text="0.75 nA", values="66.2 nm")
    table.insert("", END, text="1.2 nA", values="86.1 nm")
    table.insert("", END, text="2.4 nA", values="131 nm")
    table.insert("", END, text="9.1 nA", values="267 nm")
    table.insert("", END, text="20 nA", values="445 nm")
    table.insert("", END, text="47 nA", values="960 nm")
    table.insert("", END, text="65 nA", values="1500 nm")

    my_notebook.add(table, text="Beam Diameter at 30 kV")

    table2 = ttk.Treeview(my_notebook, height=14)
    table2.pack()
    table2['columns'] = ("1", "2", "#3")
    table2.heading("#0", text="Material")
    table2.heading("#1", text="Volume per Dose (µm3/nC)")
    table2.heading("#2", text="Material")
    table2.heading("#3", text="Volume per Dose (µm3/nC)")

    table2.column("#0", width=50, anchor=CENTER)
    table2.column("#1", width=200, anchor=CENTER)
    table2.column("#2", width=50, anchor=CENTER)
    table2.column("#3", width=200, anchor=CENTER)

    table2.insert("", END, text="C", values=("0.18", "Au", "1.50"))
    table2.insert("", END, text="Si", values=("0.27", "MgO", "0.27"))
    table2.insert("", END, text="Al", values=("0.30", "SiO2", "0.24"))
    table2.insert("", END, text="Ti", values=("0.37", "Al2O3", "0.08"))
    table2.insert("", END, text="Cr", values=("0.10", "TiO", "0.15"))
    table2.insert("", END, text="Fe", values=("0.29", "SiN4", "0.20"))
    table2.insert("", END, text="Ni", values=("0.14", "TiN", "0.15"))
    table2.insert("", END, text="Cu", values=("0.25", "Fe2O3", "0.25"))
    table2.insert("", END, text="Mo", values=("0.12", "GaAs", "0.61"))
    table2.insert("", END, text="Ta", values=("0.32", "Pt", "0.23"))
    table2.insert("", END, text="W", values=("0.12", "PMMA", "0.4"))

    my_notebook.add(table2, text="Material Volume per Dose Rates at 30 kV")


show_table = Button(parameters_bar, text='Show Milling Parameters', command=open_new_window)
show_table.place(x=400, y=10, height=25, width=150)

# ------------------------- Toolbar -------------------------------------

# -------------------- Number of Pixels ---------------------------------

# Pixel Size Label
label1 = Label(toolbar, text='─' * 8 + " Bitmap Size " + '─' * 8, bg="white", fg="black")
label1.place(x=0, y=0, width=200, height=15)

# Pitch X
label2 = Label(toolbar, text="Pitch X", bg="white").place(x=5, y=20, height=20, width=40)
pitch_x.place(x=55, y=20, height=20, width=40)

# Pitch Y
label3 = Label(toolbar, text="Pitch Y", bg="white").place(x=100, y=20, height=20, width=40)
pitch_y.place(x=150, y=20, height=20, width=40)

# Milling Area: X Dimension
label4 = Label(toolbar, text="X Size", bg="white").place(x=5, y=45, height=20, width=40)
size_x.place(x=55, y=45, height=20, width=40)

# Milling Area: Y Dimension
label5 = Label(toolbar, text="Y Size", bg="white").place(x=100, y=45, height=20, width=40)
size_y.place(x=150, y=45, height=20, width=40)

# Defining the number of pixels
pixel_size.place(x=5, y=70, height=25, width=190)

# --------------------- Grid System ---------------------------------

label6 = Label(toolbar, text='─' * 11 + " Grid " + '─' * 11, bg="white", fg="black")
label6.place(x=0, y=100, width=200, height=15)

# ------------------ Rows and Cols ----------------------------------
Label7 = Label(toolbar, text="Rows", bg="white").place(x=5, y=120, height=20, width=40)
Label8 = Label(toolbar, text="Cols", bg="white").place(x=100, y=120, height=20, width=40)

rows.place(x=55, y=120, height=20, width=40)
cols.place(x=150, y=120, height=20, width=40)

# ---------------------- Grid ----------------------------------------
grid_button.place(x=5, y=145, height=25, width=60)

# ------------------- Painting Grid ----------------------------------
paint_button.place(x=70, y=145, height=25, width=60)
clear_button.place(x=135, y=145, height=25, width=60)

# ------------------- Black or White ---------------------------------
label10 = LabelFrame(toolbar, text=' Color ', bg='white', padx=41)
label10.grid(padx=0, pady=175)

color = StringVar()
color.set('white')
color_white = Radiobutton(label10, text='white', variable=color, value='white').grid(row=0, column=0)
color_black = Radiobutton(label10, text='black', variable=color, value='black').grid(row=0, column=1)

# ---------------------- Patterns ------------------------------------
label9 = Label(toolbar, text='─' * 6 + " Patterns and Arrays " + '─' * 6, bg="white", fg="black")
label9.place(x=0, y=225, width=200, height=15)

# ----------------------- Array --------------------------------------
label11 = LabelFrame(toolbar, text=' Array Size ', height=45, width=90, bg='white')
label11.place(x=5, y=245)

matrix_row = Entry(label11, borderwidth=2)
matrix_row.place(x=5, y=0, width=30)
label12 = Label(label11, text='x', bg='white').place(x=30, y=0, width=20)
matrix_col = Entry(label11, borderwidth=2)
matrix_col.place(x=50, y=0, width=30)

# ------------------------ Period ------------------------------------
label13 = LabelFrame(toolbar, text=' Periodicity ', height=45, width=95, bg='white')
label13.place(x=100, y=245)

label14 = Label(label13, text='x:', bg='white').place(x=0, y=0, width=15)
period_x = Entry(label13, borderwidth=2)
period_x.place(x=15, y=0, width=25)

label15 = Label(label13, text='y:', bg='white').place(x=45, y=0, width=15)
period_y = Entry(label13, borderwidth=2)
period_y.place(x=60, y=0, width=25)

# --------------------------Circle-------------------------------------
circle_button.place(x=5, y=295, height=40, width=40)
label16 = Label(toolbar, text='Radio', bg='white').place(x=50, y=295, height=20, width=40)
circle_radio.place(x=95, y=295, height=20, width=100)

label17 = Label(toolbar, text='PosX', bg='white').place(x=50, y=315, height=20, width=40)
circle_center_x.place(x=95, y=315, height=20, width=30)

label18 = Label(toolbar, text='PosY', bg='white').place(x=125, y=315, height=20, width=40)
circle_center_y.place(x=165, y=315, height=20, width=30)

# --------------------------- rectangle ------------------------------------
rect_button.place(x=5, y=340, height=40, width=40)

label19 = Label(toolbar, text='X0', bg='white').place(x=50, y=340, height=20, width=30)
rect_pos1.place(x=80, y=340, height=20, width=40)
label20 = Label(toolbar, text='Y0', bg='white').place(x=125, y=340, height=20, width=30)
rect_pos2.place(x=155, y=340, height=20, width=40)

label21 = Label(toolbar, text='X1', bg='white').place(x=50, y=360, height=20, width=30)
rect_pos3.place(x=80, y=360, height=20, width=40)
label22 = Label(toolbar, text='Y1', bg='white').place(x=125, y=360, height=20, width=30)
rect_pos4.place(x=155, y=360, height=20, width=40)

# --------------------------- Triangle ------------------------------------
tri_button.place(x=5, y=387.5, height=40, width=40)
label23 = Label(toolbar, text='P1:', bg='white').place(x=50, y=385, height=15, width=30)
label24 = Label(toolbar, text='(', bg='white').place(x=80, y=385, height=15)
tri_pos_x0.place(x=90, y=385, height=15, width=40)
label25 = Label(toolbar, text=',', bg='white').place(x=130, y=385, height=15)
tri_pos_x1.place(x=145, y=385, height=15, width=40)
label26 = Label(toolbar, text=')', bg='white').place(x=185, y=385, height=15)

label27 = Label(toolbar, text='P2:', bg='white').place(x=50, y=400, height=15, width=30)
label28 = Label(toolbar, text='(', bg='white').place(x=80, y=400, height=15)
tri_pos_y0.place(x=90, y=400, height=15, width=40)
label29 = Label(toolbar, text=',', bg='white').place(x=130, y=400, height=15)
tri_pos_y1.place(x=145, y=400, height=15, width=40)
label30 = Label(toolbar, text=')', bg='white').place(x=185, y=400, height=15)

label31 = Label(toolbar, text='P3:', bg='white').place(x=50, y=415, height=15, width=30)
label32 = Label(toolbar, text='(', bg='white').place(x=80, y=415, height=15)
tri_pos_z0.place(x=90, y=415, height=15, width=40)
label33 = Label(toolbar, text=',', bg='white').place(x=130, y=415, height=15)
tri_pos_z1.place(x=145, y=415, height=15, width=40)
label34 = Label(toolbar, text=')', bg='white').place(x=185, y=415, height=15)

# ----------------------------- 3D -------------------------------------------
label35 = Label(toolbar, text='─' * 8 + ' 3D Structures ' + '─' * 8, bg='white', fg='black')
label35.place(x=0, y=435, width=200, height=15)

# ------------------------- Quadratic ----------------------------------------

label36 = LabelFrame(toolbar, text=' Quadratic Structure ', bg='white')
label36.place(x=5, y=455, height=45, width=190)

label37 = Label(label36, text='Cap height:', bg='white').place(x=5, y=0, width=65)
cap_height = Entry(label36, borderwidth=2)
cap_height.place(x=70, y=0, width=35)

label38 = Label(label36, text='Radio:', bg='white').place(x=105, y=0, width=40)
radio = Entry(label36, borderwidth=2)
radio.place(x=145, y=0, width=35)

# ------------------------- V-Groove ----------------------------------------
label50 = LabelFrame(toolbar, text=' V-Groove Structure ', bg='white')
label50.place(x=5, y=500, height=45, width=190)

label51 = Label(label50, text='Depth:', bg='white').place(x=5, y=0, width=65)
depth = Entry(label50, borderwidth=2)
depth.place(x=70, y=0, width=35)

label52 = Label(label50, text='Slope:', bg='white').place(x=105, y=0, width=40)
slope = Entry(label50, borderwidth=2)
slope.place(x=145, y=0, width=35)

# ---------------------------- Show 3D ----------------------------------------

show_3d_structure = Button(cross_view_frame, text='Show 3D structure',
                           command=lambda: (show_grayscale_bitmap(), show_grayscale_cross_view()))

show_3d_structure.pack()
show_3d_structure.configure(height=1, width=15)

# -------------------------- Import Image -----------------------------------
import_image = Button(toolbar, text='Import Image', command=import_file)
import_image.place(x=5, y=550, height=40, width=80)

label39 = Label(toolbar, text='Pos', bg='white').place(x=90, y=550, width=20, height=20)
label40 = Label(toolbar, text='(', bg='white').place(x=110, y=550, width=10, height=20)
img_pos_x.place(x=120, y=550, width=30, height=20)
label41 = Label(toolbar, text=',', bg='white').place(x=150, y=550, width=5, height=20)
img_pos_y.place(x=155, y=550, width=30, height=20)
label42 = Label(toolbar, text=')', bg='white').place(x=185, y=550, width=10, height=20)

label43 = Label(toolbar, text='Size', bg='white').place(x=90, y=570, width=20, height=20)
label44 = Label(toolbar, text='(', bg='white').place(x=110, y=570, width=10, height=20)
img_size_x.place(x=120, y=570, width=30, height=20)
label45 = Label(toolbar, text=',', bg='white').place(x=150, y=570, width=5, height=20)
img_size_y.place(x=155, y=570, width=30, height=20)
label46 = Label(toolbar, text=')', bg='white').place(x=185, y=570, width=10, height=20)

# ---------------------------- Save -----------------------------------------
save_button.pack(side=BOTTOM, anchor=SE)
save_button.config(height=1, width=10)

# ---------------------- Showing Coordinates --------------------------------

WIN.mainloop()
