from tkinter import *


def btn_clicked():
    print("Button Clicked")


window = Absensi()

window.geometry("1128x700")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 700,
    width = 1128,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    539.0, 353.5,
    image=background_img)

canvas.create_text(
    321.5, 119.0,
    text = "PAPAN INFORMASI",
    fill = "#ffffff",
    font = ("ArialRoundedMTBold", int(12.0)))

canvas.create_text(
    281.0, 154.0,
    text = "Jumlah User",
    fill = "#ffffff",
    font = ("ArialRoundedMTBold", int(12.0)))

canvas.create_text(
    277.0, 183.0,
    text = "Jam Masuk",
    fill = "#ffffff",
    font = ("ArialRoundedMTBold", int(12.0)))

canvas.create_text(
    279.0, 212.0,
    text = "Jam Keluar",
    fill = "#ffffff",
    font = ("ArialRoundedMTBold", int(12.0)))

canvas.create_text(
    345.5, 154.0,
    text = ": 12",
    fill = "#ffffff",
    font = ("ArialRoundedMTBold", int(12.0)))

canvas.create_text(
    359.5, 183.0,
    text = ": 07:00:00",
    fill = "#ffffff",
    font = ("ArialRoundedMTBold", int(12.0)))

canvas.create_text(
    359.5, 212.0,
    text = ": 16:00:00",
    fill = "#ffffff",
    font = ("ArialRoundedMTBold", int(12.0)))

canvas.create_text(
    81.5, 342.5,
    text = "NAMA",
    fill = "#ffffff",
    font = ("ArialRoundedMTBold", int(12.0)))

canvas.create_text(
    76.5, 288.0,
    text = "PRESENSI HARI INI",
    fill = "#ffffff",
    font = ("ArialRoundedMTBold", int(12.0)))

canvas.create_text(
    23.5, 344.0,
    text = "NO",
    fill = "#ffffff",
    font = ("ArialRoundedMTBold", int(12.0)))

canvas.create_text(
    195.5, 342.5,
    text = "JAM MASUK",
    fill = "#ffffff",
    font = ("ArialRoundedMTBold", int(12.0)))

canvas.create_text(
    330.5, 342.5,
    text = "JAM KELUAR",
    fill = "#ffffff",
    font = ("ArialRoundedMTBold", int(12.0)))

canvas.create_text(
    25.0, 379.0,
    text = "1",
    fill = "#000000",
    font = ("ArialRoundedMTBold", int(11.0)))

canvas.create_text(
    96.0, 378.0,
    text = "STARDUST",
    fill = "#000000",
    font = ("ArialRoundedMTBold", int(11.0)))

canvas.create_text(
    213.0, 378.0,
    text = "08:00:00",
    fill = "#000000",
    font = ("ArialRoundedMTBold", int(11.0)))

canvas.create_text(
    346.0, 377.0,
    text = "15:00:00",
    fill = "#000000",
    font = ("ArialRoundedMTBold", int(11.0)))

entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    627.5, 202.0,
    image = entry0_img)

entry0 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry0.place(
    x = 525.0, y = 186,
    width = 205.0,
    height = 30)

canvas.create_text(
    575.0, 165.0,
    text = "ENROLLMENT/ID",
    fill = "#ffffff",
    font = ("ArialRoundedMTBold", int(12.0)))

entry1_img = PhotoImage(file = f"img_textBox1.png")
entry1_bg = canvas.create_image(
    625.5, 549.0,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry1.place(
    x = 552.0, y = 533,
    width = 147.0,
    height = 30)

canvas.create_text(
    567.5, 519.5,
    text = "DARI",
    fill = "#ffffff",
    font = ("ArialRoundedMTBold", int(11.0)))

entry2_img = PhotoImage(file = f"img_textBox2.png")
entry2_bg = canvas.create_image(
    625.5, 622.0,
    image = entry2_img)

entry2 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry2.place(
    x = 552.0, y = 606,
    width = 147.0,
    height = 30)

canvas.create_text(
    574.5, 593.5,
    text = "SAMPAI",
    fill = "#ffffff",
    font = ("ArialRoundedMTBold", int(11.0)))

entry3_img = PhotoImage(file = f"img_textBox3.png")
entry3_bg = canvas.create_image(
    886.5, 548.0,
    image = entry3_img)

entry3 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry3.place(
    x = 813.0, y = 532,
    width = 147.0,
    height = 30)

canvas.create_text(
    824.0, 518.5,
    text = "DARI",
    fill = "#ffffff",
    font = ("ArialRoundedMTBold", int(11.0)))

entry4_img = PhotoImage(file = f"img_textBox4.png")
entry4_bg = canvas.create_image(
    886.5, 621.0,
    image = entry4_img)

entry4 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry4.place(
    x = 813.0, y = 605,
    width = 147.0,
    height = 30)

canvas.create_text(
    831.5, 592.5,
    text = "SAMPAI",
    fill = "#ffffff",
    font = ("ArialRoundedMTBold", int(11.0)))

entry5_img = PhotoImage(file = f"img_textBox5.png")
entry5_bg = canvas.create_image(
    627.5, 297.0,
    image = entry5_img)

entry5 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry5.place(
    x = 525.0, y = 281,
    width = 205.0,
    height = 30)

canvas.create_text(
    553.5, 264.5,
    text = "JABATAN",
    fill = "#ffffff",
    font = ("ArialRoundedMTBold", int(12.0)))

entry6_img = PhotoImage(file = f"img_textBox6.png")
entry6_bg = canvas.create_image(
    893.5, 202.0,
    image = entry6_img)

entry6 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry6.place(
    x = 791.0, y = 186,
    width = 205.0,
    height = 30)

canvas.create_text(
    811.5, 164.5,
    text = "NAMA",
    fill = "#ffffff",
    font = ("ArialRoundedMTBold", int(12.0)))

entry7_img = PhotoImage(file = f"img_textBox7.png")
entry7_bg = canvas.create_image(
    893.5, 297.0,
    image = entry7_img)

entry7 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry7.place(
    x = 791.0, y = 281,
    width = 205.0,
    height = 30)

canvas.create_text(
    817.0, 264.5,
    text = "ALAMAT",
    fill = "#ffffff",
    font = ("ArialRoundedMTBold", int(12.0)))

canvas.create_text(
    281.5, 688.5,
    text = "CREATED BY : kelompok cemara         ",
    fill = "#ffffff",
    font = ("ArialRoundedMTBold", int(10.0)))

canvas.create_text(
    623.5, 474.5,
    text = "JAM MASUK",
    fill = "#ffffff",
    font = ("ArialRoundedMTBold", int(12.0)))

canvas.create_text(
    887.5, 475.0,
    text = "JAM KELUAR",
    fill = "#ffffff",
    font = ("ArialRoundedMTBold", int(12.0)))

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 499, y = 18,
    width = 97,
    height = 33)

img1 = PhotoImage(file = f"img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b1.place(
    x = 380, y = 18,
    width = 97,
    height = 33)

img2 = PhotoImage(file = f"img2.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b2.place(
    x = 969, y = 333,
    width = 104,
    height = 35)

img3 = PhotoImage(file = f"img3.png")
b3 = Button(
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b3.place(
    x = 981, y = 625,
    width = 79,
    height = 25)

img4 = PhotoImage(file = f"img4.png")
b4 = Button(
    image = img4,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b4.place(
    x = 620, y = 18,
    width = 97,
    height = 33)

img5 = PhotoImage(file = f"img5.png")
b5 = Button(
    image = img5,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b5.place(
    x = 743, y = 18,
    width = 97,
    height = 33)

img6 = PhotoImage(file = f"img6.png")
b6 = Button(
    image = img6,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b6.place(
    x = 987, y = 18,
    width = 97,
    height = 33)

img7 = PhotoImage(file = f"img7.png")
b7 = Button(
    image = img7,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b7.place(
    x = 866, y = 18,
    width = 97,
    height = 33)

img8 = PhotoImage(file = f"img8.png")
b8 = Button(
    image = img8,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b8.place(
    x = 249, y = 18,
    width = 111,
    height = 33)

canvas.create_text(
    772.0, 115.5,
    text = "INPUT DATA USER",
    fill = "#ffffff",
    font = ("None", int(14.0)))

canvas.create_text(
    776.0, 448.5,
    text = "UBAH WAKTU PRESENSI",
    fill = "#ffffff",
    font = ("None", int(14.0)))

window.resizable(False, False)
window.mainloop()
