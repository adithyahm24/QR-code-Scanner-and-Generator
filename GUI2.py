import time
from tkinter import *
from tkinter import filedialog,ttk

from pyzbar.pyzbar import decode
from PIL import Image
import cv2
import numpy as np
import qrcode


class QR(Tk):
    def __init__(self):
        super().__init__()

        self.cam = 0

        self.f = Frame(self)
        
        self.f.pack()
        self.config(background="#01F3B3")
        self.f.config(background="#01F3B3")
        t = Label(self.f, text="QR CODE SCANNER", background='#F3D601')
        t.config(font=("Arial", 40, 'bold'))

        t.grid(row=0, column=0, rowspan=1, columnspan=3)
        self.camf = Frame(self.f)
        self.camf.config(background="#01F3B3")
        self.camf.grid(row=1, column=0)
        self.t = Entry(self.f, width=25)
        Label(self.camf, text='', bg='#01F3B3').grid(row=1, column=0)
        self.val = IntVar(self, value=1)
        self.r2 = Radiobutton(self.camf, text="Primary Camera", value=1, variable=self.val, command=self.PRI_SCAN)
        self.r2.grid(row=3, column=1)
        self.r1 = Radiobutton(self.camf, text="URL", value=0, variable=self.val, command=self.URL)
        self.r1.grid(row=3, column=0)

        self.b1 = Button(self.camf,
                         text="Open",

                         command=self.SCAN,
                         bg='#FE831D')
        self.eL = Label(self.camf, text='', bg='#01F3B3')
        self.eL.grid(row=4, column=0)

        self.b1.grid(row=5, column=0, columnspan=2)

        Label(self.camf, text='Open Camera', bg='#01F3B3', font='times 15').grid(row=2, column=0, columnspan=2)
        Label(self.camf, text='', bg='#01F3B3', ).grid(row=8, column=0)
        self.openf = Frame(self.f)
        self.openf.config(background="#01F3B3")
        self.openf.grid(row=1, column=1, columnspan=2)

        Label(self.openf, text='Select a file', bg='#01F3B3', font='times 15').grid(row=9, column=0)
        b1 = Button(self.openf,
                    text=" Import from a file ",
                    command=self.con,
                    bg='#FE831D')
        b1.grid(row=9, column=1)
        Label(self.openf, text=' ', bg='#01F3B3').grid(row=12, column=0)
        self.cur = IntVar()
        self.text = Entry(self.camf, )
        self.cb = Checkbutton(self.f, text='Create a QR CODE', variable=self.cur, offvalue=False, onvalue=True,
                              command=self.checkbox)
        self.cb.grid(row=4, column=0, )
        Label(self.f, text='', bg='#01F3B3').grid(row=5, column=0)

        self.data = Text(self.f, height=3, width=50)
        Label(self.f, text='', bg='#01F3B3').grid(row=11, column=0)
        self.crb = Button(self.f,
                          text="Create",
                          command=self.create,
                          bg='#FE831D')

    def con(self):
        self.img = filedialog.askopenfilename(initialdir='/', title='Select a Image', filetype=[(
            'Image', ('*.jpg', '*.png'))])
        d = decode(Image.open(self.img))
        if d:
            t = Text(self.f, width=50, height=5)
            t.insert(1.0, "\n" + d[0].data.decode('utf-8'))
            t.grid(row=10, column=0, columnspan=2,padx=20)

    def SCAN(self):
        if self.text.get() != '':
            self.cam = self.text.get()

        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)
        true = True

        while true:
            _, img = cap.read()
            for bar in decode(img):
                data = bar.data.decode('utf-8')
                if data:
                    pts = np.array([bar.polygon], np.int32)
                    pts = pts.reshape((-1, 1, 2))
                    cv2.polylines(img, [pts], True, (255, 0, 255), 5)
                    cv2.putText(img, data, (bar.rect[0], bar.rect[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                0.9, (255, 0, 255), 2)

                    cv2.destroyAllWindows()
                    cv2.destroyWindow('Result')

                    t = Text(self.f, width=75, height=10)
                    t.insert(1.0, "\n" + data)
                    t.grid(row=10, column=0, columnspan=2)
                    true = False
                    break

            cv2.putText(img, "Press 'Esc' to exit", (20, 20), cv2.FONT_HERSHEY_SIMPLEX,
                        0.4, (0, 0, 255), 1)
            cv2.imshow('Result', img)
            if cv2.waitKey(1) == 27:
                cv2.destroyAllWindows()
                cv2.destroyWindow('Result')
                break

    def PRI_SCAN(self):
        self.eL.config(text='')
        self.text.grid_remove()
        self.cam = 0

    def URL(self):
        self.eL.config(text='URL: ')

        self.text.grid(row=4, column=1)

    def create(self):
        if self.data.get(1.0, END) != '':
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(self.data.get(1.0, END))
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            name = int(round(time.time() * 1000))
            name = f'{name}.png'
            img.save(name)

            l = Label(self.f, text=f'Created - {name}', bg='#01F3B3')
            l.grid(row=10, column=0)
            self.data.delete(1.0,END)
        else:
            pass

    def checkbox(self):
        if self.cur.get():
            self.data.grid(row=6, column=0, columnspan=3)
            self.crb.grid(row=9, column=0)
        else:
            self.data.grid_remove()
            self.crb.grid_remove()


QR().mainloop()
