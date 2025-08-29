import curses as cur
from curses.ascii import ESC
import random

starty = 4
startx = 6

def roller(win):
    global starty, startx
    starty = 4
    startx = 6
    for i in range(5):
        win.move(starty+1, startx)
        x = f"{chr(0x2502)}{' '}{random.randint(1, 6)}{' '}{chr(0x2502)}"
        win.addstr(x)
        win.refresh()
        startx+=7

def main(scr):
    global starty, startx
    # setup loop boolean
    running = True

    # Define window geometry
    # [Height, Width, top, left]
    W = [25, 80, 0, 0]

    # initial the screen
    scr = cur.initscr()

    # initialize the main window and draw it
    win = cur.newwin(W[0], W[1], W[2], W[3])
    win.box()  # draws a box around the window
    win.refresh()

    for i in range(5):
        win.move(starty,startx)
        x = f"{chr(0x250C)}{chr(0x2500)*3}{chr(0x2510)}"
        win.addstr(x)
        win.move(starty+1,startx)
        x = f"{chr(0x2502)}{' - '}{chr(0x2502)}"
        win.addstr(x)
        win.move(starty+2, startx)
        x = f"{chr(0x2514)}{chr(0x2500) * 3}{chr(0x2518)}"
        win.addstr(x)
        win.refresh()
        startx+=7


    while running:
        scr.nodelay(True) # don't wait for keyboard input to continue execution
        ch = scr.getch()  # get keyboard input from user

        if ch in [ESC, ord('q'), ord('Q')]:  # Quit the program if ESC or 'q' is pressed
            running = False

        # do something useful
        if ch in [ord('r'), ord('R')]:
             roller(win)
        #
        # if ch in [ord('t'), ord('T')]:
        #     d.reset()

# Body of App
# curses.wrapper() is a convenience function that calls the main() function and closes the window cleanly
cur.wrapper(main)