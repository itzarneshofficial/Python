import turtle

# Set up the screen
screen = turtle.Screen()
screen.title("Itachi Uchiha")
screen.bgcolor("white")

# Create the turtle for drawing
itachi = turtle.Turtle()

# Function to draw a circle
def draw_circle(color, radius, x, y):
    itachi.penup()
    itachi.color(color)
    itachi.fillcolor(color)
    itachi.goto(x, y)
    itachi.pendown()
    itachi.begin_fill()
    itachi.circle(radius)
    itachi.end_fill()

# Function to draw Itachi's face outline
def draw_face():
    draw_circle("black", 100, 0, -100)

# Function to draw Itachi's eyes
def draw_eyes():
    draw_circle("white", 30, -40, -20)  # Left eye
    draw_circle("white", 30, 40, -20)   # Right eye

    draw_circle("black", 10, -40, -10)  # Left pupil
    draw_circle("black", 10, 40, -10)   # Right pupil

def main():
    draw_face()
    draw_eyes()

    itachi.hideturtle()
    turtle.done()

# Run the main function
if __name__ == "__main__":
    main()
