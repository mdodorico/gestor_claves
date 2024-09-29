import sys
from PyQt6.QtWidgets import QApplication
from gui.interface import PasswordManager

def main():
    app = QApplication(sys.argv)
    window = PasswordManager()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
