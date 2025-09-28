import curses as cur
from curses.ascii import ESC
import numpy as np

'''
Development Steps:
☐ ☑
☑ start with this simple, 'linear' script (code)
☑ make the dice fancier with Unicode characters 
☑ add the ability to hold a particular die (use a nested dictionary for the dice)
☑ create functions for main loop and for rolling the dice
☑ create a Die class with methods to init(), roll(), draw() 
☑ convert into a TUI using ncurses to provide keyboard, mouse interaction, color, etc.
'''



class Die():
    def __init__(self, y, x, win):
        self.y = y
        self.x = x
        self.top_left = (y, x)
        self.bot_right = (y+2,x+4)
        self.INIT_VALUE = "-"
        self.value = self.INIT_VALUE
        self.win = win
        self.held = False

    def roll(self):
        if not self.held:
            self.value = np.random.randint(1,7)
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

    def toggle_hold(self):
        if self.value == self.INIT_VALUE:
            return False
        self.held = not self.held
        self.draw()
        return True


    def is_clicked(self, y_mouse, x_mouse):
        if (self.top_left[0] <= y_mouse <= self.bot_right[0]) and (self.top_left[1] <= x_mouse <= self.bot_right[1]):
            self.toggle_hold()
            return True
        else:
            return False

class Dice():
    def __init__(self, win):
        self.dice = []
        self.y = 4
        self.x = 6
        self.ALLOWED_ROLLS = 3
        self.rolls_remaining = self.ALLOWED_ROLLS
        self.win = win
        for i in range(5):
            self.dice.append(Die(self.y, self.x, win))
            self.dice[i].draw()
            self.x += 7
        self.draw()

    def roll(self):
        if self.rolls_remaining != 0:
            for i in self.dice:
                i.roll()
            self.rolls_remaining -= 1
            self.draw()

    def reset(self):
        # reset rolls remaining
        self.rolls_remaining = self.ALLOWED_ROLLS
        # set dice to '-'
        for i in self.dice:
            i.value = i.INIT_VALUE
            i.held = False
            i.draw()
        self.draw()
        # set hold state to open circles

    def draw(self):
        self.win.move(13, 6)
        self.win.addstr(f"Rolls Remaining: {self.rolls_remaining}")
        self.win.refresh()


class Button():
    def __init__(self, win, b, x):
        self.win = win
        self.b = b
        self.y = 9
        self.x = x
        self.length = len(b["label"]) + 2
        visual_width = self.length + 2
        self.top_left = x
        self.bot_right = x + visual_width - 1

    def is_clicked(self, y_mouse, x_mouse):
        if self.y <= y_mouse <= self.y + 2:
            if self.top_left <= x_mouse <= self.bot_right:
                return self.b["key"]
        return None

    def draw(self):
        self.win.move(self.y, self.x)
        but_top = f"{chr(0x250C)}{chr(0x2500) * self.length}{chr(0x2510)}"
        self.win.addstr(but_top)
        self.win.move(self.y + 1, self.x)
        but_mid = f"{chr(0x2502)} {self.b['label']} {chr(0x2502)}"
        self.win.addstr(but_mid)
        self.win.move(self.y + 2, self.x)
        but_bot = f"{chr(0x2514)}{chr(0x2500) * self.length}{chr(0x2518)}"
        self.win.addstr(but_bot)
        self.win.refresh()

def main(scr):

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

    dice = Dice(win)
    buttons_dict = [
        {
            "label": "Roll",
            "key": "r",
            "top_left": None,
            "bot_right": None,
        },
        {
            "label": "Reset",
            "key": "t",
            "top_left": None,
            "bot_right": None,
        },
        {
            "label": "Quit",
            "key": "q",
            "top_left": None,
            "bot_right": None,
        }
    ]
    x = 6
    spacing = 5
    my_buttons = []
    for i,b in enumerate(buttons_dict):
        buttons_dict[i]["top_left"] = x
        my_buttons.append(Button(win, b, x))
        x = x + len(buttons_dict[i]["label"]) + 5 + spacing
        my_buttons[i].draw()
    cur.mousemask(cur.ALL_MOUSE_EVENTS)

    while running:
        scr.nodelay(True) # don't wait for keyboard input to continue execution
        ch = scr.getch()  # get keyboard input from user
        if ch == cur.KEY_MOUSE:
            event = cur.getmouse()
            bstate = event[4]
            if bstate & cur.BUTTON1_CLICKED:
                x_mouse = event[1]
                y_mouse = event[2]
                for die in dice.dice:
                    die.is_clicked(y_mouse, x_mouse)
                key = None
                for btn in my_buttons:
                    k = btn.is_clicked(y_mouse, x_mouse)
                    if k is not None:
                        key = k
                        break

                if key is not None:
                    ch = ord(key)

        if ch in [ESC, ord('q'), ord('Q')]:  # Quit the program if ESC or 'q' is pressed
            running = False

        # do something useful
        if ch in [ord('r'), ord('R')]:
            dice.roll()

        if ch in  [ord('1'), ord('2'), ord('3'), ord('4'), ord('5')]:
            ind = int(chr(ch))-1
            dice.dice[ind].toggle_hold()

        if ch in [ord('t'), ord('T')]:
            dice.reset()

# Body of App
# curses.wrapper() is a convenience function that calls the main() function and closes the window cleanly
cur.wrapper(main)