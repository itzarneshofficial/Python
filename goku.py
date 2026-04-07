import turtle

# Set up the screen
screen = turtle.Screen()
screen.title("Goku")
screen.bgcolor("white")

# Create the turtle for drawing
goku = turtle.Turtle()
goku.speed(3)

def draw_circle(t, radius, x, y, color):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)
    t.begin_fill()
    t.circle(radius)
    t.end_fill()

def draw_polygon(t, points, color):
    t.penup()
    t.goto(points[0])
    t.pendown()
    t.color(color)
    t.begin_fill()
    for point in points:
        t.goto(point)
    t.goto(points[0])
    t.end_fill()

# Draw Goku's head
draw_circle(goku, 100, 0, -100, "orange")

# Draw Goku's eyes
draw_circle(goku, 20, -35, 20, "white")
draw_circle(goku, 20, 35, 20, "white")
draw_circle(goku, 10, -35, 30, "black")
draw_circle(goku, 10, 35, 30, "black")

# Draw Goku's nose
draw_circle(goku, 10, 0, 0, "orange")

# Draw Goku's mouth
goku.penup()
goku.goto(-40, -20)
goku.pendown()
goku.color("black")
goku.right(60)
goku.circle(40, 120)
goku.penup()

# Draw Goku's hair
hair_points = [
    (-50, 100), (-70, 200), (-30, 150), (0, 200),
    (30, 150), (70, 200), (50, 100), (0, 140)
]
draw_polygon(goku, hair_points, "black")

# Hide the turtle and display the window
goku.hideturtle()
turtle.done()
