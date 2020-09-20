from sense_hat import SenseHat
import time

s = SenseHat()

current_initial = {
              "initials:"("firstname", "surname"),
              "selected" : 0
  }

nothing = (0,0,0)
pink = (255,105, 180)

def initial_firstname():
    P = pink
    O = nothing
    logo = [
    P, P, O, O, O, O, P, P,
    P, P, P, O, O, P, P, P,
    P, P, O, P, P, O, P, P,
    P, P, O, P, P, O, P, P,
    P, P, O, P, P, O, P, P,
    P, P, O, O, O, O, P, P,
    P, P, O, O, O, O, P, P,
    P, P, O, O, O, O, P, P,
    ]
    return logo

def initial_surname():
    P = pink
    O = nothing
    logo = [
    P, P, O, O, O, O, P, P,
    P, P, P, O, O, P, P, P,
    P, P, O, P, P, O, P, P,
    P, P, O, P, P, O, P, P,
    P, P, O, P, P, O, P, P,
    P, P, O, O, O, O, P, P,
    P, P, O, O, O, O, P, P,
    P, P, O, O, O, O, P, P,
    ]
    return logo


def which_init(state):
  
  curr = state["initials"]
  return curr [state["selected"] % len(curr)]
def display(state):
  what_initial = which_init(state)
  
  if what_initial == "firstname"
    sense.set_pixels(initial_firstname())
  elif what_initial == "surname"
  sense.set_pixels(initial_surname())
  
while True:
  movement = sense.stick.get_movements()
  if movement:
    for events in movements:
      if events.action != 'pressed':
        continue
      if events.direction == 'right':
        current_initial["selected"] += 1
        display(current_initial)
      elif events.direction == 'left':
        current_initial["selected"] += 1
        display(current_initial)
      elif events.direction == 'up':
        current_initial["selected"] += 1
        display(current_initial)
      elif events.direction == 'down':
        current_initial["selected"] += 1
        display(current_initial)
