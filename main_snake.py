import tkinter as tk
import turtle
from PIL import ImageTk 
from PIL import Image
from pygame import mixer
from pymysql import *
import time
import random
from second_snake import *

class snake(tk.Tk):
    
    def __init__(self):
        super().__init__()

        self.snake_no = 1
        self.snake_id = 0

        self.snake_size = 1
        self.sec_snake_size = 1
        self.speed = 20
        self.sec_snake_speed = 20
        self.delay = 0.1

        self.p1_score = 0
        self.p2_score = 0
        self.m_highscore = 0
        self.score = 0
        self.high_score = 0
        
        self.img1 = 'bg img/desert.jpg'
        self.img2 = 'bg img/sun.jpg'
        self.im = [self.img1,self.img2]
        self.colors = ['#fff0d2','#cce6ff']
        
        self.segments = []
        self.segments2 = []

        self.a = 0
        self.b = 0
        self.count = 1

        # connects db
        self.con = connect(db='snake',user='root',passwd='root',host='localhost')
        self.cur = self.con.cursor()

        self.can = tk.Canvas(self)
        self.can.pack(fill='both',expand=True)

        def band(self):
            self.destroy()

        self.title('Snake Game')
        self.state('zoomed')

        # defines closing functions
        self.screen_closing()

        # sets up bg image in main screen and initialise the snake head
        self.img_setup(self.img1)

        self.button_exit = tk.Button(self.can,text='EXIT',command=lambda: band(self),bg='#fff0d2')
        # button_exit.pack(side='right',anchor='ne',padx=50)
        self.can.create_window(self.width-150,10,anchor='ne',window=self.button_exit)

        # sets the turtle screen on main screen
        self.snake_screen()

        self.move2,self.h2 = sec_snake(self.turt_screen)

        self.single_player()       
        self.multi_player() 
        self.foods()
        self.write_score()
        self.bring_high_score()

        # loads the previous game
        self.load_single()
        self.load_multi()
        
        # creates save button and connects db
        self.save()

        self.key_binds()

        # main loop of the snake
        self.loop()

    def load_multi(self):
        def load_m(self):
            for sgmnt in self.segments:
                sgmnt.goto(1000,1000)
            self.segments.clear()

            for sgmnt in self.segments2:
                sgmnt.goto(1000,1000)
            self.segments2.clear()

            i = self.cur.execute("select * from multi_snakes")
            if i == 1:
                self.snake_no = 2
                values = self.cur.fetchone()

                h_x = values[1].split(',')[0]
                h_y = values[1].split(',')[1]
                self.head.goto(float(h_x),float(h_y))
                self.head.direction = 'stop'

                f_x = values[2].split(',')[0]
                f_y = values[2].split(',')[1]
                self.food.goto(float(f_x),float(f_y))

                h2_x = values[3].split(',')[0]
                h2_y = values[3].split(',')[1]
                self.h2.goto(float(h2_x),float(h2_y))
                self.h2.direction = 'stop'

                nos = values[4].split(',')[0]
                nos2 = values[4].split(',')[1]

                for y in range(int(nos)):
                    self.create_segments(1)

                for y in range(int(nos2)):
                    self.create_segments(2)

                self.p1_score = int(values[5].split(',')[0])
                self.p2_score = int(values[5].split(',')[1])

                self.food.st()
                self.head.st()
                self.h2.st()

                self.pen.clear()
                self.pen.write(f'P1-Score:{self.p1_score}  P2-Score:{self.p2_score}  High Score: {self.m_highscore}', align='center', font=('Courier', 20, 'normal'))

        self.button_load_m = tk.Button(self.can,text='LOAD MULTIPLAYER',command=lambda: load_m(self),bg='#ffd699')
        self.can.create_window(415,10,anchor='nw',window=self.button_load_m)

    def multi_player(self):
        def multi_p(self):
            self.snake_no = 2
            self.h2.goto(100,0)
            self.head.direction = 'stop'
            self.h2.direction = 'stop'
            self.p1_score = 0
            self.p2_score = 0
            self.head.goto(-100,0)
            self.h2.st()
            self.head.st()
            self.food.st()
            self.pen.clear()
            for sgmnt in self.segments:
                sgmnt.goto(1000,1000)
            self.segments.clear()

            for sgmnt in self.segments2:
                sgmnt.goto(1000,1000)
            self.segments2.clear()

            self.pen.clear()
            self.pen.write(f'P1-Score:{self.p1_score}  P2-Score:{self.p2_score}  High Score: {self.m_highscore}', align='center', font=('Courier', 20, 'normal'))

        self.button_mp = tk.Button(self.can,text='MULTI-PLAYER',command=lambda: multi_p(self),bg='#ffd699')
        # button_mp.pack(side='left',anchor='ne',padx=20)
        self.can.create_window(150,10,anchor='nw',window=self.button_mp)

    def loop(self):
        while True:
            self.turt_screen.update()
            self.turt_screen.delay(0)

            # snake out of bound/ death
            if self.head.xcor() > 340 or self.head.xcor() < -340 or self.head.ycor() > 340 or self.head.ycor() < -340 or self.h2.xcor() > 340 or self.h2.xcor() < -340 or self.h2.ycor() > 340 or self.h2.ycor() < -340:
                self.death()


            # snake eats food/ head collides food
            if self.head.distance(self.food) < 20:
                self.a += 1         

                x = random.randint(-340, 340)
                y = random.randint(-340, 340)
                self.food.goto(x, y)

                self.snake_id = 1
                
                # new segment for snake 
                self.create_segments(self.snake_id)

                self.snake_size += 0.01
                for segment in self.segments:
                    segment.shapesize(self.snake_size)
                self.head.shapesize(self.snake_size)
                self.speed += 0.1
                self.delay -= 0.001

                # set score
                if self.snake_no == 1:
                    self.score += 10
                    if self.score > self.high_score:
                        self.high_score = self.score

                    self.pen.clear()
                    self.pen.write(f'Score:{self.score} High Score: {self.high_score}', align='center', font=('Courier', 24, 'normal'))
                
                if self.snake_no == 2:
                    self.p1_score += 10
                    if self.p1_score > self.m_highscore :
                        self.m_highscore = self.p1_score  
                    
                    self.pen.clear()
                    self.pen.write(f'P1-Score:{self.p1_score}  P2-Score:{self.p2_score}  High Score: {self.m_highscore}', align='center', font=('Courier', 20, 'normal'))

            # second head collision
            if self.snake_no == 2:
                if self.h2.distance(self.food) < 20:    
                    self.b += 1      

                    x = random.randint(-340, 340)
                    y = random.randint(-340, 340)
                    self.food.goto(x, y)

                    self.snake_id = 2
                    
                    # new segment for snake 
                    self.create_segments(self.snake_id)

                    self.sec_snake_size += 0.01
                    self.h2.shapesize(self.sec_snake_size)
                    for segment in self.segments2:
                        segment.shapesize(self.sec_snake_size)
                    self.h2.shapesize(self.sec_snake_size) 
                    self.speed += 0.1
                    self.delay -= 0.001

                    # set score
                    self.p2_score += 10

                    if self.p2_score > self.m_highscore:
                        self.m_highscore = self.p2_score
                    
                    self.pen.clear()
                    self.pen.write(f'P1-Score:{self.p1_score}  P2-Score:{self.p2_score}  High Score: {self.m_highscore}', align='center', font=('Courier', 20, 'normal'))

            self.segments_setup(self.segments)
            self.segments_setup(self.segments2)
            
            if len(self.segments2) > 0:
                self.segments2[0].goto(self.h2.xcor(),self.h2.ycor())
                self.segments2[0].st()

            if len(self.segments) > 0:
                self.segments[0].goto(self.head.xcor(), self.head.ycor())
                self.segments[0].st()

            self.move()
            if self.snake_no == 2:
                self.move2(self.sec_snake_speed,self.snake_no)
                if self.h2.direction != 'stop':
                    self.self_collision(self.segments2,self.h2)  
                    if len(self.segments2) > 0:
                        for sgmnt in self.segments2:
                            sgmnt.st()

            if self.head.direction != 'stop':
                if len(self.segments) > 0:
                    if not self.new_segment.isvisible():
                        for sgmnt in self.segments:
                            sgmnt.st()
                        
        
                # collision check
                self.self_collision(self.segments,self.head)
            time.sleep(self.delay)

            if self.a == 2 or self.b == 2:
                self.a = 0
                self.b = 0
                self.img_setup(self.im[self.count]) 
                self.turt_screen.bgcolor(self.colors[self.count])
                self.button_color_changer(self.colors[self.count])
                if self.count == 1:
                        self.head.color('#000066')
                        for sgmnt in self.segments:
                            sgmnt.color('#1a8cff')
                        if self.snake_no == 2:
                            self.h2.color('#000d1a')
                            for sgmnt in self.segments2:
                                sgmnt.color('#0066cc')
                else:
                    self.head.color('#804d00')
                    for sgmnt in self.segments:
                        sgmnt.color('#ff6666')
                    if self.snake_no == 2:
                        self.h2.color('#000d1a')
                        for sgmnt in self.segments2:
                            sgmnt.color('brown')
                self.count += 1
                if self.count == 2:
                    self.count = 0

    def segments_setup(self,seg):
        # for index in range(1, len(seg)):
        #     x = seg[index-1].xcor()
        #     y = seg[index-1].ycor()
        #     seg[index].goto(x, y)
        for index in range(len(seg)-1, 0, -1):
            x = seg[index-1].xcor()
            y = seg[index-1].ycor()
            seg[index].goto(x, y)

    def create_segments(self,id):
        self.new_segment = turtle.RawTurtle(self.turt_screen)
        self.new_segment.hideturtle()
        self.new_segment.speed(0)
        self.new_segment.shape('square')
        self.new_segment.penup()
        if id == 1:
            self.segments.append(self.new_segment)
            if self.count == 1:
                self.new_segment.color('#ff6666')
            else:
                self.new_segment.color('#1a8cff')
        elif id == 2:
            self.segments2.append(self.new_segment)
            if self.count == 1:
                self.new_segment.color('brown')
            else:
                self.new_segment.color('#0066cc')

    def write_score(self):
        self.pen = turtle.RawPen(self.turt_screen)
        self.pen.speed(0)
        self.pen.color("black")
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.goto(0, 300)

    def bring_high_score(self):
        try:
            k = self.cur.execute("select highest_score from high_score order by highest_score desc")
            if k > 0:
                self.high_score = self.cur.fetchone()[0]
                # self.pen.clear()
                # self.pen.write(f'Score:{self.score} High Score: {self.high_score}', align='center', font=('Courier', 24, 'normal'))

            i = self.cur.execute("select highest_score from multi_score order by highest_score desc")
            if i > 0:
                self.m_highscore = self.cur.fetchone()[0]
                    
        except Exception as e:
            print(e)

    def button_color_changer(self,color):
        self.button_sp['bg'] = color
        self.button_mp['bg'] = color
        self.b_save['bg'] = color
        self.button_load_s['bg'] = color 
        self.button_load_m['bg'] = color
        self.button_exit['bg'] = color

    def death(self):
        if self.snake_no == 1:
            time.sleep(1)
            self.head.goto(0,0)

            # resetting variables
            self.snake_size = 1
            self.speed = 20
            self.delay = 0.1

            # set score
            self.score = 0
            self.pen.clear()
            self.pen.write(f'Score:{self.score} High Score: {self.high_score}', align='center', font=('Courier', 24, 'normal'))

        elif self.snake_no == 2:

            # resetting variables
            self.snake_size = 1
            self.sec_snake_size = 1
            self.speed = 20
            self.sec_snake_speed = 20
            self.delay = 0.1

            self.head.goto(-100,0)
            self.h2.goto(100,0)
            self.h2.direction = 'stop'
            for segment in self.segments2:
                segment.goto(1000,1000)
            self.segments2.clear()

            # set score
            self.p1_score = 0
            self.p2_score = 0
            self.pen.clear()
            self.pen.write(f'P1-Score:{self.p1_score}  P2-Score:{self.p2_score}  High Score: {self.m_highscore}', align='center', font=('Courier', 20, 'normal'))

        self.head.direction = 'stop'

        for segment in self.segments:
            segment.goto(1000, 1000)

        self.segments.clear()

    def self_collision(self,segs,h):
        for segment in segs:
            if h.distance(segment) < 19.5:
                self.death()
                print('your snake collided')

    def img_setup(self, img):

        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()

        desert = Image.open(img)
        desert = desert.resize((self.width,self.height),Image.ANTIALIAS)
        self.resize_desert = ImageTk.PhotoImage(desert)

        self.can.create_image(0,0,image=self.resize_desert,anchor='nw')

    def single_player(self):
        def single_p(self):
            self.snake_no = 1
            self.head.direction = 'stop'
            self.score = 0
            self.food.st()
            self.head.goto(0,0)
            self.head.st()
            self.h2.ht()
            for sgmnt in self.segments2:
                sgmnt.goto(1000,1000)
            self.segments2.clear()

            for sgmnt in self.segments:
                sgmnt.goto(1000,1000)
            self.segments.clear()

            self.pen.clear()
            self.pen.write(f'Score:{self.score} High Score: {self.high_score}', align='center', font=('Courier', 24, 'normal'))

        self.button_sp = tk.Button(self.can,text='SINGLE PLAYER',command=lambda: single_p(self),bg='#ffd699')
        # button_sp.pack(side='left',anchor='ne',padx=20)
        self.can.create_window(10,10,anchor='nw',window=self.button_sp)

    def load_single(self):
        def load(self):
            i = self.cur.execute("select * from snake where sno=1")
            if i == 1:
                for sgmnt in self.segments:
                    sgmnt.goto(1000,1000)
                self.segments.clear()
                for sgmnt in self.segments2:
                    sgmnt.goto(1000,1000)
                self.segments2.clear()
                self.h2.direction = 'stop'

                values = self.cur.fetchone()
                self.snake_no = 1
                self.head.goto(values[1],values[2])
                self.food.goto(values[3],values[4])
                self.score = values[6]
                self.head.direction = 'stop'
                self.head.showturtle()
                self.food.st()
                self.h2.ht()
                for x in range(values[5]):
                    self.create_segments(1)

                self.pen.clear()
                self.pen.write(f'Score:{self.score} High Score: {self.high_score}', align='center', font=('Courier', 24, 'normal'))
        self.button_load_s = tk.Button(self.can,text='LOAD GAME',command=lambda : load(self),bg='#ffd699')
        self.can.create_window(290,10,anchor='nw',window=self.button_load_s)

    def snake_screen(self):
        # create canvas to hold turtle screen. And we need turtle screen to hold turtle objects or shapes.
        self.canvas = tk.Canvas(self.can,width=700,height=700)
        self.canvas.place(x=425,y=60)

        # turtle screen
        self.turt_screen = turtle.TurtleScreen(self.canvas)
        self.turt_screen.bgcolor('#fff5e6')

        # snake head
        self.head = turtle.RawTurtle(self.turt_screen)
        self.head.ht()
        self.head.shape('square')
        self.head.color('#804d00')
        self.head.penup()
        self.head.direction = 'stop'
        self.head._tracer(0)

    def foods(self):
        self.food = turtle.RawTurtle(self.turt_screen)
        self.food.ht()
        self.food.shape('circle')
        self.food.color('#336600')
        self.food._tracer(0)
        self.food.penup()
        self.food.goto(0,100)

    def move(self):
    
        if self.head.direction == 'up':
            y = self.head.ycor()
            self.head.sety(y + self.speed)

        if self.head.direction == 'down':            
            y = self.head.ycor()
            self.head.sety(y - self.speed)

        if self.head.direction == 'right':
            x = self.head.xcor()
            self.head.setx(x + self.speed)

        if self.head.direction == 'left':
            x = self.head.xcor()
            self.head.setx(x - self.speed) 


    def key_binds(self):
        def go_up():
            if self.head.direction != 'down':
                self.head.direction = 'up'      

        def go_down():
            if self.head.direction != 'up':
                self.head.direction = 'down'

        def go_left():
            if self.head.direction != 'right':
                self.head.direction = 'left'

        def go_right():
            if self.head.direction != 'left':
                self.head.direction = 'right'

        # keyboard bindings
        self.turt_screen.listen()
        self.turt_screen.onkeypress(go_up, 'w')
        self.turt_screen.onkeypress(go_down, 's')
        self.turt_screen.onkeypress(go_right, 'd')
        self.turt_screen.onkeypress(go_left, 'a')     
    
    def screen_closing(self):
        def on_closing(self):
            try:
                i = self.cur.execute("select highest_score from high_score order by highest_score desc")
                if i > 0:
                    highest_score = self.cur.fetchone()[0]
                    print(highest_score,'sing')
                    if self.high_score > highest_score:
                        j = self.cur.execute("insert into high_score (highest_score) values(%d)"%(self.high_score))
                        if j == 1:
                            self.con.commit()

                j = self.cur.execute("select highest_score from multi_score order by highest_score desc")
                if j > 0:
                    highest_score = self.cur.fetchone()[0]
                    if self.m_highscore > highest_score:
                        k = self.cur.execute("insert into multi_score (highest_score) values(%d)"%(self.m_highscore))
                        if k == 1:
                            self.con.commit()

            except Exception as e:
                print(e)

            finally:
                self.con.close()
                mixer.music.stop()
                self.destroy()

        self.protocol('WM_DELETE_WINDOW',lambda: on_closing(self))

    def save(self):
        def saves(self):
            self.head.direction = 'stop'
            self.h2.direction = 'stop'

            if self.snake_no == 1:
                i = self.cur.execute("select * from snake")
                if i == 1:
                    self.cur.execute("delete from snake where sno=1")
                
                j = self.cur.execute("insert into snake(sno, snake_x, snake_y, food_x ,food_y,segment_no, score) values(%d,%d,%d,%d,%d,%d,%d)"%(1,self.head.pos()[0],self.head.pos()[1],self.food.pos()[0],self.food.pos()[1],len(self.segments),self.score))
                if j == 1: 
                    self.con.commit()

            if self.snake_no == 2:
                l = self.cur.execute("select * from multi_snakes")
                if l == 1:
                    self.cur.execute("delete from multi_snakes where sno = 1")

                m = self.cur.execute("insert into multi_snakes(sno,snake_cord,food_cord,snake_2_cord,segment_no,scores) values(%d,'%s','%s','%s','%s','%s')"%(1,f'{self.head.xcor()},{self.head.ycor()}',f'{self.food.xcor()},{self.food.ycor()}',f'{self.h2.xcor()},{self.h2.ycor()}',f'{len(self.segments)},{len(self.segments2)}',f'{self.p1_score},{self.p2_score}'))
                if m == 1:
                    self.con.commit()
                
        self.b_save = tk.Button(self.can,text='SAVE',command= lambda: saves(self),bg='#ffd699')
        self.can.create_window(600,10,anchor='nw',window=self.b_save)
        
        

mixer.init()
mixer.music.load('music/Sands_of_Mystery.mp3')
mixer.music.play()

s = snake()

tk.mainloop()