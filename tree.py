import turtle

# Set up the screen
screen = turtle.Screen()
screen.title("Tree with Turtle Graphics")
screen.bgcolor("white")

# Create the turtle
tree_turtle = turtle.Turtle()
tree_turtle.shape("turtle")
tree_turtle.color("green")
tree_turtle.speed("fastest")  # Speed up drawing

# Define the recursive function to draw the tree
def draw_branch(turtle, branch_length, angle):
    if branch_length > 5:  # Base case: stop when the branch is very short
        # Draw the branch
        turtle.forward(branch_length)
        
        # Draw right branch
        turtle.right(angle)
        draw_branch(turtle, branch_length - 15, angle)  # Reduce branch length
        
        # Draw left branch
        turtle.left(2 * angle)
        draw_branch(turtle, branch_length - 15, angle)  # Reduce branch length
        
        # Return to the original position and angle
        turtle.right(angle)
        turtle.backward(branch_length)

# Position the turtle
tree_turtle.penup()
tree_turtle.goto(0, -200)  # Move to the bottom center of the screen
tree_turtle.left(90)       # Point the turtle upwards
tree_turtle.pendown()

# Draw the tree
draw_branch(tree_turtle, 100, 30)  # Initial branch length and angle

# Hide the turtle and display the window
tree_turtle.hideturtle()
turtle.done()
