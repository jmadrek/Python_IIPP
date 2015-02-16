# template for "Stopwatch: The Game"
# start, stop and reset button. 
# Goal is to stop stopwatch on a whole number
# Reset sets everything back to zero and stops watch
##################################################
#Imports
import simplegui


##################################################
# define global variables
#1 represents 100 ms
time = 0
tries = 0
catch = 0
##################################################
# define helper function format that converts time

# in tenths of seconds into formatted string A:BC.D
#Should be zero if no value
def format(t):
    ms = time%10
    sec = (time/10)%60
    min = int(time/600)
    return az(str(min)) + ":" + az(str(sec)) + "." + str(ms)
    
def az(t):
    if len(t) >= 2:
        return str(t)
    else:
        return "0" + t

##################################################    


# define draw handler

def draw_handler(canvas):
    canvas.draw_text(format(time), (50,100), 32, "Red")
    canvas.draw_text(str(catch) +'/' + str(tries), (150,24), 24, "Blue")
# define event handler for timer with 0.1 sec interval
def timer_handler():
    global time
    time += 1

# define event handlers for buttons; "Start", "Stop", "Reset"
def button_start():
    timer.start()
    
def button_stop():
    global tries, catch
    allow = timer.is_running()
    timer.stop()
    if allow:
        tries += 1
        if time%10 == 0:
            catch += 1

def button_restart():
    global time, catch, tries
    timer.stop()
    time,catch,tries = 0,0,0


##################################################    
# create frame
f = simplegui.create_frame("Guess the number", 200, 200)

##################################################
# register event handlers
f.set_draw_handler(draw_handler)

timer = simplegui.create_timer(100, timer_handler)
f.add_button('Start', button_start, 100)
f.add_button('Stop', button_stop, 100)
f.add_button('Restart', button_restart, 100)
##################################################
# start frame
f.start()
