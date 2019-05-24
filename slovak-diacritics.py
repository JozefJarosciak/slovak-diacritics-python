import keyboard
import re
import sqlite3
import unidecode
import pyperclip

words = ''
found_words = []
last_word = ''
offset = 1
right_press_counter = 0


def db_search_to_list(search_term):
    global found_words
    conn = sqlite3.connect('sk.db')
    cursor = conn.execute("select word from sk_aspell where lower(worddf) = '" + search_term.lower() + "'")
    for row in cursor:
        if search_term[0].isupper():
            found_words.append(str(row[0]).capitalize())
        else:
            found_words.append(str(row[0]))
    #print(found_words)


def place_word(found_word):
    for x in range(len(found_word)+1):
        keyboard.press('backspace')
    pyperclip.copy(found_word)
    keyboard.send('ctrl+v')
    keyboard.press(' ')


def on_press_reaction(event):
    global words, found_words, last_word, right_press_counter
    if event.name == 'space' or event.name == '.' or event.name == ',' or event.name == ';' or event.name == 'enter':
        if len(str(words)) > 0:
            search = unidecode.unidecode(words)
            found_words = [search]
            right_press_counter = 1
            db_search_to_list(search)
        words = ''
    elif event.name == 'backspace':
        if len(words) > 0:
            words = words[:-1]
    elif event.name == 'delete':
        found_words = []
    elif event.name == 'right':
        if len(found_words)>1:
            #print(str(right_press_counter) + " - " + found_words[right_press_counter])
            place_word(str(found_words[right_press_counter]))
            right_press_counter = right_press_counter + 1
            #print("Counter: " + str(right_press_counter))
            if right_press_counter > len(found_words)-1:
                right_press_counter = 0
    else:
        #print(event.name)
        if len(str(event.name)) == 1:
            if re.match("^[A-Za-z0-9_-]*$", event.name):
                words = words + str(event.name)
    #conn.close()


keyboard.on_press(on_press_reaction)

while True:
    pass
