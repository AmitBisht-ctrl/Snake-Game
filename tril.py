from tkinter import *
from PIL import Image,ImageTk
import turtle

root = Tk()
root.state('zoomed')



width = root.winfo_screenwidth()
height = root.winfo_screenheight()

img1 = 'bg img/desert.jpg'
img = PhotoImage(file='bg img/m.png')

desert = Image.open(img1)
desert = desert.resize((width,height),Image.ANTIALIAS)
resize_desert = ImageTk.PhotoImage(desert)

def printl(s):
    can.create_image(0,0,image=resize_desert,anchor='nw')

can = Canvas(root)
can.pack(fill='both',expand=True)
can.create_image(0,0,image=img,anchor='nw')
can.create_text(100,100,text='heello world')

B1 = Button(can,text='cliked')
b1_window = can.create_window(300,300,anchor='nw',window=B1)

f = Frame(can,width=100,height=30,bg='red')
f.pack(fill='x')

Button(f,text='broken',command=lambda:printl('amit')).pack(side='left',anchor='ne')

canvas = Canvas(can,width=700,height=700)
canvas.pack()


# def snake_screen():
#         # turtle screen
#         turt_screen = turtle.TurtleScreen(can)
#         turt_screen.bgcolor('#fff5e6')

#         # snake head
#         head = turtle.RawTurtle(turt_screen)
#         head.ht()
#         head.shape('square')
#         head.color('#804d00')
#         head.penup()
#         head.direction = 'stop'
#         head._tracer(0)
#         return turt_screen
# ts= snake_screen()

# while True:
#     # can.create_image(0,0,image=resize_desert,anchor='nw')
#     ts.update()


root.mainloop()
