#Guess the number

###############################################
#Import libraries
import random
import simplegui
import math

###############################################
# initialize global variables used in your code
num_range = 100
guesses = 7
guesses_remaining = guesses
my_number = 0

###############################################
# helper function to start and restart the game
def new_game():
    global guesses_remaining, my_number
    my_number = random.randrange(0,num_range)
    guesses_remaining = guesses
    print
    print "New Game. Range is from 0 to", num_range
    print "Number of guesses is", guesses_remaining

###############################################
# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    global num_range, guesses
    num_range, guesses = 100, 7
    new_game()

def range1000():
    # button that changes range to range [0,1000) and restarts
    global num_range, guesses
    num_range, guesses = 1000, 10
    new_game()
    
def input_guess(guess):
    # Main game logic.
    global guesses_remaining
    guessed = int(guess)
    guesses_remaining -= 1
    
    print
    print "Guess was", guessed
    print "Number of remaining guesses is", (guesses_remaining)
    
    #determine game status
    if guessed == my_number:
        print "Correct!"
        new_game()
    elif guesses_remaining == 0:
        print "You ran out of guesses. You lose"
        new_game()
    elif guessed < my_number:
        print "Higher!"
    else:
        print "Lower!"
              
###############################################   
# create frame
f = simplegui.create_frame("Guess the number", 200, 200)

###############################################
# register event handlers for control elements
f.add_button("Range is [0,100)", range100, 200)
f.add_button("Range is [0,1000)", range1000, 200)
f.add_input("Guess", input_guess, 200)

###############################################
# call new_game and start frame
new_game()
f.start()
