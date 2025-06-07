import turtle
import random

# --- Screen Setup
screen = turtle.Screen()
screen.title("Flappy Bird Full Fixed")
screen.bgcolor("skyblue")
screen.setup(width=500, height=600)
screen.tracer(0)

# --- Ground Line
ground_line = -250
ground = turtle.Turtle()
ground.penup()
ground.goto(-250, ground_line)
ground.color("darkgreen")
ground.pendown()
ground.begin_fill()
for _ in range(2):
    ground.forward(500)
    ground.right(90)
    ground.forward(40)
    ground.right(90)
ground.end_fill()
ground.hideturtle()

# --- Bird Setup
bird = turtle.Turtle()
bird.shape("turtle")
bird.color("orange")
bird.shapesize(1.5)
bird.penup()
bird.goto(-100, 0)
bird.dy = 0
gravity = -0.3

# --- Score Display
score = 0
pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.color("white")
pen.goto(0, 260)
pen.write("Score: 0", align="center", font=("Arial", 24, "bold"))

# --- Pipe Setup
pipes = []
gap = 150
pipe_speed = 3
frame_count = 0
game_running = True

# --- Controls
def flap():
    bird.dy = 6

screen.listen()
screen.onkeypress(flap, "space")

# --- Pipe Generation
def create_pipe():
    top_pipe = turtle.Turtle()
    top_pipe.shape("square")
    top_pipe.color("forest green")
    top_pipe.shapesize(stretch_wid=18, stretch_len=3)
    top_pipe.penup()
    top_y = random.randint(100, 250)
    top_pipe.goto(250, top_y)

    bottom_pipe = turtle.Turtle()
    bottom_pipe.shape("square")
    bottom_pipe.color("forest green")
    bottom_pipe.shapesize(stretch_wid=18, stretch_len=3)
    bottom_pipe.penup()
    bottom_pipe.goto(250, top_y - gap - 360)

    pipes.append((top_pipe, bottom_pipe))

# --- Game Over
def game_over():
    global game_running
    game_running = False
    pen.goto(0, 0)
    pen.color("red")
    pen.write("GAME OVER!", align="center", font=("Arial", 28, "bold"))
    screen.update()

# --- Main Game Loop
def game_loop():
    global frame_count, game_running, score

    if not game_running:
        return

    bird.dy += gravity
    bird.sety(bird.ycor() + bird.dy)

    # Check for ground or sky collision
    if bird.ycor() < ground_line + 20 or bird.ycor() > 280:
        game_over()
        return

    # Move pipes and check collision
    for top, bottom in pipes:
        top.setx(top.xcor() - pipe_speed)
        bottom.setx(bottom.xcor() - pipe_speed)

        # Bounding box collision detection
        for pipe in [top, bottom]:
            pipe_left = pipe.xcor() - 30
            pipe_right = pipe.xcor() + 30
            pipe_top = pipe.ycor() + 180
            pipe_bottom = pipe.ycor() - 180

            bird_left = bird.xcor() - 10
            bird_right = bird.xcor() + 10
            bird_top = bird.ycor() + 10
            bird_bottom = bird.ycor() - 10

            if (bird_right > pipe_left and
                bird_left < pipe_right and
                bird_top > pipe_bottom and
                bird_bottom < pipe_top):
                game_over()
                return

    # Remove off-screen pipes
    pipes[:] = [(top, bottom) for top, bottom in pipes if top.xcor() > -300]

    # Pipe spawning and scoring
    frame_count += 1
    if frame_count % 100 == 0:
        create_pipe()
        score += 1
        pen.clear()
        pen.goto(0, 260)
        pen.write(f"Score: {score}", align="center", font=("Arial", 24, "bold"))

    screen.update()
    screen.ontimer(game_loop, 20)

# --- Start Game
game_loop()
screen.mainloop()
