# This code uses the turtle graphics library to draw a triangle.
import turtle
import time

pointer = turtle.Turtle()
pointer.shape('turtle')

pointer.fillcolor('blue')  # Set the fill color to blue
pointer.begin_fill()

while True:
    # Draw a triangle
    for i in range(3):
        pointer.forward(100)
        pointer.left(120)
        
    break    

pointer.end_fill()  # Fill the triangle with blue color 

time.sleep(5)  # Pause for 5 seconds to view the drawing

# Hide the turtle and finish
pointer.hideturtle()