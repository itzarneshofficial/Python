import turtle

# Set up the screen
screen = turtle.Screen()
screen.title("Interactive Dragon Curve with Turtle Graphics")
screen.bgcolor("black")

# Create the turtle
dragon_turtle = turtle.Turtle()
dragon_turtle.shape("turtle")
dragon_turtle.color("white")
dragon_turtle.speed("fastest")

# Global variable to control the depth of recursion
depth = 5

# Function to draw the Dragon Curve
def dragon_curve(turtle, length, depth, sign=1):
    if depth == 0:
        turtle.forward(length)
    else:
        turtle.right(45 * sign)
        dragon_curve(turtle, length / (2 ** 0.5), depth - 1, 1)
        turtle.left(90 * sign)
        dragon_curve(turtle, length / (2 ** 0.5), depth - 1, -1)
        turtle.right(45 * sign)

# Function to clear and redraw the dragon curve with the current depth
def redraw():
    dragon_turtle.clear()
    dragon_turtle.penup()
    dragon_turtle.goto(-100, 0)
    dragon_turtle.pendown()
    dragon_curve(dragon_turtle, 200, depth)

# Increase depth
def increase_depth():
    global depth
    if depth < 15:  # Limit to avoid excessive recursion depth
        depth += 1
        redraw()

# Decrease depth
def decrease_depth():
    global depth
    if depth > 1:  # Minimum depth of 1
        depth -= 1
        redraw()

# Initial draw
redraw()

# Bind the keys for interaction
screen.listen()
screen.onkey(increase_depth, "Up")      # Press Up arrow to increase depth
screen.onkey(decrease_depth, "Down")    # Press Down arrow to decrease depth

# Keep the window open
turtle.done()
