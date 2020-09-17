import sys
from PyQt5.QtWidgets import QApplication, QDialog
from gui import Dialog, Notification


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = Dialog()
    dlg.show()    
    sys.exit(app.exec_())
