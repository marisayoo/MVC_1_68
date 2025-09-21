import sys
import sys as _sys
_sys.dont_write_bytecode = True

from PyQt5.QtWidgets import QApplication
from View.app import MainWindow
from Controller.controller import Controller

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    controller = Controller(window)
    window.set_controller(controller)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
