from pymysql import *
from tkinter import *
from pygame import *
from PIL import Image,ImageTk

con = connect(user='root',passwd='root',host='localhost',db='snake')
cur = con.cursor()

def c_account():
    global warn
    if len(user_entry.get()) < 5 or len(user_entry.get()) > 20:
        warn.config(text='Range of username is from 5 to 20 words only')
        user_entry.config(fg='red')
        return

    elif len(passwd_entry.get()) < 5 or len(passwd_entry.get()) > 20:
        warn.config(text='Range of password is from 5 to 20 words only')
        passwd_entry.config(fg='red')
        return

    else:
        try:
            i = cur.execute("insert into account (username,password) values('%s','%s')"%(user_entry.get(),passwd_entry.get()))
            if i == 1:
                user_entry.config(fg='green')
                passwd_entry.config(fg='green')
                warn.config(text='Account Created',fg='blue')
                con.commit()

        except Exception as e:
            warn.config(text=e)

def log_in():
    global warn
    if len(user_entry.get()) < 5 or len(user_entry.get()) > 20:
        warn.config(text='Range of username is from 5 to 20 words only')
        user_entry.config(fg='red')
        return

    elif len(passwd_entry.get()) < 5 or len(passwd_entry.get()) > 20:
        warn.config(text='Range of password is from 5 to 20 words only')
        passwd_entry.config(fg='red')
        return

    else:
        i = cur.execute("select username from account where username='%s'"%(user_entry.get()))
        user_entry.config(fg='red')
        warn.config(text='Username doesnt exist')
        if i == 1:
            try:
                j = cur.execute("select password from account where username='%s' and password='%s'"%(user_entry.get(),passwd_entry.get()))
                warn.config(text='Password does not exist')
                passwd_entry.config(fg='red')
                if j == 1:
                    warn.config(text='reached here')
                    root.destroy()
                    import main_snake

                    mixer.init()
                    mixer.music.load('music/Sands of Mystery.mp3')
                    mixer.music.play()

                    s = main_snake.snake()


            except Exception as e:
                warn.config(text=e)
                print(e)
                

root = Tk()
root.title('LOGIN PAGE')
root.geometry('1000x500')
root.resizable(0,0)

img = Image.open('bg img/snake.png')
img = img.resize((1000,500),Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)
Label(root, image=img).place(x=0,y=0,relwidth=1,relheight=1)

f = Frame(root,width=500,height=335)
f.place(x=100,y=70)

title = Label(f,text='LOGIN HERE',font='impact 35 bold',fg='#006600')
title.place(x=100,y=15)

desc = Label(f,text='Login for Snake Game',font=('goudy old style',17),fg='#008000')
desc.place(x=100,y=85)

username = StringVar()
password = StringVar()

user = Label(f,text='Username:',font=('goudy old style',15),fg='#003300')
user.place(x=100,y=135) 

user_entry = Entry(f,textvariable=username,fg='green',bg='light grey',justify="center",font='algerian 13')
user_entry.place(x=100,y=165)

passwd = Label(f,text='Password:',font=('goudy old style',15),fg='#003300')
passwd.place(x=100,y=205)

passwd_entry = Entry(f,textvariable=password,show='*',fg='green',bg='light grey',justify='center',font='algerian 13')
passwd_entry.place(x=100,y=235)

submit = Button(root,text='LOG-IN',command=log_in,cursor='hand2',fg='white',bg='#006600')
submit.place(x=190,y=385,width=150)

c_acc = Button(root,text='CREATE ACCOUNT',command=c_account,cursor='hand2',fg='white',bg='#006600')
c_acc.place(x=380,y=385,width=150)

status_bar = Frame(root)
status_bar.pack(fill='x',side='bottom')

warn = Label(status_bar,text=None,fg='red')
warn.pack(anchor='nw')

root.mainloop()
