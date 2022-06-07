'''
=======================================================================================================
                                            IMPORT LIBRARY
=======================================================================================================
'''
import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
from tkinter import messagebox
import cv2
import csv
import os
import requests
import numpy as np
import hashlib
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
from pathlib import Path
from tkinter import ttk
import mysql.connector

# %%
window = tk.Tk()
icon_DA = PhotoImage(file='assets/img/bg-2.png')
window.tk.call('wm', 'iconphoto', window._w, icon_DA)
#setting window size
width=1128
height=700
screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
window.geometry(alignstr)
window.resizable(width=False, height=False)
cur_dir = Path.cwd()

''''
=========================================KONEKSI DATABASE===============================================
                            JIKA DATABASE TIDAK TERKONEKSI APLIKASI TIDAK AKAN BERJALAN

========================================================================================================
'''
global mydb, koneksi, username

dataDB  = {}
def koneksiDB():
    data    = []
    with open('{}/config/database/database.csv'.format(cur_dir)) as fileDb:
        reader = csv.DictReader(fileDb)
        for x in reader:
            data.append(x)
    for row in data:
        host = f"{row['HOST']}"
        user = f"{row['USER']}"
        pw   = f"{row['PASSWORD']}"
        db   = f"{row['DATABASE']}"
    return dataDB.update({'host':host,
                    'user':user,
                    'pw':pw,
                    'db':db})

koneksiDB()
try:
    mydb    = mysql.connector.connect(  host=dataDB['host'], 
                                        user=dataDB['user'],
                                        password=dataDB['pw'], 
                                        database=dataDB['db'])
    if(dataDB['host']==''):
        messagebox.showinfo('INFORMASI','Lakukan konfigurasi pada database terlebih dahulu')
        dbConnected = False
    else:
        koneksi = mydb.cursor()
        print('DATABASE CONNECTED')
        dbConnected = True
except Exception as tampil:
   messagebox.showinfo("DATABASE ERROR", tampil)
   dbConnected = False

''''
========================================METHOD UNTUK REFRES KONEKSI DATABASE======================================
'''
def database():
    try:
        if(dbConnected == True):
            koneksi = mydb.cursor()
            return koneksi
    except Exception as tampil:
        messagebox.showinfo("DATABASE ERROR", tampil)
'''
====================================METHOD UNTUK MENAMPILKAN POPUP INFORMASI======================================
'''
def info(jenis,pesan):
    messagebox.showinfo(jenis, pesan)
'''
====================================METHOD UNTUK MENAMPILKAN POPUP ERROR======================================
'''
def error(pesan):
    messagebox.showerror('ERROR',pesan)
'''
======================METHOD UNTUK MENGEMBALIKAN NILAI STATUS TABEL TAKE IMAGE====================================
'''
def retak():
    database()
    koneksi.execute("UPDATE tb_take_image SET status = '0',nama = '',enrollment = ''")
    mydb.commit()
'''
================================METHOD UNTUK MENGIRIMKAN DATA LOG KE DATABASE====================================
'''
def log(log):
    database()
    sql = ("INSERT INTO log SET log = '{}'".format(str(log)))
    koneksi.execute(sql)
    mydb.commit()
'''
================================METHOD UNTUK MENGAMBIL DATA PENGATURAN APLIKASI====================================
'''
dataPengaturan = {}
def dbPengaturan():
    with open('{}/config/database/pengaturan.csv'.format(cur_dir)) as file:
        reader = csv.DictReader(file)
        for r in reader:
            server      = r['SERVER']
            kamera   = r['KAMERA']
            header      = r['HEADER']
    return dataPengaturan.update({  'server': server,
                                    'kamera': kamera,
                                    'header': header})
    
'''
================================METHOD UNTUK MENGAMBIL DATA PRESENSI HARI INI====================================
'''
dNama = []
dJamMasuk = []
dJamKeluar = []
def presensiHariIni():
    database()
    sql = ("SELECT nama, clockin, clockout FROM tb_presensi WHERE tanggal = '{}' ORDER BY clockin ASC LIMIT 10".format(time.strftime("%Y-%m-%d")))
    koneksi.execute(sql)
    result = koneksi.fetchall()

    for x in result:
        dNama.append(x[0])
        dJamMasuk.append(x[1])
        dJamKeluar.append(x[2])
'''
================================METHOD UNTUK MENGAHAPUS KARAKTER SPESIAL==========================================
'''
def remove_special_characters(character):
    if character.isalnum() or character == ' ':
        return True
    else:
        return False
'''
================================METHOD UNTUK MENGAHAPUS SPASI====================================================
'''
def rSpasi(text):
    return "".join(text.split())
'''
==================   METHOD UNTUK MENGAMBIL DATA WAKTU PRESENSI MASUK/KELUAR    =================================
'''
waktu = {}
def dataWaktu():
    #Mengambil data waktu presensi masuk dan keluar
    waktuMasuk  = koneksi.execute("SELECT dari, sampai FROM tb_waktu_masuk")
    wMasuk      = koneksi.fetchall()
    waktuKeluar = koneksi.execute("SELECT dari, sampai FROM tb_waktu_keluar")
    wKeluar     = koneksi.fetchall()

    for x in wMasuk:
        dariwm      = x[0]
        sampaiwm    = x[1]
    for i in wKeluar:
        dariwk      = i[0]
        sampaiwk    = i[1]
    return waktu.update({'dariwm':dariwm,
                         'sampaiwm':sampaiwm,
                         'dariwk':dariwk,
                         'sampaiwk':sampaiwk})
'''
================================METHOD UNTUK MENGHITUNG JUMLAH USERS====================================
'''
def jmlUser():
    koneksi.execute('SELECT COUNT(id) FROM tb_users')
    data = str(koneksi.fetchall())

    return "".join(a for a in data if a.isalnum())
'''
================================METHOD UNTUK MENDAPATKAN IMAGES LABELS==========================================
'''    
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faceSamples = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image

        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces = detector.detectMultiScale(imageNp)
        # If a face is there then append that in the list as well as Id of it
        for (x, y, w, h) in faces:
            faceSamples.append(imageNp[y:y + h, x:x + w])
            Ids.append(Id)
    return faceSamples, Ids


window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

'''
================================METHOD UNTUK KELUAR APLIKASI===================================================
'''
def on_closing():
    if messagebox.askokcancel("KELUAR", "Apakah anda yakin?"):
        if(dbConnected == True):
            log("Log out")
        window.destroy()
        


window.protocol("WM_DELETE_WINDOW", on_closing)

'''
============================================CLASS APP========================================================
                                ============CLASS APP===========
                                    ========CLASS APP=======
=============================================================================================================
'''
class App:
    '''
=============================================================================================================
                                        INTERFACE DAN VALIDASI SAAT LOGIN

=============================================================================================================
'''
    def login(self):
        def validasi():
            try:
                username    = str(en_username.get())
                get_pw      = hashlib.md5(enPassword.get().encode())
                password    = str(get_pw.hexdigest())
                koneksi.execute("SELECT username, password FROM tb_admin WHERE username = '{}' AND password = '{}'".format(username,password))
                hasil       = str(koneksi.fetchall())

                if hasil != "[]":
                    print("berhasil cok")
                    log("Login")
                    self.halaman()
                else:
                    info("Gagal","USERNAME/PASSWORD SALAH")
                    log("username/password salah")
            except Exception as error:
                log("validasi error")
                print(error)
        window.title('LOGIN')
        window.configure(bg = "#ffffff")
        canvas = Canvas(
            window,
            bg = "#ffffff",
            height = 740,
            width = 1128,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        canvas.place(x = 0, y = 0)

        canvas.create_text(
            73.0, 58.0,
            text = "LOGO",
            fill = "#000000",
            font = ("None", int(25.0)))

        canvas.create_text(
            889.5, 171.5,
            text = "SELAMAT DATANG!",
            fill = "#000000",
            font = ("ArchivoBlack-Regular", int(25.0)))

        canvas.create_text(
            885.5, 210.5,
            text = "Silahkan login menggunakan username dan password",
            fill = "#000000",
            font = ("None", int(11.0)))

        entry0_img = PhotoImage(file = f"Views/login/img_textBox0.png")
        entry0_bg = canvas.create_image(
            915.0, 333.0,
            image = entry0_img)

        en_username = Entry(
            bd = 0,
            bg = "#c4c4c4",
            highlightthickness = 0)

        en_username.place(
            x = 766.0, y = 310,
            width = 298.0,
            height = 44)

        entry1_img = PhotoImage(file = f"Views/login/img_textBox1.png")
        entry1_bg = canvas.create_image(
            915.0, 455.0,
            image = entry1_img)

        enPassword = Entry(
            bd = 0,
            bg = "#c4c4c4",
            highlightthickness = 0,
            show='*')

        enPassword.place(
            x = 766.0, y = 432,
            width = 298.0,
            height = 44)

        canvas.create_text(
            821.0, 283.5,
            text = "USERNAME",
            fill = "#000000",
            font = ("None", int(14.0)))

        canvas.create_text(
            821.0, 407.5,
            text = "PASSWORD",
            fill = "#000000",
            font = ("None", int(14.0)))

        canvas.create_text(
            821.0, 407.5,
            text = "PASSWORD",
            fill = "#000000",
            font = ("None", int(14.0)))

        background_img = PhotoImage(file = f"Views/login/background.png")
        background = canvas.create_image(
            598.0, 400.5,
            image=background_img)

        img0 = PhotoImage(file = f"Views/login/img0.png")
        b0 = Button(
            image = img0,
            borderwidth = 0,
            highlightthickness = 0,
            command = validasi,
            relief = "flat")

        b0.place(
            x = 963, y = 532,
            width = 108,
            height = 39)

        window.resizable(False, False)
        window.mainloop()

    def __init__(self, window):
        dbPengaturan()
        if(dbConnected == True):
            self.login() 
        else:
            window.destroy()
            self.pengaturan()
        
        '''
======================================================================================================================
                                        INTERFACE HALAMAN UTAMA 
                                    KET:
                                        wMasuk      == Waktu Masuk
                                        wKeluar     == Waktu Keluar
                                        dariwm      == data kolom "dari" yang terdapat pada tabel waktu
                                                       presensi masuk
                                        sampaiwm    == data kolom "sampai" yang terdapat pada tabel waktu
                                                       presensi masuk
                                        dariwk      == data kolom "dari" yang terdapat pada tabel waktu
                                                       presensi keluar
                                        sampaiwk    == data kolom "sampai" yang terdapat pada tabel waktu
                                                       presensi keluar

=======================================================================================================================
'''
        
    def halaman(self):
        database()
        presensiHariIni()
        dbPengaturan()
        global en_nama, en_id, en_dari_wk, en_dari_wm, en_sampai_wk, en_sampai_wm, en_jabatan, en_alamat
        dataWaktu()

        #INTERFACE HALAMAN UTAMA
        window.title(dataPengaturan['header'])

        menubar = Menu(window)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Dashboard",
                             command=self.halaman)
        filemenu.add_command(label="Mulai Presensi", command=self.start)
        filemenu.add_command(label="User Terdaftar", command=self.lihat_data)
        filemenu.add_command(label="Pengaturan",
                             command=self.pengaturan)
        filemenu.add_command(label="Data Users",
                             command=self.lihat_data)

        filemenu.add_separator()

        filemenu.add_command(label="Keluar", command=window.quit)
        menubar.add_cascade(label="Menu", menu=filemenu)
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Remote",
                             command=self.remote)
        editmenu.add_command(label="Test Kamera",
                             command=self.testCamera)

        editmenu.add_separator()

        editmenu.add_command(label="test kamera", command=self.testCamera)

        menubar.add_cascade(label="Tools", menu=editmenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Test Kamera", command=self.testCamera)
        helpmenu.add_command(label="About...", command="")
        menubar.add_cascade(label="Help", menu=helpmenu)

        window.config(menu=menubar)

        menubutton = Menubutton(window, text="File", width=70)
        menubutton.menu = Menu(menubutton)
        menubutton["menu"] = menubutton.menu
        menubutton.menu.add_checkbutton(label="New file", variable=IntVar())
        menubutton.menu.add_checkbutton(label="Save", variable=IntVar())
        menubutton.menu.add_checkbutton(label="Save as", variable=IntVar())

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

        background_img = PhotoImage(file = f"Views/dashboard/background.png")
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
            345.5, 154.0,
            text = ": {}".format(jmlUser()),
            fill = "#ffffff",
            font = ("ArialRoundedMTBold", int(12.0)))

        canvas.create_text(
            277.0, 183.0,
            text = "Jam Masuk",
            fill = "#ffffff",
            font = ("ArialRoundedMTBold", int(12.0)))

        canvas.create_text(
            359.5, 183.0,
            text = ": {}".format(waktu['dariwm']),
            fill = "#ffffff",
            font = ("ArialRoundedMTBold", int(12.0)))

        canvas.create_text(
            279.0, 212.0,
            text = "Jam Keluar",
            fill = "#ffffff",
            font = ("ArialRoundedMTBold", int(12.0)))

        canvas.create_text(
            359.5, 212.0,
            text = ": {}".format(waktu['dariwk']),
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
        h = 379.0
        line = 400
        no = 1
        for x in range(len(dNama)):
            canvas.create_text(
                25.0, h,
                text = no,
                fill = "#000000",
                font = ("ArialRoundedMTBold", int(11.0)))

            canvas.create_text(
                96.0, h,
                text = dNama[x],
                fill = "#000000",
                font = ("ArialRoundedMTBold", int(11.0)))

            canvas.create_text(
                213.0, h,
                text = dJamMasuk[x],
                fill = "#000000",
                font = ("ArialRoundedMTBold", int(11.0)))

            canvas.create_text(
                346.0, h,
                text = dJamKeluar[x],
                fill = "#000000",
                font = ("ArialRoundedMTBold", int(11.0)))

            h += 30
            no += 1

        canvas.create_text(
            623.5, 474.5,
            text = "JAM MASUK",
            fill = "#ffffff",
            font = ("ArialRoundedMTBold", int(12.0)))

        canvas.create_text(
            567.5, 519.5,
            text = "DARI",
            fill = "#ffffff",
            font = ("ArialRoundedMTBold", int(11.0)))

        entry1_img = PhotoImage(file = f"Views/dashboard/img_textBox1.png")
        entry1_bg = canvas.create_image(
            625.5, 549.0,
            image = entry1_img)

        en_dari_wm = Entry(
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0)

        en_dari_wm.place(
            x = 552.0, y = 533,
            width = 147.0,
            height = 30)

        en_dari_wm.insert(0,waktu['dariwm'])

        canvas.create_text(
            574.5, 593.5,
            text = "SAMPAI",
            fill = "#ffffff",
            font = ("ArialRoundedMTBold", int(11.0)))

        entry2_img = PhotoImage(file = f"Views/dashboard/img_textBox2.png")
        entry2_bg = canvas.create_image(
            625.5, 622.0,
            image = entry2_img)

        en_sampai_wm = Entry(
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0)

        en_sampai_wm.place(
            x = 552.0, y = 606,
            width = 147.0,
            height = 30)

        en_sampai_wm.insert(0, waktu['sampaiwm'])

        canvas.create_text(
            887.5, 475.0,
            text = "JAM KELUAR",
            fill = "#ffffff",
            font = ("ArialRoundedMTBold", int(12.0)))

        canvas.create_text(
            824.0, 518.5,
            text = "DARI",
            fill = "#ffffff",
            font = ("ArialRoundedMTBold", int(11.0)))

        entry3_img = PhotoImage(file = f"Views/dashboard/img_textBox3.png")
        entry3_bg = canvas.create_image(
            886.5, 548.0,
            image = entry3_img)

        en_dari_wk = Entry(
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0)

        en_dari_wk.place(
            x = 813.0, y = 532,
            width = 147.0,
            height = 30)

        en_dari_wk.insert(0, waktu['dariwk'])

        canvas.create_text(
            831.5, 592.5,
            text = "SAMPAI",
            fill = "#ffffff",
            font = ("ArialRoundedMTBold", int(11.0)))

        entry4_img = PhotoImage(file = f"Views/dashboard/img_textBox4.png")
        entry4_bg = canvas.create_image(
            886.5, 621.0,
            image = entry4_img)

        en_sampai_wk = Entry(
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0)

        en_sampai_wk.place(
            x = 813.0, y = 605,
            width = 147.0,
            height = 30)

        en_sampai_wk.insert(0, waktu['sampaiwk'])

        img3 = PhotoImage(file = f"Views/dashboard/img3.png")
        b3 = Button(
            image = img3,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.simpan_waktu,
            relief = "flat")

        canvas.create_text(
            575.0, 165.0,
            text = "ENROLLMENT/ID",
            fill = "#ffffff",
            font = ("ArialRoundedMTBold", int(12.0)))

        entry0_img = PhotoImage(file = f"Views/dashboard/img_textBox0.png")
        entry0_bg = canvas.create_image(
            627.5, 202.0,
            image = entry0_img)

        en_id = Entry(
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0)

        en_id.place(
            x = 525.0, y = 186,
            width = 205.0,
            height = 30)

        canvas.create_text(
            811.5, 164.5,
            text = "NAMA",
            fill = "#ffffff",
            font = ("ArialRoundedMTBold", int(12.0)))

        entry6_img = PhotoImage(file = f"Views/dashboard/img_textBox6.png")
        entry6_bg = canvas.create_image(
            893.5, 202.0,
            image = entry6_img)

        en_nama = Entry(
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0)

        en_nama.place(
            x = 791.0, y = 186,
            width = 205.0,
            height = 30)

        canvas.create_text(
            553.5, 264.5,
            text = "JABATAN",
            fill = "#ffffff",
            font = ("ArialRoundedMTBold", int(12.0)))

        entry5_img = PhotoImage(file = f"Views/dashboard/img_textBox5.png")
        entry5_bg = canvas.create_image(
            627.5, 297.0,
            image = entry5_img)

        en_jabatan = Entry(
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0)

        en_jabatan.place(
            x = 525.0, y = 281,
            width = 205.0,
            height = 30)

        canvas.create_text(
            817.0, 264.5,
            text = "ALAMAT",
            fill = "#ffffff",
            font = ("ArialRoundedMTBold", int(12.0)))

        entry7_img = PhotoImage(file = f"Views/dashboard/img_textBox7.png")
        entry7_bg = canvas.create_image(
            893.5, 297.0,
            image = entry7_img)

        en_alamat = Entry(
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0)

        en_alamat.place(
            x = 791.0, y = 281,
            width = 205.0,
            height = 30)

        img2 = PhotoImage(file = f"Views/dashboard/img2.png")
        b2 = Button(
            image = img2,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.take_img,
            relief = "flat")

        img0 = PhotoImage(file = f"Views/dashboard/img0.png")
        b0 = Button(
            image = img0,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.remote,
            relief = "flat")

        b0.place(
            x = 499, y = 18,
            width = 97,
            height = 33)

        img1 = PhotoImage(file = f"Views/dashboard/img1.png")
        b1 = Button(
            image = img1,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.testCamera,
            relief = "flat")

        b1.place(
            x = 380, y = 18,
            width = 97,
            height = 33)

        b2.place(
            x = 969, y = 333,
            width = 104,
            height = 35)

        b3.place(
            x = 981, y = 625,
            width = 79,
            height = 25)

        img4 = PhotoImage(file = f"Views/dashboard/img4.png")
        b4 = Button(
            image = img4,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.training,
            relief = "flat")

        b4.place(
            x = 620, y = 18,
            width = 97,
            height = 33)

        img5 = PhotoImage(file = f"Views/dashboard/img5.png")
        b5 = Button(
            image = img5,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.lihat_data,
            relief = "flat")

        b5.place(
            x = 743, y = 18,
            width = 97,
            height = 33)

        img6 = PhotoImage(file = f"Views/dashboard/img6.png")
        b6 = Button(
            image = img6,
            borderwidth = 0,
            highlightthickness = 0,
            command = "",
            relief = "flat")

        b6.place(
            x = 987, y = 18,
            width = 97,
            height = 33)

        img7 = PhotoImage(file = f"Views/dashboard/img7.png")
        b7 = Button(
            image = img7,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.pengaturan,
            relief = "flat")

        b7.place(
            x = 866, y = 18,
            width = 97,
            height = 33)

        img8 = PhotoImage(file = f"Views/dashboard/img8.png")
        b8 = Button(
            image = img8,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.start,
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

        canvas.create_text(
            200, 688.5,
            text = "CREATED BY : DEFA NUGARAHA             HAPPY CODING >_",
            fill = "#ffffff",
            font = ("ArialRoundedMTBold", int(10.0)))

        window.resizable(False, False)
        window.mainloop()


        '''
===================================================================================================================
                                       FITUR REMOTE MELALUI WEBSITE
                                      [AGAR DAPAT DIAKSES JARAK JAUH] 

===================================================================================================================
'''               
    def remote(self):
        while(True):
            koneksiDB()
            import mysql.connector as sql
            db = sql.connect(host="{}".format(dataDB['host']),user="{}".format(dataDB['user']),password="{}".format(dataDB['pw']),database="{}".format(dataDB['db']))

            #mengambil data status (untuk mengecek ada perintah untuk take image (ambil sample gambar) atau tidak)
            koneksi     = db.cursor()
            koneksi.execute("SELECT status FROM tb_take_image")
            sql         = koneksi.fetchall()
            for row in sql:
                take    = int(row[0])

            #mengambil data dari tabel controls
            koneksi.execute("SELECT * FROM tb_controls")
            hasil       = koneksi.fetchall()
            for data in hasil:
                status  = data[1]
                start   = data[2]
                stop    = data[3]
                train   = data[4]
                destroy = data[5]

            #REMOTE
            if status == 1:
                if(take == 1):
                    self.takeRemote()
                    break
                if start == 1:
                    print("start")
                    self.start(True)
                    break
                if stop == 1:
                    window.destroy()
                    print("stop")
                    break
                if train == 1:
                    print("train")
                    self.training()
                    break
                print('status aktif')
            elif status == 0:
                info('INFO','Aktifkan "CONTROL DEVICE" pada web terlebih dahulu')
                break
        '''
===================================================================================================================================
                                        MENGAMBIL SAMPLE GAMBAR [FITUR REMOTE]

===================================================================================================================================
'''     
    def takeRemote(self):
        dbPengaturan()
        while(True):
            database()            
            koneksi.execute("SELECT nama FROM tb_take_image WHERE status = '1'")
            hasil = koneksi.fetchall()
            for i in hasil:
                nama = i[0]
            koneksi.execute("SELECT enrollment FROM tb_take_image WHERE status = '1'")
            data = koneksi.fetchall()
            for x in data:
                Id = x[0]
            if nama == '' and Id == '':
                log("MASUKAN ID DAN NAMA")
                retak()
                break
            else:
                try:
                    cam         = cv2.VideoCapture(0)
                    detector    = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                    Enrollment  = Id
                    Name        = nama
                    sampleNum   = 0

                    if(dataPengaturan['kamera']== 'fullscreen'):
                        cv2.namedWindow('Take Image', cv2.WND_PROP_FULLSCREEN)
                        cv2.setWindowProperty('Take Image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

                    while (True):
                        ret, img = cam.read()
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        faces = detector.detectMultiScale(gray, 1.3, 5)
                        for (x, y, w, h) in faces:
                            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                            # incrementing sample number
                            sampleNum = sampleNum + 1
                            # saving the captured face in the dataset folder
                            cv2.imwrite(str(cur_dir)+"/TrainingImage/" + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg",
                                        gray[y:y + h, x:x + w])
                            cv2.imshow('Take Image', img)
                        # wait for 100 miliseconds
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                        # break if the sample number is morethan 70
                        elif sampleNum > 70:
                            cam.release()
                            cv2.destroyAllWindows()
                            sql = "INSERT INTO tb_users SET enrollment = %s, nama = %s, status = %s"
                            val = (str(Enrollment), str(Name), "registered")
                            koneksi.execute(sql, val)
                            koneksi.execute("UPDATE tb_take_image SET status ='0'")
                            mydb.commit()
                            ts = time.time()
                            Date = datetime.datetime.fromtimestamp(
                                ts).strftime('%Y-%m-%d')
                            Time = datetime.datetime.fromtimestamp(
                                ts).strftime('%H:%M:%S')
                            row = [Enrollment, Name, Date, Time]
                            with open(str(cur_dir)+'\\DataUser\\DataUser.csv', 'a+') as csvFile:
                                writer = csv.writer(csvFile, delimiter=',')
                                writer.writerow(row)
                                csvFile.close()
                            log("TAKE IMAGE | {}".format(Name))
                            retak()
                            break
                    cam.release()
                    cv2.destroyAllWindows()
                    self.remote()

                except FileExistsError:
                    info('Gagal','Input Data Gagal')
                '''
=========================================================================================================================================
                                        UPDATE INTERFACE JAM/WAKTU SAAT INI

=========================================================================================================================================
'''  
                
    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.label.configure(text=now)
        window.after(1000, self.update_clock)
        '''
=========================================================================================================================================
                                        MENYIMPAN DATA WAKTU PRESENSI KE DATABASE
                                KET:
                                    wm == waktu masuk
                                    wk == waktu keluar
=========================================================================================================================================
'''

    def simpan_waktu(self):
        database()
        dataWaktu()
        dari_wm     = en_dari_wm.get()
        sampai_wm   = en_sampai_wm.get()
        dari_wk     = en_dari_wk.get()
        sampai_wk   = en_sampai_wk.get() 
        try:
            if dari_wm == '':
                dari_wm     = waktu['dariwm']
            if sampai_wm == '':
                sampai_wm   = waktu['sampaiwm']
            if dari_wk == '':
                dari_wk = waktu['dariwk']
            if sampai_wk == '':
                sampai_wk   = waktu['sampaiwk']
            if dari_wm == '' and sampai_wm == '':
                dari_wm     = waktu['dariwm']
                sampai_wm   = waktu['sampaiwm']
            if dari_wk == '' and sampai_wk == '':
                dari_wk     = waktu['dariwk']
                sampai_wk   = waktu['sampaiwk']
        except Exception as err:
            log(err)
            info('GAGAL',err)
        try:    
            masuk   = "UPDATE tb_waktu_masuk SET dari = %s, sampai = %s WHERE id = 1"
            val     = (dari_wm, sampai_wm)
            koneksi.execute(masuk, val)
            
            keluar  = "UPDATE tb_waktu_keluar SET dari = %s, sampai = %s WHERE id = 1"
            values  = (dari_wk, sampai_wk)
            koneksi.execute(keluar, values)
            
            mydb.commit()
            info("Berhasil","Waktu Presensi Diperbaharui")
            log("Waktu Presensi Diperbaharui")
            self.halaman()
        except Exception as error:
            log(error)
            info("GAGAL","Input Data Gagal")
            '''
============================================================================================================================================
                                        MENGUPLOAD FOTO HASIL PRESENSI KE WEBSITE

============================================================================================================================================
'''

    def uploadImg(self,file):
        dbPengaturan()
        file = open(str(file), "rb")
        url  = dataPengaturan['server']
        upload = requests.post(url, files = {"file": file})
        if upload.ok:
            log("img uploaded")
            '''
===========================================================================================================================================
                                        MEMULAI PRESENSI 
                        [BEKERJA PADA FITUR REMOTE DAN TANPA FITUR REMOTE]
                                    KET:
                                        wm      == waktu masuk
                                        wk      == waktu keluar
                                        now     == waktu sekarang
                                        future  == waktu sekarang + 20

===========================================================================================================================================
'''

    def start(self,remote=False):
        dbPengaturan()
        #MENGAMBIL DATA WAKTU PRESENSI MASUK DAN KELUAR
        koneksi.execute("SELECT dari, sampai FROM tb_waktu_masuk")
        hasil_wm        = koneksi.fetchall()
        for data in hasil_wm:
            dari_wm     = int(data[0])
            sampai_wm   = int(data[1])

        koneksi.execute("SELECT dari, sampai FROM tb_waktu_keluar")
        hasil_wk        = koneksi.fetchall()
        for r in hasil_wk:
            dari_wk     = int(r[0])
            sampai_wk   = int(r[1])

        future          = time.time() + 20
        now             = int(time.strftime("%H%M%S"))
        masuk           = int(dari_wm)
        keluar          = int(dari_wk)
        
        global sub
        #MENENTUKAN APAKAH SAAT INI KATEGORI PRESENSI MASUK DAN MENENTUKAN TERLAMBAT ATAU TIDAK
        if now <= keluar and now >= masuk:
            sub = 'tb_presensi_masuk'
            jenis = 'clockin'
            if now >= dari_wm and now <= sampai_wm:
                ket = "hadir"
            elif now > sampai_wm:
                ket = "terlambat"
            else:
                ket = "error"
        #MENENTUKAN APAKAH SAAT INI KATEGORI PRESENSI MASUK DAN MENENTUKAN TERLAMBAT ATAU TIDAK
        elif now >= keluar and now >= masuk:
            sub = 'tb_presensi_keluar'
            jenis = 'clockout'
            if now >= dari_wk and now <= sampai_wk:
                ket = "hadir"
            elif now >= sampai_wk:
                ket = "terlambat"
            else:
                ket = "error"
        else:
            sub     = 'log'
            jenis   = 'log'
            ket     = "waktu error"
            retak()
            info("INFO","Absensi Belum Dimulai")
            log("Absensi belum dimulai")

        #JIKA WAKTU TIDAK ERROR MAKA PRESENSI DIMULAI
        if sub != 'log':
            log("Presensi dimulai")
            #mengenali setiap wajah user
            recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
            try:
                recognizer.read("TrainingImageLabel/Trainer.yml")
            except:
                info('Peringatan','Lakukan train terlebih dahulu')
                log("belum melakukan train image")

            harcascadePath  = "haarcascade_frontalface_default.xml"
            faceCascade     = cv2.CascadeClassifier(harcascadePath)
            #membaca data user pada file DataUser.csv
            df              = pd.read_csv("{}/DataUser/DataUser.csv".format(str(cur_dir)))
            #object memulai camera video
            cam             = cv2.VideoCapture(0)
            #font family
            font            = cv2.FONT_HERSHEY_SIMPLEX
            col_names       = ['Enrollment', 'Name', 'Date', 'Time']
            attendance      = pd.DataFrame(columns=col_names)
            print(attendance)
            print("Here")
            while 1:
                #resfresh koneksi database
                koneksiDB()
                db          = mysql.connector.connect(host="{}".format(dataDB['host']),user="{}".format(dataDB['user']),password="{}".format(dataDB['pw']),database="{}".format(dataDB['db']))
                connect     = db.cursor()
                #ambil data status pada tabel control
                connect.execute("SELECT start FROM tb_controls")
                result      = connect.fetchall()
                for data in result:
                    statusStart = int(data[0])
                #mengembailikan nilai bool (True/False)
                ret, im     = cam.read()
                gray        = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces       = faceCascade.detectMultiScale(gray, 1.2, 5)
                for (x, y, w, h) in faces:
                    global Id
                    
                    Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                    if (conf < 70):
                        print(conf)
                        global aa
                        global date
                        global timeStamp
                        ts          = time.time()
                        date        = datetime.datetime.fromtimestamp(
                            ts).strftime('%Y-%m-%d')
                        timeStamp   = datetime.datetime.fromtimestamp(
                            ts).strftime('%H:%M:%S')
                        aa          = df.loc[df['Enrollment'] == Id]['Name'].values
                        global tt
                        tt = aa + "-" + str(Id)
                        attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                        cv2.putText(im, str(tt), (x + h, y),
                                    font, 1, (255, 255, 0,), 4)
                        #cv2.putText(im, text='Suhu : '+'98', org=(30, 440),
                                    #fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0), thickness=2)
                        nama = "".join(filter(remove_special_characters, str(aa)))
                    else:
                        Id = 'Unknown'
                        tt = str(Id)
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                        cv2.putText(im, str(tt), (x + h, y),
                                    font, 1, (0, 25, 255), 4)
                    if conf >= 40:
                        if Id != 'Unknown':
                            timer       = time.time()
                            date        = time.strftime('%Y-%m-%d')
                            enrollment  = str(Id)
                            koneksi.execute("SELECT clockin FROM tb_presensi WHERE enrollment = '{}' AND tanggal = '{}'".format(str(Id),str(date)))
                            data1       = str(koneksi.fetchall())
                            koneksi.execute("SELECT clockout FROM tb_presensi WHERE enrollment = '{}' AND tanggal = '{}'".format(str(Id),str(date)))
                            data2       = str(koneksi.fetchall())
                            jamMasuk    = "".join(filter(remove_special_characters, str(data1)))
                            jamKeluar   = "".join(filter(remove_special_characters, str(data2)))
                            mydb.commit()
                            if timer > future:
                                print(Id)
                                nameForImg = "".join(a for a in nama if a.isalpha())
                                if jenis == "clockin":
                                    #insert data hasil presensi ke database
                                    try:
                                        clockin     = time.strftime("%H:%M:%S")
                                        tanggal     = "".join(filter(remove_special_characters,str(date)))
                                        dirImg      = "{}{}{}.jpg".format(str(nameForImg),str(tanggal),str(jenis))
                                        if ket == "hadir" and jamMasuk == "":
                                            foto        = "{}\\assets\\upload\\{}{}{}.jpg".format(str(cur_dir),str(nameForImg),str(tanggal),str(jenis))
                                            cv2.imwrite(foto,im)
                                            sql         = "INSERT INTO tb_presensi (enrollment,nama,tanggal,clockin, img_in) VALUES (%s,%s,%s,%s,%s)"
                                            val         = (str(Id), str(nama), str(date), str(clockin),str(dirImg))
                                            koneksi.execute(sql, val)
                                            mydb.commit()
                                            self.uploadImg(foto)
                                            log("presensi|{}|{}".format(Id,ket))

                                        elif ket == "terlambat" and jamMasuk == "":
                                            foto        = "{}\\assets\\upload\\{}{}{}.jpg".format(str(cur_dir),str(nameForImg),str(tanggal),str(jenis))
                                            cv2.imwrite(foto,im)
                                            sql         = "INSERT INTO tb_presensi (enrollment,nama,tanggal,clockin, img_in, c_in) VALUES (%s,%s,%s,%s,%s,%s)"
                                            val         = (str(Id), str(nama), str(date), str(clockin),str(dirImg),str(ket))
                                            koneksi.execute(sql, val)
                                            mydb.commit()
                                            self.uploadImg(foto)
                                            log("presensi|{}|{}".format(Id,ket))
                                        else:
                                            cv2.putText(im, text='Anda Sudah Absen', org=(30, 400), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0), thickness=2)
                                        timer = time.time()
                                        # time.sleep(6)
                                    except Exception as error:
                                        log('error')
                                        print(error)
                                        print("masuk")
                                elif jenis == "clockout":
                                    try:
                                        clockout    = time.strftime("%H:%M:%S")
                                        tanggal     = "".join(filter(remove_special_characters,str(date)))
                                        dirImg      = "{}{}{}.jpg".format(str(nameForImg),str(tanggal),str(jenis))
                                        if ket == "hadir" and jamKeluar == "":
                                            foto        = "{}\\assets\\upload\\{}{}{}.jpg".format(str(cur_dir),str(nameForImg),str(tanggal),str(jenis))
                                            sql         = "UPDATE tb_presensi SET clockout = %s, img_out = %s WHERE enrollment = %s AND tanggal = %s"
                                            val         = (str(clockout), str(dirImg), str(Id), str(date))
                                            koneksi.execute(sql, val)
                                            mydb.commit()
                                            log("presensi|{}".format(Id))
                                            print("clockout !hadir")
                                            cv2.imwrite(foto,im)
                                            self.uploadImg(foto)
                                            log("presensi|{}|{}".format(Id,ket))

                                        elif ket == "terlambat" and jamKeluar == "":
                                            foto        = "{}\\assets\\upload\\{}{}{}.jpg".format(str(cur_dir),str(nameForImg),str(tanggal),str(jenis))
                                            sql         = "UPDATE tb_presensi SET clockout = %s, c_out = %s, img_out = %s WHERE enrollment = %s AND tanggal = %s"
                                            val         = (str(clockout), str(ket), str(dirImg), str(Id), str(date))
                                            koneksi.execute(sql, val)
                                            mydb.commit()
                                            log("presensi|{}".format(Id))
                                            print("clockout !hadir")
                                            cv2.imwrite(foto,im)
                                            self.uploadImg(foto)
                                            log("presensi|{}|{}".format(Id,ket))
                                        else:
                                            cv2.putText(im, text='Anda Sudah Absen', org=(30, 400), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0), thickness=2)
                                        timer = time.time()
                                    except Exception as error:
                                        log("error")
                                        print(error)
                                        print("Keluar")

                                if ket == "waktu error":
                                    cv2.putText(im, text="Diluar jam presensi", org=(30, 440),
                                        fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0), thickness=2)
                                timer = time.time()
                attendance = attendance.drop_duplicates(['Enrollment'], keep='first')

                if(dataPengaturan['kamera']=='fullscreen'):
                    cv2.namedWindow('Start Recognition', cv2.WND_PROP_FULLSCREEN)
                    cv2.setWindowProperty('Start Recognition', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

                cv2.imshow('Start Recognition', im)
                key = cv2.waitKey(30) & 0xff
                #menutup camera menggunakan tombol esc
                if key == 27 :
                    retak()
                    cam.release()
                    cv2.destroyAllWindows()
                    return
                #menutup camera menggunakan tombol start di website [jika fitur remote aktif]
                elif remote == True and statusStart == 0:
                    retak()
                    cam.release()
                    cv2.destroyAllWindows()
                    self.remote()
            return
            '''
=========================================================================================================
                                            UNTUK MELAKUKAN TEST KAMERA

=========================================================================================================
'''
    def testCamera(self):
        dbPengaturan()
        try:
            if(dataPengaturan['kamera']=='fullscreen'):
                cv2.namedWindow('Test Camera', cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty('Test Camera', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            camera = cv2.VideoCapture(0)
            while True:
                test, camOpn = camera.read()
                cv2.imshow('Test Camera', camOpn)

                key = cv2.waitKey(1)
                if key == 27:
                    break
            camera.release()
            cv2.destroyAllWindows()
        except Exception as error:
            error(error)
            log(error)
            '''
=========================================================================================================
                                MENGAMBIL SAMPLE GAMBAR/FOTO 
                                    [BUKAN FITUR REMOTE]

=========================================================================================================
'''

    def take_img(self):
        dbPengaturan()
        database()
        Name = en_nama.get()
        Enrollment = en_id.get()
        jabatan = en_jabatan.get()
        alamat = en_alamat.get()

        if Name == '':
            info('Gagal','Nama tidak boleh kosong')
        elif Enrollment == '':
            info('Gagal','ID tidak boleh kosong')
        else:
            try:
                cam         = cv2.VideoCapture(0)
                detector    = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                sampleNum   = 0

                if(dataPengaturan['kamera']== 'fullscreen'):
                        cv2.namedWindow('Take Image', cv2.WND_PROP_FULLSCREEN)
                        cv2.setWindowProperty('Take Image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

                while (True):
                    ret, img = cam.read()
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = detector.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        # menghitung sample 
                        sampleNum = sampleNum + 1
                        # simpan gambar
                        cv2.imwrite(str(cur_dir)+"/TrainingImage/" + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg",
                                    gray[y:y + h, x:x + w])
                        cv2.imshow('Take Image', img)
                    # wait for 100 miliseconds
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    # break if the sample number is morethan 100
                    elif sampleNum > 70:
                        break
                cam.release()
                cv2.destroyAllWindows()
                ts = time.time()
                Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                row = [Enrollment, Name, Date, Time]
                with open(str(cur_dir)+'\\DataUser\\DataUser.csv', 'a+') as csvFile:
                    writer = csv.writer(csvFile, delimiter=',')
                    writer.writerow(row)
                    sql = "INSERT INTO tb_users (enrollment,nama, jabatan, alamat, status) VALUES (%s, %s, %s,%s,%s)"
                    val = (Enrollment, Name,jabatan, alamat, 'registered')
                    koneksi.execute(sql, val)                  
                    csvFile.close()
                info('Berhasil','Input Data Berhasil!')
                log("TAKE IMAGE|".format(str(Enrollment)))
            except FileExistsError:
                info('GAGAL','Input Data Gagal')
                log("Input data gagal")
                '''
=========================================================================================================
                                MENGUBAH SAMPLE GAMBAR MENJADI BINARY   

========================================================================================================
'''

    def training(self):
        database()
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        global detector
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        try:
            global faces, Id
            faces, Id = getImagesAndLabels("TrainingImage")
            log("TrainingImage")
        except Exception:
            error('ID::(ImagesNotFound) :: suggested -- Take the training images first or create "TrainingImage" folder, place the Images')
            log('ERROR', 'ID::(ImagesNotFound) :: suggested -- Take the training images first or create "TrainingImage" folder, place the Images')

        recognizer.train(faces, np.array(Id))
        try:
            recognizer.save("{}/TrainingImageLabel/Trainer.yml".format(str(cur_dir)))
            log("Proses Train Berhasil")
            messagebox.showinfo('Berhasil', 'Proses Train Berhasil')
            time.sleep(2)
        except Exception:
            info('Peringatan', 'Folder "TrainingImageLabel" tidak ditemukan')
            log('Peringatan', 'Folder "TrainingImageLabel" tidak ditemukan')
        koneksi.execute("UPDATE tb_controls SET train = '0'")
        koneksi.execute("UPDATE tb_take_image SET status ='0'")
        mydb.commit()
        '''
=========================================================================================================
                                            MENAMPILKAN DATA USERS TERDAFTAR

========================================================================================================
'''

    def lihat_data(self):
        database()
        log("Lihat data")

        koneksi = mydb.cursor()

        query = "SELECT enrollment, nama, jabatan, alamat, status FROM tb_users ORDER BY nama ASC"

        koneksi.execute(query)
        data = koneksi.fetchall()

        nama = []
        Id = []
        jabatan = []
        alamat = []
        status = []
        for r in data:
            nama.append(r[1])
            Id.append(r[0])
            jabatan.append(r[2])
            alamat.append(r[3])
            status.append(r[4])

        # Views

        window.geometry("1000x700")
        window.configure(bg="#ffffff")

        canvas = Canvas(
            window,
            bg = "#ffffff",
            height = 700,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        canvas.place(x = 0, y = 0)  

        y = 140
        noLabel = 1
        yLabel = 146
        for r in range(len(Id)):
            image = Image.open('Views/dataUser/background.png')
            photo = ImageTk.PhotoImage(image)

            bg = Label(image = photo)
            bg.image = photo
            bg.place(x=0, y=0)

            no = Label(window, text = "#", bg="#ffffff", font=('ArialRoundedMTBold', int(12)))
            no.place(x=30, y=77)

            IdL = Label(window, text = "ENROLLMENT", bg="#ffffff", font=('ArialRoundedMTBold', int(12)))
            IdL.place(x=100, y=77)

            namaL = Label(window, text = "NAMA", bg="#ffffff", font=('ArialRoundedMTBold', int(12)))
            namaL.place(x=370, y=77)

            jabatanL = Label(window, text = "JABATAN", bg="#ffffff", font=('ArialRoundedMTBold', int(12)))
            jabatanL.place(x=570, y=77)

            statusL = Label(window, text = "STATUS", bg="#ffffff", font=('ArialRoundedMTBold', int(12)))
            statusL.place(x=770, y=77)

            # img = Image.open('Views/dataUser/img0.png')
            # pht = ImageTk.PhotoImage(img)

            # bgTabel = Label(image=pht)
            # bgTabel.img = pht
            # bgTabel.place(x=3, y=y)

            no = Label(window, text = noLabel, bg="#ffffff", borderwidth=2,fg="black", font=('ArialRoundedMTBold', int(10)))
            no.place(x=30, y=yLabel)

            IdL = Label(window, text = Id[r], bg="#ffffff", borderwidth=2,fg="black", font=('ArialRoundedMTBold', int(10)))
            IdL.place(x=100, y=yLabel)

            namaL = Label(window, text = nama[r], bg="#ffffff", borderwidth=2,fg="black", font=('ArialRoundedMTBold', int(10)))
            namaL.place(x=370, y=yLabel)

            jabatanL = Label(window, text = jabatan[r], bg="#ffffff", borderwidth=2,fg="black", font=('ArialRoundedMTBold', int(10)))
            jabatanL.place(x=570, y=yLabel)

            statusL = Label(window, text = status[r], bg="#ffffff", borderwidth=2,fg="black", font=('ArialRoundedMTBold', int(10)))
            statusL.place(x=770, y=yLabel)


            y+=56
            yLabel+=30
            noLabel+=1
            



        window.resizable(False, True)
        window.mainloop()
        '''
=========================================================================================================
                                    INTERFACE PENGATURAN APLIKASI  

=========================================================================================================
'''

    def pengaturan(self):
        import tkinter as tk
        import tkinter.font as tkFont
        root = tk.Tk()
        #setting title
        root.title("Pengaturan")
        # icon_DA = PhotoImage(file='assets/img/bg-2.png')
        # root.tk.call('wm', 'iconphoto', root._w, icon_DA)
        #setting root size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        def pengaturanAkun():

            def simpanData():
                database()
                username    =  enUsername.get()
                password    =  enPassword.get()
                nama        =  enNama.get()
                jabatan     =  enJabatan.get()
                email       =  enEmail.get()

                if(username == '' or password == ''):
                    info('Peringatan','Form USERNAME dan PASSWORD tidak boleh kosong')
                else:
                    try:
                        pwd         = hashlib.md5(password.encode())
                        koneksi.execute("SELECT * FROM tb_admin WHERE username = '{}' AND password = '{}'".format(username,pwd.hexdigest()))
                        result      =  koneksi.fetchall()
                        for x in result:
                            Id          = x[0]
                            dbUsername  = x[1]
                            dbPassword  = x[2]
                            dbNama      = x[3]
                            dbJabatan   = x[4]
                            dbEmail     = x[5]
                    except:
                        error("DALAH")

                    if(dbUsername == '' or dbPassword == ''):
                        error('USERNAME ATAU PASSWORD SALAH')
                    else:       
                        if(username == ''):
                            username = dbUsername
                        if(nama == ''):
                            nama = dbNama
                        if(jabatan == ''):
                            jabatan = dbJabatan
                        if(email == ''):
                            email = dbEmail
                        pw    = hashlib.md5(password.encode())
                        try:
                            sql = "UPDATE tb_admin SET username = %s, password = %s,nama = %s, jabatan = %s, email = %s WHERE id = %s"
                            val = (str(username),str(pw.hexdigest()),str(nama),str(jabatan),str(email),str(Id))
                            koneksi.execute(sql,val)
                            mydb.commit()
                            info('Berhasil','Profil Diperbaharui')
                        except Exception as error:
                            print(error)

            def ubahPassword():

                def simpanPassword():
                    usernameLama    = enUsernameLama.get()
                    passwordLama    = enPasswordLama.get()
                    usernameBaru    = enUsernameBaru.get()
                    passwordBaru    = enPasswordBaru.get()

                    database()
                    try:
                        if (usernameLama == '' or usernameBaru == '' or passwordLama == '' or passwordBaru == ''):
                            info('Peringatan','Form Isian Wajib Diisi')
                        Id = 0
                        pwl     = hashlib.md5(passwordLama.encode()) # encode password lama ke md5
                        pwb     = hashlib.md5(passwordBaru.encode()) # encode password baru ke md5

                        koneksi.execute("SELECT * FROM tb_admin WHERE username = '{}' AND password = '{}'".format(usernameLama,pwl.hexdigest()))
                        result  = koneksi.fetchall()
                        for x in result:
                            Id = [0]

                        if (Id != 0):
                            sql     = "UPDATE tb_admin SET username = %s, password = %s WHERE username = %s AND password = %s"
                            data    = (str(usernameBaru),str(pwb.hexdigest()),str(usernameLama),str(pwl.hexdigest()))
                            koneksi.execute(sql,data)
                            mydb.commit()
                            info('Berhasil','Data Berhasil Diperbaharui')
                            log('Ubah Username Dan Password Berhasil')
                        else:
                            error('Username dan Password Salah')
                            log('Username dan Password Salah')

                    except Exception as error:
                        print("HOLA DISINI ERRORNYA")
                        log("terjadi error saat menyimpan data username password")
                        info('Peringatan','Gagal verifikasi username dan password')
                        
                garisBiru=tk.Label(root)
                garisBiru["bg"] = "#1e9fff"
                ft = tkFont.Font(family='Times',size=10)
                garisBiru["font"] = ft
                garisBiru["fg"] = "#333333"
                garisBiru["justify"] = "center"
                garisBiru["text"] = ""
                garisBiru.place(x=210,y=40,width=372,height=30)

                bgWhite=tk.Label(root)
                bgWhite["bg"] = "#ffffff"
                ft = tkFont.Font(family='Times',size=10)
                bgWhite["font"] = ft
                bgWhite["fg"] = "#333333"
                bgWhite["justify"] = "center"
                bgWhite["text"] = ""
                bgWhite.place(x=210,y=50,width=372,height=439)

                labelPengaturanAkun=tk.Label(root)
                labelPengaturanAkun["bg"] = "#ffffff"
                ft = tkFont.Font(family='Times',size=15)
                labelPengaturanAkun["font"] = ft
                labelPengaturanAkun["fg"] = "#333333"
                labelPengaturanAkun["justify"] = "left"
                labelPengaturanAkun["text"] = "Pengaturan Akun"
                labelPengaturanAkun.place(x=240,y=60,width=175,height=46)

                labelUsernameLama=tk.Label(root)
                labelUsernameLama["bg"] = "#ffffff"
                ft = tkFont.Font(family='Times',size=13)
                labelUsernameLama["font"] = ft
                labelUsernameLama["fg"] = "#333333"
                labelUsernameLama["justify"] = "left"
                labelUsernameLama["text"] = "Username lama"
                labelUsernameLama.place(x=210,y=140,width=128,height=42)

                enUsernameLama=tk.Entry(root)
                enUsernameLama["bg"] = "#ffffff"
                enUsernameLama["borderwidth"] = "1px"
                ft = tkFont.Font(family='Times',size=13)
                enUsernameLama["font"] = ft
                enUsernameLama["fg"] = "#333333"
                enUsernameLama["justify"] = "center"
                enUsernameLama["text"] = "Username lama"
                enUsernameLama.place(x=340,y=140,width=195,height=41)

                labelPasswordLama=tk.Label(root)
                labelPasswordLama["bg"] = "#ffffff"
                ft = tkFont.Font(family='Times',size=13)
                labelPasswordLama["font"] = ft
                labelPasswordLama["fg"] = "#333333"
                labelPasswordLama["justify"] = "left"
                labelPasswordLama["text"] = "Password lama"
                labelPasswordLama.place(x=210,y=210,width=133,height=34)

                enPasswordLama=tk.Entry(root)
                enPasswordLama["bg"] = "#ffffff"
                enPasswordLama["borderwidth"] = "1px"
                ft = tkFont.Font(family='Times',size=13)
                enPasswordLama["font"] = ft
                enPasswordLama["fg"] = "#333333"
                enPasswordLama["justify"] = "center"
                enPasswordLama["text"] = "Password lama"
                enPasswordLama.place(x=340,y=210,width=195,height=40)
                enPasswordLama["show"] = "*"

                labelUsernameBaru=tk.Label(root)
                labelUsernameBaru["bg"] = "#ffffff"
                ft = tkFont.Font(family='Times',size=13)
                labelUsernameBaru["font"] = ft
                labelUsernameBaru["fg"] = "#333333"
                labelUsernameBaru["justify"] = "left"
                labelUsernameBaru["text"] = "Username baru"
                labelUsernameBaru.place(x=210,y=280,width=128,height=42)

                enUsernameBaru=tk.Entry(root)
                enUsernameBaru["bg"] = "#ffffff"
                enUsernameBaru["borderwidth"] = "1px"
                ft = tkFont.Font(family='Times',size=13)
                enUsernameBaru["font"] = ft
                enUsernameBaru["fg"] = "#333333"
                enUsernameBaru["justify"] = "center"
                enUsernameBaru["text"] = "Username baru"
                enUsernameBaru.place(x=340,y=280,width=194,height=41)

                labelPasswordBaru=tk.Label(root)
                labelPasswordBaru["bg"] = "#ffffff"
                ft = tkFont.Font(family='Times',size=13)
                labelPasswordBaru["font"] = ft
                labelPasswordBaru["fg"] = "#333333"
                labelPasswordBaru["justify"] = "left"
                labelPasswordBaru["text"] = "Password Baru"
                labelPasswordBaru.place(x=210,y=350,width=133,height=34)

                enPasswordBaru=tk.Entry(root)
                enPasswordBaru["bg"] = "#ffffff"
                enPasswordBaru["borderwidth"] = "1px"
                ft = tkFont.Font(family='Times',size=13)
                enPasswordBaru["font"] = ft
                enPasswordBaru["fg"] = "#333333"
                enPasswordBaru["justify"] = "center"
                enPasswordBaru["text"] = "Password Baru"
                enPasswordBaru.place(x=340,y=350,width=195,height=40)
                enPasswordBaru["show"] = "*"

                btnSimpan=tk.Button(root)
                btnSimpan["activebackground"] = "#01aaed"
                btnSimpan["bg"] = "#1e9fff"
                ft = tkFont.Font(family='Times',size=13)
                btnSimpan["font"] = ft
                btnSimpan["fg"] = "#ffffff"
                btnSimpan["justify"] = "center"
                btnSimpan["text"] = "SIMPAN"
                btnSimpan["relief"] = "groove"
                btnSimpan.place(x=470,y=440,width=102,height=33)
                btnSimpan["command"] = simpanPassword

            garisBiru=tk.Label(root)
            garisBiru["bg"] = "#1e9fff"
            ft = tkFont.Font(family='Times',size=10)
            garisBiru["font"] = ft
            garisBiru["fg"] = "#333333"
            garisBiru["justify"] = "center"
            garisBiru["text"] = ""
            garisBiru.place(x=210,y=40,width=372,height=30)

            bgWhite=tk.Label(root)
            bgWhite["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=10)
            bgWhite["font"] = ft
            bgWhite["fg"] = "#333333"
            bgWhite["justify"] = "center"
            bgWhite["text"] = ""
            bgWhite.place(x=210,y=50,width=372,height=439)

            labelPengaturanAkun=tk.Label(root)
            labelPengaturanAkun["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=15)
            labelPengaturanAkun["font"] = ft
            labelPengaturanAkun["fg"] = "#333333"
            labelPengaturanAkun["justify"] = "left"
            labelPengaturanAkun["text"] = "Pengaturan Akun"
            labelPengaturanAkun.place(x=240,y=60,width=175,height=46)

            btnSimpan=tk.Button(root)
            btnSimpan["activebackground"] = "#01aaed"
            btnSimpan["bg"] = "#1e9fff"
            ft = tkFont.Font(family='Times',size=13)
            btnSimpan["font"] = ft
            btnSimpan["fg"] = "#ffffff"
            btnSimpan["justify"] = "center"
            btnSimpan["text"] = "Ubah Password"
            btnSimpan["relief"] = "ridge"
            btnSimpan.place(x=217,y=5,width=125,height=33)
            btnSimpan["command"] = ubahPassword

            labelNama=tk.Label(root)
            labelNama["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=13)
            labelNama["font"] = ft
            labelNama["fg"] = "#333333"
            labelNama["justify"] = "center"
            labelNama["text"] = "Nama"
            labelNama.place(x=210,y=140,width=130,height=41)

            enNama=tk.Entry(root)
            enNama["bg"] = "#ffffff"
            enNama["borderwidth"] = "1px"
            ft = tkFont.Font(family='Times',size=13)
            enNama["font"] = ft
            enNama["fg"] = "#333333"
            enNama["justify"] = "center"
            enNama["text"] = "nama"
            enNama.place(x=340,y=140,width=192,height=38)

            labelJabatan=tk.Label(root)
            labelJabatan["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=13)
            labelJabatan["font"] = ft
            labelJabatan["fg"] = "#333333"
            labelJabatan["justify"] = "center"
            labelJabatan["text"] = "Jabatan"
            labelJabatan.place(x=210,y=200,width=134,height=39)

            enJabatan=tk.Entry(root)
            enJabatan["bg"] = "#ffffff"
            enJabatan["borderwidth"] = "1px"
            ft = tkFont.Font(family='Times',size=13)
            enJabatan["font"] = ft
            enJabatan["fg"] = "#333333"
            enJabatan["justify"] = "center"
            enJabatan["text"] = "Jabatan"
            enJabatan.place(x=340,y=200,width=193,height=39)

            labelEmail=tk.Label(root)
            labelEmail["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=13)
            labelEmail["font"] = ft
            labelEmail["fg"] = "#333333"
            labelEmail["justify"] = "center"
            labelEmail["text"] = "Email"
            labelEmail.place(x=210,y=260,width=136,height=43)

            enEmail=tk.Entry(root)
            enEmail["bg"] = "#ffffff"
            enEmail["borderwidth"] = "1px"
            ft = tkFont.Font(family='Times',size=13)
            enEmail["font"] = ft
            enEmail["fg"] = "#333333"
            enEmail["justify"] = "center"
            enEmail["text"] = "Email"
            enEmail.place(x=340,y=260,width=195,height=39)

            labelPesan=tk.Label(root)
            labelPesan["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=13)
            labelPesan["font"] = ft
            labelPesan["fg"] = "#333333"
            labelPesan["justify"] = "center"
            labelPesan["text"] = "Verifikasi Username dan Password"
            labelPesan.place(x=210,y=300,width=300,height=42)

            labelUsername=tk.Label(root)
            labelUsername["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=13)
            labelUsername["font"] = ft
            labelUsername["fg"] = "#333333"
            labelUsername["justify"] = "center"
            labelUsername["text"] = "Username"
            labelUsername.place(x=210,y=330,width=128,height=42)

            enUsername=tk.Entry(root)
            enUsername["bg"] = "#ffffff"
            enUsername["borderwidth"] = "1px"
            ft = tkFont.Font(family='Times',size=13)
            enUsername["font"] = ft
            enUsername["fg"] = "#333333"
            enUsername["justify"] = "center"
            enUsername["text"] = "Username"
            enUsername.place(x=340,y=330,width=194,height=41)

            labelPassword=tk.Label(root)
            labelPassword["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=13)
            labelPassword["font"] = ft
            labelPassword["fg"] = "#333333"
            labelPassword["justify"] = "center"
            labelPassword["text"] = "Password"
            labelPassword.place(x=210,y=390,width=133,height=34)

            enPassword=tk.Entry(root)
            enPassword["bg"] = "#ffffff"
            enPassword["borderwidth"] = "1px"
            ft = tkFont.Font(family='Times',size=13)
            enPassword["font"] = ft
            enPassword["fg"] = "#333333"
            enPassword["justify"] = "center"
            enPassword["text"] = "Password"
            enPassword.place(x=340,y=390,width=195,height=40)
            enPassword["show"] = "*"

            btnSimpan=tk.Button(root)
            btnSimpan["activebackground"] = "#01aaed"
            btnSimpan["bg"] = "#1e9fff"
            ft = tkFont.Font(family='Times',size=13)
            btnSimpan["font"] = ft
            btnSimpan["fg"] = "#ffffff"
            btnSimpan["justify"] = "center"
            btnSimpan["text"] = "SIMPAN"
            btnSimpan["relief"] = "groove"
            btnSimpan.place(x=470,y=440,width=102,height=33)
            btnSimpan["command"] = simpanData

        def pengaturanDatabase():
            koneksiDB()
            def simpanDb():
                host = enHost.get()
                user = enUser.get()
                pw   = enPassword.get()
                db   = enDatabase.get()

                try:
                    with open('{}/config/database/database.csv'.format(cur_dir),mode='w') as file:
                        field = ['HOST','USER','PASSWORD','DATABASE']

                        writer = csv.DictWriter(file,fieldnames = field)

                        writer.writeheader()
                        writer.writerow({   'HOST': host,
                                            'USER': user,
                                            'PASSWORD': pw,
                                            'DATABASE': db})
                        info('Successfully','Database Diperbaharui!')
                        if(messagebox.askokcancel('INFORMASI','Restart aplikasi untuk menerapkan perubahan?')):
                            info('INFORMASI', 'Buka kembali setelah aplikasi tertutup!')
                            root.destroy()
                except:
                    error('Gagal menyimpan data')
            garisBiru=tk.Label(root)
            garisBiru["bg"] = "#1e9fff"
            ft = tkFont.Font(family='Times',size=10)
            garisBiru["font"] = ft
            garisBiru["fg"] = "#333333"
            garisBiru["justify"] = "center"
            garisBiru["text"] = ""
            garisBiru.place(x=210,y=40,width=372,height=30)

            bgWhite=tk.Label(root)
            bgWhite["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=10)
            bgWhite["font"] = ft
            bgWhite["fg"] = "#333333"
            bgWhite["justify"] = "center"
            bgWhite["text"] = ""
            bgWhite.place(x=210,y=50,width=372,height=439)

            labelPengaturanDatabase=tk.Label(root)
            labelPengaturanDatabase["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=15)
            labelPengaturanDatabase["font"] = ft
            labelPengaturanDatabase["fg"] = "#333333"
            labelPengaturanDatabase["justify"] = "left"
            labelPengaturanDatabase["text"] = "Pengaturan Database"
            labelPengaturanDatabase.place(x=240,y=60,width=175,height=46)

            labelHost=tk.Label(root)
            labelHost["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=13)
            labelHost["font"] = ft
            labelHost["fg"] = "#333333"
            labelHost["justify"] = "center"
            labelHost["text"] = "Host"
            labelHost.place(x=210,y=140,width=130,height=41)

            enHost=tk.Entry(root)
            enHost["bg"] = "#ffffff"
            enHost["borderwidth"] = "1px"
            ft = tkFont.Font(family='Times',size=13)
            enHost["font"] = ft
            enHost["fg"] = "#333333"
            enHost["justify"] = "center"
            enHost["text"] = "Host"
            enHost.place(x=340,y=140,width=192,height=38)
            enHost.insert(END,dataDB['host'])

            labelUser=tk.Label(root)
            labelUser["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=13)
            labelUser["font"] = ft
            labelUser["fg"] = "#333333"
            labelUser["justify"] = "center"
            labelUser["text"] = "User"
            labelUser.place(x=210,y=200,width=134,height=39)

            enUser=tk.Entry(root)
            enUser["bg"] = "#ffffff"
            enUser["borderwidth"] = "1px"
            ft = tkFont.Font(family='Times',size=13)
            enUser["font"] = ft
            enUser["fg"] = "#333333"
            enUser["justify"] = "center"
            enUser["text"] = "User"
            enUser.place(x=340,y=200,width=193,height=39)
            enUser.insert(END,dataDB['user'])

            labelPassword=tk.Label(root)
            labelPassword["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=13)
            labelPassword["font"] = ft
            labelPassword["fg"] = "#333333"
            labelPassword["justify"] = "center"
            labelPassword["text"] = "Password"
            labelPassword.place(x=210,y=260,width=136,height=43)

            enPassword=tk.Entry(root)
            enPassword["bg"] = "#ffffff"
            enPassword["borderwidth"] = "1px"
            ft = tkFont.Font(family='Times',size=13)
            enPassword["font"] = ft
            enPassword["fg"] = "#333333"
            enPassword["justify"] = "center"
            enPassword["text"] = "Password"
            enPassword["show"] = "*"
            enPassword.place(x=340,y=260,width=195,height=39)
            enPassword.insert(END,dataDB['pw'])

            labelDatabase=tk.Label(root)
            labelDatabase["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=13)
            labelDatabase["font"] = ft
            labelDatabase["fg"] = "#333333"
            labelDatabase["justify"] = "center"
            labelDatabase["text"] = "Database"
            labelDatabase.place(x=210,y=320,width=128,height=42)

            enDatabase=tk.Entry(root)
            enDatabase["bg"] = "#ffffff"
            enDatabase["borderwidth"] = "1px"
            ft = tkFont.Font(family='Times',size=13)
            enDatabase["font"] = ft
            enDatabase["fg"] = "#333333"
            enDatabase["justify"] = "center"
            enDatabase["text"] = "Database"
            enDatabase.place(x=340,y=320,width=194,height=41)
            enDatabase.insert(END,dataDB['db'])

            btnSimpan=tk.Button(root)
            btnSimpan["activebackground"] = "#01aaed"
            btnSimpan["bg"] = "#1e9fff"
            ft = tkFont.Font(family='Times',size=13)
            btnSimpan["font"] = ft
            btnSimpan["fg"] = "#ffffff"
            btnSimpan["justify"] = "center"
            btnSimpan["text"] = "SIMPAN"
            btnSimpan["relief"] = "groove"
            btnSimpan.place(x=470,y=440,width=102,height=33)
            btnSimpan["command"] = simpanDb

        def pengaturanServer():
            dbPengaturan()

            def simpanServer():
                server = enAlamatServer.get()
                field  = ['SERVER','KAMERA','HEADER']

                if(server==''):
                    info('Peringatan','Server wajib diisi')
                else:
                    try:
                        with open('{}/config/database/pengaturan.csv'.format(cur_dir),mode='w') as file:
                            writer = csv.DictWriter(file,fieldnames=field)

                            writer.writeheader()
                            writer.writerow({'SERVER':server,
                                            'KAMERA':dataPengaturan['kamera'],
                                            'HEADER': dataPengaturan['header']})
                        pengaturanServer()
                    except Exception as error:
                        info('Error',error)

            garisBiru=tk.Label(root)
            garisBiru["bg"] = "#1e9fff"
            ft = tkFont.Font(family='Times',size=10)
            garisBiru["font"] = ft
            garisBiru["fg"] = "#333333"
            garisBiru["justify"] = "center"
            garisBiru["text"] = ""
            garisBiru.place(x=210,y=40,width=372,height=30)

            bgWhite=tk.Label(root)
            bgWhite["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=10)
            bgWhite["font"] = ft
            bgWhite["fg"] = "#333333"
            bgWhite["justify"] = "center"
            bgWhite["text"] = ""
            bgWhite.place(x=210,y=50,width=372,height=439)

            labelPengaturanServer=tk.Label(root)
            labelPengaturanServer["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=15)
            labelPengaturanServer["font"] = ft
            labelPengaturanServer["fg"] = "#333333"
            labelPengaturanServer["justify"] = "left"
            labelPengaturanServer["text"] = "Pengaturan Server"
            labelPengaturanServer.place(x=240,y=60,width=175,height=46)

            labelAlamatServer=tk.Label(root)
            labelAlamatServer["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=13)
            labelAlamatServer["font"] = ft
            labelAlamatServer["fg"] = "#333333"
            labelAlamatServer["justify"] = "center"
            labelAlamatServer["text"] = "Alamat Server"
            labelAlamatServer.place(x=220,y=200,width=130,height=41)

            enAlamatServer=tk.Entry(root)
            enAlamatServer["bg"] = "#ffffff"
            enAlamatServer["borderwidth"] = "1px"
            ft = tkFont.Font(family='Times',size=13)
            enAlamatServer["font"] = ft
            enAlamatServer["fg"] = "#333333"
            enAlamatServer["justify"] = "left"
            enAlamatServer["text"] = "alamat server"
            enAlamatServer.place(x=360,y=200,width=192,height=38)
            enAlamatServer.insert(0,"http://")

            labelServerSaatIni=tk.Label(root)
            labelServerSaatIni["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=13)
            labelServerSaatIni["font"] = ft
            labelServerSaatIni["fg"] = "#333333"
            labelServerSaatIni["justify"] = "left"
            labelServerSaatIni["text"] = "Server saat ini"
            labelServerSaatIni.place(x=210,y=100,width=373,height=37)

            labelServer=tk.Label(root)
            labelServer["bg"] = "#00babd"
            ft = tkFont.Font(family='Times',size=13)
            labelServer["font"] = ft
            labelServer["fg"] = "#ffffff"
            labelServer["justify"] = "left"
            labelServer["text"] = dataPengaturan['server']
            labelServer.place(x=210,y=140,width=373,height=37)

            btn_simpan=tk.Button(root)
            btn_simpan["activebackground"] = "#01aaed"
            btn_simpan["bg"] = "#1e9fff"
            ft = tkFont.Font(family='Times',size=13)
            btn_simpan["font"] = ft
            btn_simpan["fg"] = "#ffffff"
            btn_simpan["justify"] = "center"
            btn_simpan["text"] = "SIMPAN"
            btn_simpan["relief"] = "groove"
            btn_simpan.place(x=450,y=270,width=102,height=33)
            btn_simpan["command"] = simpanServer

        def pengaturanHeader():
            dbPengaturan()
            def simpanHeader():
                header = enHeader.get()
                field  = ['SERVER','KAMERA','HEADER']

                def simpan():
                    try:
                        with open('{}/config/database/pengaturan.csv'.format(cur_dir),mode='w') as file:
                            writer = csv.DictWriter(file,fieldnames=field)

                            writer.writeheader()
                            writer.writerow({'SERVER':dataPengaturan['server'],
                                            'KAMERA':dataPengaturan['kamera'],
                                            'HEADER': header})
                        pengaturanHeader()
                    except Exception as error:
                        info('Error',error)

                if(header==''):
                    if(messagebox.askokcancel('PERINGATAN','APAKAH ANDA YAKIN INGIN MENGOSONGKAN HEADER?')):
                        simpan()
                else:
                    simpan()
                    
            garisBiru=tk.Label(root)
            garisBiru["bg"] = "#1e9fff"
            ft = tkFont.Font(family='Times',size=10)
            garisBiru["font"] = ft
            garisBiru["fg"] = "#333333"
            garisBiru["justify"] = "center"
            garisBiru["text"] = ""
            garisBiru.place(x=210,y=40,width=372,height=30)

            bgWhite=tk.Label(root)
            bgWhite["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=10)
            bgWhite["font"] = ft
            bgWhite["fg"] = "#333333"
            bgWhite["justify"] = "center"
            bgWhite["text"] = ""
            bgWhite.place(x=210,y=50,width=372,height=439)

            labelPengaturanHeader=tk.Label(root)
            labelPengaturanHeader["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=15)
            labelPengaturanHeader["font"] = ft
            labelPengaturanHeader["fg"] = "#333333"
            labelPengaturanHeader["justify"] = "left"
            labelPengaturanHeader["text"] = "Pengaturan Haeder Aplikasi"
            labelPengaturanHeader.place(x=240,y=60,width=300,height=46)

            labelHeader=tk.Label(root)
            labelHeader["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=13)
            labelHeader["font"] = ft
            labelHeader["fg"] = "#333333"
            labelHeader["justify"] = "center"
            labelHeader["text"] = "Header"
            labelHeader.place(x=220,y=200,width=130,height=41)

            enHeader=tk.Entry(root)
            enHeader["bg"] = "#ffffff"
            enHeader["borderwidth"] = "1px"
            ft = tkFont.Font(family='Times',size=13)
            enHeader["font"] = ft
            enHeader["fg"] = "#333333"
            enHeader["justify"] = "center"
            enHeader["text"] = "Header"
            enHeader.place(x=360,y=200,width=192,height=38)

            labelHeaderSaatIni=tk.Label(root)
            labelHeaderSaatIni["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=13)
            labelHeaderSaatIni["font"] = ft
            labelHeaderSaatIni["fg"] = "#333333"
            labelHeaderSaatIni["justify"] = "left"
            labelHeaderSaatIni["text"] = "Header saat ini"
            labelHeaderSaatIni.place(x=210,y=100,width=373,height=37)

            labelHeader=tk.Label(root)
            labelHeader["bg"] = "#1e9fff"
            ft = tkFont.Font(family='Times',size=13)
            labelHeader["font"] = ft
            labelHeader["fg"] = "#ffffff"
            labelHeader["justify"] = "left"
            labelHeader["text"] = dataPengaturan['header']
            labelHeader.place(x=210,y=140,width=373,height=37)

            btn_simpan=tk.Button(root)
            btn_simpan["activebackground"] = "#01aaed"
            btn_simpan["bg"] = "#1e9fff"
            ft = tkFont.Font(family='Times',size=13)
            btn_simpan["font"] = ft
            btn_simpan["fg"] = "#ffffff"
            btn_simpan["justify"] = "center"
            btn_simpan["text"] = "SIMPAN"
            btn_simpan["relief"] = "groove"
            btn_simpan.place(x=450,y=270,width=102,height=33)
            btn_simpan["command"] = simpanHeader


        def pengaturanKamera():
            dbPengaturan()
            def simpanKamera():
                sw = screenwidth.get()
                print(sw)

                field  = ['SERVER','KAMERA','HEADER']

                if(str(sw) == ''):
                    info('Peringatan','Form wajib diisi')
                else:
                    try:
                        with open('{}/config/database/pengaturan.csv'.format(cur_dir),mode='w') as file:
                            writer = csv.DictWriter(file,fieldnames=field)

                            writer.writeheader()
                            writer.writerow({'SERVER':dataPengaturan['server'],
                                            'KAMERA':sw,
                                            'HEADER': dataPengaturan['header']})
                        pengaturanKamera()
                    except Exception as error:
                        info('Error',error)
            garisBiru=tk.Label(root)
            garisBiru["bg"] = "#1e9fff"
            ft = tkFont.Font(family='Times',size=10)
            garisBiru["font"] = ft
            garisBiru["fg"] = "#333333"
            garisBiru["justify"] = "center"
            garisBiru["text"] = ""
            garisBiru.place(x=210,y=40,width=372,height=30)

            bgWhite=tk.Label(root)
            bgWhite["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=10)
            bgWhite["font"] = ft
            bgWhite["fg"] = "#333333"
            bgWhite["justify"] = "center"
            bgWhite["text"] = ""
            bgWhite.place(x=210,y=50,width=372,height=439)

            labelPengaturanKamera=tk.Label(root)
            labelPengaturanKamera["bg"] = "#ffffff"
            ft = tkFont.Font(family='Times',size=15)
            labelPengaturanKamera["font"] = ft
            labelPengaturanKamera["fg"] = "#333333"
            labelPengaturanKamera["justify"] = "left"
            labelPengaturanKamera["text"] = "Pengaturan Kamera"
            labelPengaturanKamera.place(x=240,y=60,width=175,height=60)

            FrameScreenWidht = LabelFrame(root, text="Screen Width",width=280,height=80,bg="#ffffff")
            FrameScreenWidht.place(x=240,y=170,width=280,height=100)

            screenwidth    = StringVar(root)

            rad1 = Radiobutton(root, text="Fullscreen", variable=screenwidth, value="fullscreen",command=simpanKamera,bg="#ffffff")
            rad1.place(x=247,y=190,width=160,height=46 )
            rad2 =Radiobutton(root, text="Default", variable=screenwidth, value="default",command=simpanKamera,bg="#ffffff")
            screenwidth.set(str(dataPengaturan['kamera']))
            rad2.place(x=370,y=190,width=120,height=46 )
        sidebarBiru=tk.Label(root)
        sidebarBiru["bg"] = "#1e9fff"
        ft = tkFont.Font(family='Times',size=22)
        sidebarBiru["font"] = ft
        sidebarBiru["fg"] = "#ffffff"
        sidebarBiru["justify"] = "center"
        sidebarBiru["text"] = ""
        sidebarBiru.place(x=0,y=0,width=194,height=492)

        labelPengaturan=tk.Label(root)
        labelPengaturan["bg"] = "#1e9fff"
        ft = tkFont.Font(family='Times',size=14)
        labelPengaturan["font"] = ft
        labelPengaturan["fg"] = "#ffffff"
        labelPengaturan["justify"] = "right"
        labelPengaturan["text"] = "PENGATURAN"
        labelPengaturan.place(x=10,y=0,width=160,height=49)

        btnAkun=tk.Button(root)
        btnAkun["activebackground"] = "#64b6f4"
        btnAkun["bg"] = "#1e9fff"
        ft = tkFont.Font(family='Times',size=13)
        btnAkun["font"] = ft
        btnAkun["fg"] = "#ffffff"
        btnAkun["justify"] = "center"
        btnAkun["text"] = "Akun"
        btnAkun["relief"] = "flat"
        btnAkun.place(x=0,y=70,width=192,height=42)
        btnAkun["command"] = pengaturanAkun

        btnPengaturanServer=tk.Button(root)
        btnPengaturanServer["activebackground"] = "#64b6f4"
        btnPengaturanServer["bg"] = "#1e9fff"
        ft = tkFont.Font(family='Times',size=13)
        btnPengaturanServer["font"] = ft
        btnPengaturanServer["fg"] = "#ffffff"
        btnPengaturanServer["justify"] = "center"
        btnPengaturanServer["text"] = "Server"
        btnPengaturanServer["relief"] = "flat"
        btnPengaturanServer.place(x=0,y=120,width=193,height=38)
        btnPengaturanServer["command"] = pengaturanServer

        btnDatabase=tk.Button(root)
        btnDatabase["activebackground"] = "#64b6f4"
        btnDatabase["bg"] = "#1e9fff"
        ft = tkFont.Font(family='Times',size=13)
        btnDatabase["font"] = ft
        btnDatabase["fg"] = "#ffffff"
        btnDatabase["justify"] = "center"
        btnDatabase["text"] = "Database"
        btnDatabase["relief"] = "flat"
        btnDatabase.place(x=0,y=170,width=193,height=40)
        btnDatabase["command"] = pengaturanDatabase

        btnKamera=tk.Button(root)
        btnKamera["activebackground"] = "#64b6f4"
        btnKamera["bg"] = "#1e9fff"
        ft = tkFont.Font(family='Times',size=13)
        btnKamera["font"] = ft
        btnKamera["fg"] = "#ffffff"
        btnKamera["justify"] = "center"
        btnKamera["text"] = "Kamera"
        btnKamera["relief"] = "flat"
        btnKamera.place(x=0,y=220,width=193,height=39)
        btnKamera["command"] = pengaturanKamera

        btnHeader=tk.Button(root)
        btnHeader["activebackground"] = "#64b6f4"
        btnHeader["bg"] = "#1e9fff"
        ft = tkFont.Font(family='Times',size=13)
        btnHeader["font"] = ft
        btnHeader["fg"] = "#ffffff"
        btnHeader["justify"] = "center"
        btnHeader["text"] = "Header"
        btnHeader["relief"] = "flat"
        btnHeader.place(x=0,y=270,width=193,height=39)
        btnHeader["command"] = pengaturanHeader

        pengaturanAkun()

        root.mainloop()

database()
app = App(window)
window.mainloop()
