import turtle

# Set up the screen
screen = turtle.Screen()
screen.title("Simple House")
screen.bgcolor("white")

# Create the turtle for drawing
house = turtle.Turtle()
house.speed(3)

def draw_square(t, size, color):
    t.color(color)
    t.begin_fill()
    for _ in range(4):
        t.forward(size)
        t.right(90)
    t.end_fill()

def draw_rectangle(t, width, height, color):
    t.color(color)
    t.begin_fill()
    for _ in range(2):
        t.forward(width)
        t.right(90)
        t.forward(height)
        t.right(90)
    t.end_fill()

def draw_triangle(t, size, color):
    t.color(color)
    t.begin_fill()
    for _ in range(3):
        t.forward(size)
        t.left(120)
    t.end_fill()

def draw_house():
    # Draw the base of the house
    house.penup()
    house.goto(-100, -100)
    house.pendown()
    draw_square(house, 200, "red")
    
    # Draw the roof
    house.penup()
    house.goto(-120, 100)
    house.pendown()
    draw_triangle(house, 240, "brown")
    
    # Draw the door
    house.penup()
    house.goto(-30, -100)
    house.pendown()
    draw_rectangle(house, 60, 100, "blue")
    
    # Draw windows
    house.penup()
    house.goto(-70, 0)
    house.pendown()
    draw_square(house, 40, "white")
    
    house.penup()
    house.goto(30, 0)
    house.pendown()
    draw_square(house, 40, "white")

# Draw the house
draw_house()

# Hide the turtle and display the window
house.hideturtle()
turtle.done()
