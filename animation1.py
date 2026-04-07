import turtle
import time

# Set up the screen
screen = turtle.Screen()
screen.title("Happy Birthday Animation")
screen.bgcolor("black")

# Create a turtle for drawing
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.hideturtle()

# Function to draw the text
def draw_text(message, color, x, y):
    pen.penup()
    pen.goto(x, y)
    pen.color(color)
    pen.write(message, align="center", font=("Arial", 24, "bold"))
    pen.pendown()

# Function to animate the text
def animate_text():
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    message = "Happy Birthday!"
    x, y = 0, 0

    for color in colors:
        pen.clear()
        draw_text(message, color, x, y)
        time.sleep(0.5)

# Run the animation
animate_text()

# Keep the window open
screen.mainloop()
