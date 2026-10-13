import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
import time


# options menu that allows the user to pick what they want to do
def to_do_options(stdscr):
    # sets up the keybord function/input
    curses.cbreak()
    stdscr.keypad(True)
    # option to be printed
    options = ["View list","Add task","Delete task","End program"]
    count = 0
    counter = 0
    # loop that prints and takes the input of the user
    while True:
        stdscr.clear()
        stdscr.refresh()
        stdscr.addstr("~Options: To Do List~")
        # loop that prints out options in order and with brackets
        while counter < len(options):
            stdscr.addstr(counter + 1, 1,options[counter])
            if count == counter:
                stdscr.addstr(counter + 1, 0,"[")
                stdscr.addstr(counter + 1, len(options[count]) + 2,"]")
            counter += 1
        counter = 0
        key = stdscr.getch()
        # takes input of user to select and move the brackets
        if key == curses.KEY_UP:
            count -= 1
        elif key == curses.KEY_DOWN:
            count += 1
        if count < 0:
            count = 3
        elif count > 3:
            count = 0
        # Ends function
        elif key == 10:
            stdscr.clear()
            stdscr.refresh()
            return count
            break


# Views the list with all the tasks and allows the user to check them off
def to_do_view_list(stdscr, list, completed):
    # sets up the keybord function/input
    curses.cbreak()
    stdscr.keypad(True)
    # option to be printed
    count = 0
    counter = 0
    # loop that prints and takes the input of the user
    while True:
        if len(list) <= 0:
            stdscr.addstr("No List Here")
            stdscr.getkey()
            break
        stdscr.clear()
        stdscr.refresh()
        stdscr.addstr("~To Do List~     (Space key to exit)")
        # loop that prints out list in order and with brackets (adjusting for size of text)
        while counter < len(list):
            stdscr.addstr(counter + 1, 1,list[counter])
            if count in completed:
                complete = "✓"
            else:
                complete = "!"
            # Prints brackets and check marks
            if count == counter:
                stdscr.addstr(counter + 1, 0,"[")
                stdscr.addstr(counter + 1, len(list[count]) + 2,"]")
                stdscr.addstr(counter + 1, len(list[count]) + 5,"[")
                stdscr.addstr(counter + 1, len(list[count]) + 6, complete)
                stdscr.addstr(counter + 1, len(list[count]) + 7, "]")
            counter += 1
        counter = 0
        key = stdscr.getch()
        # takes input of user to select
        if key == curses.KEY_UP:
            count -= 1
        elif key == curses.KEY_DOWN:
            count += 1
        if count < 0:
            count = len(list) - 1
        elif count > len(list) - 1:
            count = 0
        # Allows the user to check off their tasks
        if key == 10 and not(count in completed):
            completed.append(count)
        elif key == 10:
            completed.remove(count)
        # Ends function
        if key == ord(" "):
            return completed
            break


# Function that ends the textbox
def exit_on_enter(ch):
    if ch == 10:
        return 7
    return ch
# Function that adds tasks to the list
def to_do_add_task(stdscr, list):
    stdscr.addstr(1, 0,"~Write a New Task to Add~     (Enter to exit)")
    # Makes a window and truns it into a textbox
    win = curses.newwin(4 , 38, 4, 4)
    user_text = Textbox(win)
    # Draws a rectangle around the textbox
    rectangle(stdscr, 3, 3, 8, 42)
    stdscr.refresh()
    # Allows the user to edit the textbox
    user_text.edit(exit_on_enter)
    task = user_text.gather().strip().replace("\n", "")
    stdscr.clear()
    stdscr.refresh()
    stdscr.addstr("Added Task...")
    stdscr.getkey()
    if task == "":
        return list
    else:
        list.append(task)
        return list


# Allows user to delete tasks form the list
def to_do_delete_task(stdscr, list):
    # sets up the keybord function/input
        curses.cbreak()
        stdscr.keypad(True)
        # Sets up variables
        count = 0
        counter = 0
        # loop that prints and takes the input of the user
        while True:
            # Ends the function if thier is nothing in the list
            if len(list) <= 0:
                stdscr.addstr("No List Here")
                stdscr.getkey()
                return 0.1
                break
            stdscr.clear()
            stdscr.refresh()
            stdscr.addstr("~To Do List - Delete~     (Enter to exit)")
            # loop that prints out list in order and with brackets (adjusting for size of text)
            while counter < len(list):
                stdscr.addstr(counter + 1, 1,list[counter])
                # Prints brackets around the task
                if count == counter:
                    stdscr.addstr(counter + 1, 0,"[")
                    stdscr.addstr(counter + 1, len(list[count]) + 2,"]")
                counter += 1
            counter = 0
            key = stdscr.getch()
            # takes input of user to select
            if key == curses.KEY_UP:
                count -= 1
            elif key == curses.KEY_DOWN:
                count += 1
            if count < 0:
                count = len(list) - 1
            elif count > len(list) - 1:
                count = 0
            # deletes the task when the user presses enter
            if key == 10:
                return count


# Allows the program to switch between different functions
def to_do_list():
    # Main list
    list = []
    completed = []
    while True:
        # Options menu
        count = curses.wrapper(to_do_options)
        # Views list
        if count == 0:
            completed = curses.wrapper(to_do_view_list, list, completed)
        # Adds task to the list
        elif count == 1:
            list = curses.wrapper(to_do_add_task, list)
        # Deletes task form the list
        elif count == 2:
            counting = curses.wrapper(to_do_delete_task, list)
            if counting == int:
                list.remove(list[counting])
                if counting in completed:
                    completed.remove(counting)
        # Closes the whole program
        elif count == 3:
            print("~Closing Program - Bye!!~")
            time.sleep(3)
            break

to_do_list()