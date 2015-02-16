# Mini-project #6 - Blackjack
######################################3
#Imports
import simplegui
import random

######################################3
#Constant Globals
# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

DECKS = 1
DEALT = 2

X = 0
Y = 1
UP = True
DOWN = False
CANVAS_SIZE = [600,600]
DEALER_START_POS = [50,75]
PLAYER_START_POS= [50, CANVAS_SIZE[Y]-CARD_SIZE[Y]-20]
# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}
MAX_CARDS = 5

#######################################
#Aestetic Const
TITLE_FONT = 48
TITLE_POS = (20,50)
DEALER_TITLE = (50,(DEALER_START_POS[Y] + CARD_SIZE[Y]*1.1 + 36))
ALT_FONT = 36
PLAYER_TITLE = (50,(PLAYER_START_POS[Y]*.97))
LINE_POS = [(0,TITLE_POS[Y]*1.25),(CANVAS_SIZE[X],TITLE_POS[Y]*1.25)]
SCORE_POS = (3*CANVAS_SIZE[X]/5,TITLE_POS[Y])
POLY_P1 = (10, DEALER_TITLE[Y]*1.1)
POLY_P2 = (10, PLAYER_TITLE[Y]*.97 - ALT_FONT)
POLY_POS = [POLY_P1,POLY_P2,(CANVAS_SIZE[X]-10,POLY_P2[Y]),(CANVAS_SIZE[X]-10,POLY_P1[Y])]
OUT_POS = (20, POLY_P1[Y] + (POLY_P2[Y] - POLY_P1[Y])/3)
OUT_POS_2 = (20, POLY_P1[Y] + 2*(POLY_P2[Y] - POLY_P1[Y])/3)
#######################################
#Variable globals
# initialize some useful global variables
in_play = False
outcome = ""
m_msg_2 = ""
score = 0

######################################
#Classes
# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
            self.face_up = True
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank
        
    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        if self.face_up:
            my_card = card_images
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            my_size = CARD_SIZE
        else:
            my_card= card_back
            card_loc = CARD_BACK_CENTER
            my_size = CARD_BACK_SIZE  
        canvas.draw_image(my_card, card_loc, my_size, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        self.initiate_deck()
        self.orig_deck = self.deck[:]
        #self.shuffle()
        
    def initiate_deck(self):
        for d in range(DECKS):
            for s in SUITS:
                for r in RANKS:
                    self.deck[:] += [Card(s,r)]
                    
    def reset_deck(self):
        self.deck = self.orig_deck[:]
    
    def shuffle(self):
        # shuffle the deck 
        self.reset_deck()
        random.shuffle(self.deck)
       
    def shuffle_frag(self):
        random.shuffle(self.deck)
    
    def deal_card(self, c_dir):
        # deal a card object from the deck
        m_ret = self.deck.pop()
        m_ret.face_up = c_dir
        return m_ret
    
    def __str__(self):
        # return a string representing the deck
        my_return = ' '.join([str(x) for x in self.deck])
        return "Hand contains " + str(my_return)
    
# define hand class
class Hand:
    def __init__(self, start_pos):
        # = true Hand object
        #Start pos represent where hand is displayed on canvas
        self.hand = []
        self.in_play = True
        self.start_pos = start_pos
        self.aces = False
   
    def __str__(self):
        # return a string representation of a hand
        my_return = ' '.join([str(x) for x in self.hand])
        return "Hand contains " + str(my_return)
    
    def return_value(self):
        m_ret = ""
        if self.aces:
            if self.hand_value + 10 <= 21 :
                m_ret += ("(" + str(self.hand_value) +  ") / ")
        m_ret += "(" + str(self.get_value())        
        m_ret += ")"
        return m_ret
        
    def add_card(self, deck, c_dir):
        self.hand += [deck.deal_card(c_dir)]
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        self.aces = False
        self.hand_value = 0
        for c in self.hand:
            self.hand_value += VALUES[c.get_rank()]
            if c.get_rank() == RANKS[0]:
                self.aces = True
        if not self.aces:
            return self.hand_value
        else:
            if self.hand_value + 10 <= 21 :
                return self.hand_value + 10
            else:
                return self.hand_value
                
    def draw(self, canvas):
        # draw a hand on the canvas, use the draw method for cards      
        for c in range(len(self.hand)):
            self.draw_pos = (self.start_pos[X] + c*((CANVAS_SIZE[X] - self.start_pos[X])//MAX_CARDS), self.start_pos[Y])
            self.hand[c].draw(canvas, self.draw_pos )
                            
    def show(self):
        for x in self.hand:
            if not x.face_up: x.face_up = True

######################################
# class globals
#Deck
deck= Deck()

#Hand
player = Hand(PLAYER_START_POS)
dealer = Hand(DEALER_START_POS)
######################################
#Event Handlers
#define event handlers for buttons
def deal():
    global outcome, deck, player, dealer, in_play, score, m_msg_2
    outcome = "Hit or Stand?"
    m_msg_2 = ""
    if in_play == True:
        score -= 1
        outcome = "Thats Cheating! You lose!"
        m_msg_2 = "Hit or Stand?"
    in_play = True
    player = Hand(PLAYER_START_POS)
    dealer = Hand(DEALER_START_POS)
    deck.shuffle()
    for x in range(DEALT):
        player.add_card(deck, UP)
        dealer.add_card(deck, (x==1))

def hit():
    global in_play, outcome, score, m_msg_2
    if in_play:
        # if the hand is in play, hit the player
        player.add_card(deck, UP)
        if player.get_value() > 21:
            # if busted, assign a message to outcome, update in_play and score
            outcome = "You Have Busted!"
            m_msg_2 = "Select 'Deal' to play another round."  
            score -= 1
            in_play = False
        else:
            outcome = "Hit or Stand?"
        m_msg_2 = ""
                 
def stand():
    # replace with your code below
    global score, in_play, outcome, m_msg_2
    if in_play:
        in_play = False
        dealer_play()
        dealer.show()
        if dealer.get_value() > 21 or dealer.get_value() < player.get_value():
            #Player Wins:
            outcome = "Player has won!"
            score += 1
        else:
            outcome = "Dealer wins"
            score -= 1
        m_msg_2 = "Select 'Deal' to play another round."  
           
def dealer_play():
    while dealer.get_value() < 17:
        dealer.add_card(deck, UP)
        
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Blackjack", TITLE_POS, TITLE_FONT, "White")
    canvas.draw_text("Score : " + str(score), SCORE_POS, ALT_FONT, "White")
    if in_play or player.get_value() > 21 :
        d_r = ""
    else:
        d_r = str(dealer.return_value())

        
    canvas.draw_text("Dealer " + d_r, DEALER_TITLE, ALT_FONT, "White")
    canvas.draw_text("Player " + str(player.return_value()), PLAYER_TITLE, ALT_FONT, "White")
    canvas.draw_line(LINE_POS[X], LINE_POS[Y], 2, "White")
    canvas.draw_polygon(POLY_POS, 2, "White")
    canvas.draw_text(outcome, OUT_POS, ALT_FONT + 2, "Orange")
    canvas.draw_text(m_msg_2, OUT_POS_2, ALT_FONT + 2, "Orange")
    player.draw(canvas)
    dealer.draw(canvas)
    
######################################
# initialization frame
frame = simplegui.create_frame("Blackjack", CANVAS_SIZE[X], CANVAS_SIZE[Y])
frame.set_canvas_background("Green")

######################################
#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
b_hit = frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

######################################
# get things rolling
deal()
frame.start()
