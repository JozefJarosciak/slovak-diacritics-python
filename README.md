# slovak-diacritics-python
Automaticke pridavanie Slovenskej Diakritiky v texte

More at:
https://www.joe0.com/2019/05/25/automatically-adding-foreign-diacritics-accents-anywhere-in-windows-linux-using-python-with-global-keyboard-hooks-embedded-sqlite-db/

#Installation Windows
- Download: https://github.com/JozefJarosciak/slovak-diacritics-python/raw/master/dist/sk-1.0.rar
- UnRAR the sk-1.0.rar
- Run /sk/sk.exe

#To Deploy Windows Executable:
pyinstaller -y -w -i "C:/code/slovak-diacritics/sk.ico" --add-data "C:/code/slovak-diacritics/sk.db";"." --add-data "C:/code/slovak-diacritics/sk.ico";"." "C:/code/slovak-diacritics/slovak-diacritics.py"

#To Convert UI:
pyuic5 appUI.ui -o appUI.py 