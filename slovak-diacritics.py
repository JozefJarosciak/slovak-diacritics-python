import keyboard
import re

words = '';

def on_press_reaction(event):
    global words
    if event.name == 'space' or event.name == '.' or event.name == ',' or event.name == ';' or event.name == 'enter':
        if len(str(words))>0:
            print(words)
        words = ''
    elif event.name == 'backspace':
        if len(words) > 0:
            words = words[:-1]
    else:
        if len(str(event.name)) == 1:
            if re.match("^[A-Za-z0-9_-]*$", event.name):
                words = words + str(event.name)


keyboard.on_press(on_press_reaction)

while True:
    pass
