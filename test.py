
a = [1,2,3, 'hi\nbye']
x='{} {} {} {}'


#print(' '.join(x.format(*k) for k in a))

#print(x.format(*a))


import curses

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

print(x.format(*a))

curses.nocbreak()
stdscr.keypad(False)
curses.echo()

curses.endwin()