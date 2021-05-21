import turtle

def sec_snake(z):
    head2 = turtle.RawTurtle(z)
    head2.hideturtle()
    head2.direction = 'stop'
    head2.speed(0)
    head2.shape('square')
    head2.color('#4d0000')
    head2.penup()
    head2.goto(100, 0)


    def move2(speed,snake_no):

        if head2.direction == 'up':
            y = head2.ycor()
            head2.sety(y + speed)

        if head2.direction == 'down':
            y = head2.ycor()
            head2.sety(y - speed)

        if head2.direction == 'right':
            x = head2.xcor()
            head2.setx(x + speed)

        if head2.direction == 'left':
            x = head2.xcor()
            head2.setx(x - speed)

        def go_up2():
            if head2.direction != 'down':
                head2.direction = 'up'

        def go_down2():
            if head2.direction != 'up':
                head2.direction = 'down'

        def go_left2():
            if head2.direction != 'right':
                head2.direction = 'left'

        def go_right2():
            if head2.direction != 'left':
                head2.direction = 'right'

        # keybinding for 2nd snake
        nonlocal z
        z.listen()
        # if snake_no == 2:
        z.onkeypress(go_up2, 'i')
        z.onkeypress(go_down2, 'k')
        z.onkeypress(go_right2, 'l')
        z.onkeypress(go_left2, 'j')

    return move2, head2

