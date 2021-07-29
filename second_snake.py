import turtle

def sec_snake(screen):
    head2 = turtle.RawTurtle(screen)


    
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
        nonlocal screen
        screen.listen()
        # if snake_no == 2:
        screen.onkeypress(go_up2, 'i')
        screen.onkeypress(go_down2, 'k')
        screen.onkeypress(go_right2, 'l')
        screen.onkeypress(go_left2, 'j')

    return move2, head2

