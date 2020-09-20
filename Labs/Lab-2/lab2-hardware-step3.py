import turtle

wn = turtle.Screen()
t = turtle.Turtle()

def fwd ():
    t.forward(20)
        
def bkw():
    t.forward(-20)
    
def rt ():
    t.right(20)
    
def lt ():
    t.left(20)
        
wn.onkey(fwd,'Up')
wn.onkey(bkw,'Down')
wn.onkey(rt, 'Right')
wn.onkey(lt, 'Left')

wn.listen()
