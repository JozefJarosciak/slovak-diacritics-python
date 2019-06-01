# Slovenská Diakritika pre Windows a Linux
Automatické pridávanie diakritiky do Slovenského textu naprogramované v Python programovacom jazyku.

- Viacej informácii: https://www.joe0.com/2019/05/25/automatically-adding-foreign-diacritics-accents-anywhere-in-windows-linux-using-python-with-global-keyboard-hooks-embedded-sqlite-db/

# Inštalácia pod Windows

- Download: https://github.com/JozefJarosciak/slovak-diacritics-python/raw/master/dist/sk-1.0.rar
- UnRAR sk-1.0.rar
- Spusti /sk/sk.exe


# Inštalácia pod Linux
Na Ubuntu:
- Nainštaluj Python 3.7.x, Pip3, Git-core
- Potom v home directory, klonuj repo: git clone https://github.com/JozefJarosciak/slovak-diacritics-python.git
- Kolektni v konzole:
  * pip3 install pyqt5
  * pip3 install keyboard
  * pip3 install unidecode
  
- Potom choď do directory kde je uložený spúšťací script sk.py
- Spusti program v konzole: sudo python3 slovak-diacritics.py

# To Deploy Windows Executable:
- pyinstaller -y -w -i "C:/code/slovak-diacritics/sk.ico" --add-data "C:/code/slovak-diacritics/sk.db";"." --add-data "C:/code/slovak-diacritics/sk.ico";"." "C:/code/slovak-diacritics/sk.py"

# To Convert UI:
- pyuic5 appUI.ui -o appUI.py 