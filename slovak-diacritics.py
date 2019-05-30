import re
import sqlite3
import time
import keyboard
import unidecode
import tkinter
from tkinter import messagebox
from sys import exit

words = ''
found_words = []
equal_sign_press_counter = 0
showWindow = True

# Initialize the main window
window = tkinter.Tk()
window.minsize(400, 300)
window.title("Slovenská Diakritika vs 1.0")
window.wm_iconbitmap("sk.ico")

# Place UI components
labelUpdateTrigger = tkinter.Label(window, text="Zmeniť Spúšťač:")
labelUpdateTrigger.place(x=10, y=10)

trigger = tkinter.Entry(window, width=3)
trigger.place(x=110, y=10)
trigger.insert(0, "=")

labelAddWord = tkinter.Label(window, text="Pridať Slovo:")
labelAddWord.place(x=10, y=30)

addWord = tkinter.Entry(window, width=30)
addWord.place(x=110, y=30)

label3 = tkinter.Label(window, text="Návod na použitie:\nPo napísaní akéhokoľvek Slovenského slova bez diakritiky stačí zadať 'spúšťač'"
                                    "\n(znak ktorý ste si zvolili) a program automaticky doplní mäkčene a dĺžne."
                                    "\nAk ma dané slovo viacero možných vyznamov, tak opakované stláčanie klávesy "
                                    "\n'spúšťača' automaticky prejde cez všetky možnosti."
                                    "\nNapríklad slovo 'stat' môže byť: stáť, sťať, štát atď..."
                                    "\nV prípade že nejaké slovo nie je v databáze, môžete si ho do databázy pridať."
                                    "\nDEMO: https://www.youtube.com/watch?v=ejE9HQi7jcw")
label3.place(x=10, y=90)

label = tkinter.Label(window, text="Posledné nájdene slovo:")
label.place(x=10, y=270)


# Define button press function
def press():
    # set label
    try:
        my_list = [str(addWord.get()).lower(), unidecode.unidecode(str(addWord.get()).lower())]
        DBconnection = sqlite3.connect('sk.db')
        c = DBconnection.cursor()
        c.execute('INSERT INTO "sk_aspell" ("word", "worddf") VALUES (?,?)', my_list)
        DBconnection.commit()
        messagebox.showinfo(title="Databáza",
                            message=f"Slovo '{str(addWord.get()).lower()}' bolo úspešne vložené do databázy")
        print(my_list)
    except:
        messagebox.showinfo(title="Databáza",
                            message=f"Slovo '{str(addWord.get()).lower()}' sa už nachádza v databáze!")


# Place 'Change Label' button on the window
button = tkinter.Button(window, text="Vlož", command=press)
# Place label at coordinates x=10 and y=10 (top right hand corner)
button.place(x=290, y=28)


def on_closing():
    if messagebox.askokcancel("Ukončiť Program", "Chcete ukončiť program?"):
        window.destroy()
        exit()


window.protocol("WM_DELETE_WINDOW", on_closing)


# Function to find the screen dimensions, calculate the center and set geometry
def center(win):
    # Call all pending idle tasks - carry out geometry management and redraw widgets.
    win.update_idletasks()
    # Get width and height of the screen
    width = win.winfo_width()
    height = win.winfo_height()
    # Calculate geometry
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    # Set geometry
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


# Center Window on Screen
center(window)


def db_search_to_list(search_term):
    global found_words
    conn = sqlite3.connect('sk.db')
    cursor = conn.execute("select word from sk_aspell where lower(worddf) = '" + search_term.lower() + "'")
    for row in cursor:
        if search_term[0].isupper():
            found_words.append(str(row[0]).capitalize())
        else:
            found_words.append(str(row[0]))
    if len(found_words) > 1:
        print(found_words)


def place_word(found_word):
    for x in range(len(found_word) + 1):
        keyboard.send('backspace')
    keyboard.write(found_word)


def on_press_reaction(event):
    global words, found_words, equal_sign_press_counter
    if event.name == 'space' or event.name == '.' or event.name == ',' or event.name == ';' or event.name == 'enter':
        words = ''
    elif event.name == 'backspace':
        if len(words) > 0:
            words = words[:-1]
    elif event.name == 'delete':
        found_words = []
    elif event.name == str(trigger.get()):
        if len(str(words)) > 0:
            search = unidecode.unidecode(words)
            found_words = [search]
            equal_sign_press_counter = 1
            db_search_to_list(search)
        words = ''
        if len(found_words) > 1:
            print(str(equal_sign_press_counter) + " - " + found_words[equal_sign_press_counter])
            label.config(text=f"Posledné nájdene slovo: {found_words[equal_sign_press_counter]}")
            place_word(str(found_words[equal_sign_press_counter]))
            equal_sign_press_counter = equal_sign_press_counter + 1
            if equal_sign_press_counter > len(found_words) - 1:
                equal_sign_press_counter = 0
    else:
        # print(event.name)
        if len(str(event.name)) == 1:
            if re.match("^[A-Za-z0-9_-]*$", event.name):
                words = words + str(event.name)


keyboard.on_press(on_press_reaction)

while True:
    if showWindow:
        window.mainloop()
        showWindow = False
    time.sleep(0.01)
    pass
