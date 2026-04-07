import turtle

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("white")
screen.title("Simple Car Drawing")

# Create turtle object
car = turtle.Turtle()

# Draw the car body
car.color("black")
car.fillcolor("gray")
car.begin_fill()
car.forward(200)   # Length of the car
car.left(90)
car.forward(50)    # Height of the car
car.left(90)
car.forward(200)
car.left(90)
car.forward(50)
car.end_fill()

# Draw the roof
car.color("black")
car.fillcolor("darkgray")
car.begin_fill()
car.left(135)
car.forward(70.71) # Diagonal of the roof
car.right(90)
car.forward(70.71)
car.end_fill()

# Draw the windows
car.penup()
car.goto(50, 50)
car.pendown()
car.fillcolor("white")
car.begin_fill()
car.setheading(45)
car.forward(50)
car.right(90)
car.forward(50)
car.right(135)
car.forward(70.71)
car.end_fill()

car.penup()
car.goto(150, 50)
car.pendown()
car.fillcolor("white")
car.begin_fill()
car.setheading(45)
car.forward(50)
car.right(90)
car.forward(50)
car.right(135)
car.forward(70.71)
car.end_fill()

# Draw the wheels
car.penup()
car.goto(40, -10)
car.pendown()
car.color("black")
car.circle(20)

car.penup()
car.goto(160, -10)
car.pendown()
car.circle(20)

# Hide the turtle
car.hideturtle()

# Keep the window open
turtle.done()
