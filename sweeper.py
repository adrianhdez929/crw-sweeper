import sys
from PyQt5.QtWidgets import QApplication
from gui import Ui


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui()
    app.exec_()
