from tkinter import *
import random
from PIL import ImageTk, Image

screen = Tk()
screen.title("Key Code Generator")
screen.geometry('600x400')
screen.configure(background ="bisque")
photo = ImageTk.PhotoImage(Image.open("logo.jpeg"))
screen.iconphoto(False,photo)


def gen():
    global key
    if not (str(il.get()).isspace() or il.get()==""):
        k = ""
        variables='''ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()-_=+{}[]|\:;"'<>,./?`~'''
        code = il.get()
        code.strip()
        random.seed(code)
        for _ in range(8):
            k+=random.choice(variables)

        key.set(k)



key=StringVar('')
t1=Label(screen,text='Key Code Generator',font=('Arial',25),fg='red',background ="bisque")
t1.place(x=140,y=0)


t2=Label(screen,text='Code: ',font=('Arial',14),background ="bisque")
t2.place(x=145,y=90)

il=Entry(screen,font=('Arial',14),width=15)
il.place(x=240,y=90)

t3=Label(screen,text='Key: ',font=('Arial',14),background ="bisque")
t3.place(x=145,y=130)

c1=Entry(screen,font=('Arial',14),width=15,textvariable=key)
c1.place(x=240,y=130)

b=Button(screen,text='Generate',font=('Arial',14),fg='red',background ="white",command=gen)
b.place(x=240,y=180)


screen.mainloop()