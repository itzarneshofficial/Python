from turtle import *

# Set up the screen and turtle properties
bgcolor("black")
pensize(2)
color("green")
left(90)           # Start pointing up
backward(100)      # Move turtle down to give space for the tree
speed("fastest")   # Use a predefined speed string
shape("turtle")

def tree(i):
    if i < 10:
        return
    else:
        forward(i)
        color("orange")    # Leaf color
        circle(2)          # Draw a small circle for leaf
        color("brown")     # Back to branch color
        
        # Recursively draw branches
        left(30)
        tree(3 * i / 4)    # Left branch
        
        right(60)
        tree(3 * i / 4)    # Right branch
        
        left(30)           # Return to initial orientation
        backward(i)        # Go back to previous branch point

# Start drawing the tree
tree(100)

# Finish
done()
