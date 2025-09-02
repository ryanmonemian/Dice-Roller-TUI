import curses as cur
from curses.ascii import ESC
import random

starty = 4
startx = 6

class Die():
    def __init__(self, y, x, win):
        self.y = y
        self.x = x
        self.value = "-"
        self.win = win
        self.held = False

    def roll(self):
        if not self.held:
            self.value = random.randint(1,6)
            self.draw()

    def draw(self):
        self.win.move(self.y, self.x)
        die_top = f"{chr(0x250C)}{chr(0x2500) * 3}{chr(0x2510)}"
        self.win.addstr(die_top)
        self.win.move(self.y + 1, self.x)
        die_mid = f"{chr(0x2502)}{' '}{self.value}{' '}{chr(0x2502)}"
        self.win.addstr(die_mid)
        self.win.move(self.y + 2, self.x)
        die_bot = f"{chr(0x2514)}{chr(0x2500) * 3}{chr(0x2518)}"
        self.win.addstr(die_bot)
        self.win.move(self.y + 3, self.x + 2)
        if self.held:
            self.win.addstr(f"{chr(0x25C9)}")
        else:
            self.win.addstr(f"{chr(0x25CB)}")
        self.win.refresh()

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
    dice = []
    starty = 4
    startx = 6
    for i in range (5):
        dice.append(Die(starty, startx, win))
        dice[i].draw()
        startx+=7

    while running:
        scr.nodelay(True) # don't wait for keyboard input to continue execution
        ch = scr.getch()  # get keyboard input from user

        if ch in [ESC, ord('q'), ord('Q')]:  # Quit the program if ESC or 'q' is pressed
            running = False

        # do something useful
        if ch in [ord('r'), ord('R')]:
            for i in range(5):
                dice[i].roll()
            win.refresh()


        if ch in  [ord('1'), ord('2'), ord('3'), ord('4'), ord('5')]:
            ind = int(chr(ch))-1
            dice[ind].held = not dice[ind].held
            dice[ind].draw()
        #
        # if ch in [ord('t'), ord('T')]:
        #     d.reset()

# Body of App
# curses.wrapper() is a convenience function that calls the main() function and closes the window cleanly
cur.wrapper(main)