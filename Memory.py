# implementation of card game - Memory
#Participant clicks on two cards. If paired keeps them exposed
#If not then flips them over.
#ignore clicks on cards already exposed.

######################################
#Imports
import simplegui
import random
######################################
#Globals
#CONST
NUMBER_CARDS = 16
CARD_WIDTH = 50
CARD_HEIGHT = 100
X = 0
Y = 1
P1 = 0
P3 = 2
POS = 0
SET = 1
VALUE = 2
#Other GLobals
state = 0
canvas = [NUMBER_CARDS*CARD_WIDTH, CARD_HEIGHT]
turns = 0
cards = []
cardA = []
cardB = []
######################################
#Helper Function
# New Game
def new_game():
    global cards, turns, state, cardA, cardB
    state = 0
    turns = 0
    cardA = []
    cardB = []
    my_range = range(NUMBER_CARDS/2)*2
    random.shuffle(my_range)
    for x in range(len(my_range)):
        card_borders = [(x*CARD_WIDTH,0),(x*CARD_WIDTH,CARD_HEIGHT), ((x+1)*CARD_WIDTH-1, CARD_HEIGHT),((x+1)*CARD_WIDTH,0)]
        cards = cards[:] + [[card_borders, False, my_range.pop()]]

def ret_color(val):
    if val:
        return "Black"
    return "Green"
     
# define event handlers
def mouseclick(pos):
    global selected, turns, cardA, cardB
    # Find what card was clicked
    for card in cards:
        if pos[X] >= card[POS][P1][X] and pos[X] <= card[POS][P3][X]:
            sel_card = card
    if sel_card[SET] == False:
        if state < 2:
            #first clear a and b
            if state == 1 and cardA[VALUE] <> cardB[VALUE]:
                cardA[SET] = False
                cardB[SET] = False
            #Now for new value 
            turns += 1
            cardA = sel_card
            cardA[SET] = True
        if state == 2:
            cardB = sel_card
            cardB[SET] = True
            
        buttonclick()
   
def buttonclick():
    global state
    if state == 0:
        state = 2
    elif state == 1:
        state = 2
    else:
        state = 1
    #state represents number of cards exposed in memory

######################################
#Event Handlers	
# cards are logically 50x100 pixels in size    
def draw(canvas):
    label.set_text("Turns : " + str(turns))
    for card in cards:
        canvas.draw_polygon(card[POS], 2, "Grey", ret_color(card[SET]))
        if card[SET]:
            canvas.draw_text(str(card[VALUE]), [card[POS][P1][X] + CARD_WIDTH/3, card[POS][P3][Y] - CARD_HEIGHT/3], 32, "White")
######################################
# create frame
frame = simplegui.create_frame("Memory", canvas[X], canvas[Y])
######################################
#Add controls
frame.add_button("Restart", new_game)
label = frame.add_label("Turns : " + str(turns))
######################################
# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)
######################################
# get things rolling
new_game()
frame.start()