import keyboard
import re
import sqlite3
import unidecode

words = ''


def on_press_reaction(event):
    global words
    conn = sqlite3.connect('sk.db')
    if event.name == 'space' or event.name == '.' or event.name == ',' or event.name == ';' or event.name == 'enter':
        if len(str(words))>0:
            search = unidecode.unidecode(words)
            cursor = conn.execute("select distinct(word) from sk_aspell where length(word)>2 AND lower(worddf)<>lower(word) AND lower(worddf) = '"+search.lower()+"' limit 1")
            for row in cursor:
                found_word = row[0]
                if search[0].isupper():
                    found_word = str(found_word).capitalize()
            print(words + ": " + found_word)
        words = ''
    elif event.name == 'backspace':
        if len(words) > 0:
            words = words[:-1]
    else:
        if len(str(event.name)) == 1:
            if re.match("^[A-Za-z0-9_-]*$", event.name):
                words = words + str(event.name)
    conn.close()


keyboard.on_press(on_press_reaction)

while True:
    pass

