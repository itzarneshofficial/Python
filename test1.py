import turtle

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("black")

# Create turtle object
rgb_turtle = turtle.Turtle()
rgb_turtle.speed(0)  # Fastest speed
rgb_turtle.width(2)

# RGB gradient circle
for i in range(360):
    rgb_turtle.color((i % 100) / 100, (i % 200) / 200, (i % 300) / 300)
    rgb_turtle.forward(1)
    rgb_turtle.left(1)

# Hide the turtle
rgb_turtle.hideturtle()

# Keep the window open
turtle.done()
