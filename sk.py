from appUI import *
import sys
import re
import sqlite3
import time
import keyboard
import unidecode

words = ''
found_words = []
equal_sign_press_counter = 0
showWindow = True

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)


# Define button press function
def press():
    # set label
    try:
        my_list = [ui.textEdit_2.toPlainText().lower(), unidecode.unidecode(ui.textEdit_2.toPlainText().lower())]
        print(my_list)
        db_connection = sqlite3.connect('sk.db')
        c = db_connection.cursor()
        c.execute('INSERT INTO "sk_aspell" ("word", "worddf") VALUES (?,?)', my_list)
        db_connection.commit()
        db_connection.close()
        ui.statusbar.showMessage(f"Slovo '{str(ui.textEdit_2.toPlainText()).lower()}' bolo úspešne vložené do databázy", 5000)
    except Exception:
        ui.statusbar.showMessage(f"Slovo '{str(ui.textEdit_2.toPlainText()).lower()}' sa už nachádza v databáze!", 5000)


ui.pushButton.clicked.connect(press)


def db_search_to_list(search_term):
    global found_words
    conn = sqlite3.connect('sk.db')
    cursor = conn.execute("select word from sk_aspell where lower(worddf) = '" + search_term.lower() + "'")
    for row in cursor:
        if search_term[0].isupper():
            found_words.append(str(row[0]).capitalize())
        else:
            found_words.append(str(row[0]))
    conn.close()
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
    elif event.name == str(ui.textEdit.toPlainText()):
        if len(str(words)) > 0:
            search = unidecode.unidecode(words)
            found_words = [search]
            equal_sign_press_counter = 1
            db_search_to_list(search)
        words = ''
        if len(found_words) > 1:
            print(str(equal_sign_press_counter) + " - " + found_words[equal_sign_press_counter])
            # ui.statusbar.showMessage("d")
            ui.statusbar.showMessage(f"Posledné nájdene slovo: {found_words[equal_sign_press_counter]}", 5000)
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
        showWindow = False
        MainWindow.show()
        sys.exit(app.exec_())
    time.sleep(0.01)
    pass




