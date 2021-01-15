import sys, os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, QApplication, QDialog
from PyQt5.QtGui import QCursor, QFontMetrics, QIcon
from functools import partial


from logic import *
from model import Options


class Notification(QDialog):
    def __init__(self, message):
        super(Notification, self).__init__()
        uic.loadUi('UI/Notification.ui', self)
        self.message.setText(message)

        self.show()

class PasswordPop(QDialog):
    def __init__(self, parent):
        super(PasswordPop, self).__init__(parent=parent)
        uic.loadUi('UI/PasswordPop.ui', self)

        self.connectEvents()
        self.show()

    def connectEvents(self):
        self.buttonBox.accepted.connect(self.getpswd)
        self.buttonBox.rejected.connect(self.cancel)

    def getpswd(self):
        self.parent().options.passphrase = self.lineEdit.text()
        self.accept()

    def cancel(self):
        self.parent().options.pswdcanceled = True
        self.close()

class TxPop(QDialog):
    def __init__(self, txid):
        super(TxPop, self).__init__()
        uic.loadUi('UI/TxPop.ui', self)

        self.label.setText(txid)
        self.connectEvents()
        self.show()    

    def connectEvents(self):
        self.copy_button.clicked.connect(self.copytoclip)
        self.close_button.clicked.connect(self.accept)

    def copytoclip(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.label.text(), mode=cb.Clipboard)

class About(QDialog):
    def __init__(self):
        super(About, self).__init__()
        uic.loadUi('UI/About.ui', self)

        self.show()

class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('UI/SweeperMainPage.ui', self)

        self.setWindowIcon(QIcon('sweeper.ico'))
        ordering = ['Largest', 'Smallest', 'Label']
        self.order_combobox.addItems(ordering)
        self.options = Options()
        self.connectEvents()

        if not try_conn(self, self.options):
            raise RuntimeError("Can't connect to crownd")

        refresh(self, self.options)

        self.show()

    def connectEvents(self):
        # Connect elements to actions
        # OnClick
        self.sweep_button.clicked.connect(partial(sweep, self, self.options))
        self.new_address_checkbox.clicked.connect(partial(get_checkbox, self.new_address_checkbox, self.options))
        self.upto_checkbox.clicked.connect(partial(get_checkbox, self.upto_checkbox, self.options))
        self.actionAbout.triggered.connect(self.about)
        # OnEditFinished
        self.fee_edit.editingFinished.connect(partial(get_input, self.fee_edit, self.options))
        self.amount_edit.editingFinished.connect(partial(get_input, self.amount_edit, self.options))
        self.to_address_edit.textEdited.connect(partial(get_input, self.to_address_edit, self.options))
        self.to_address_edit.textEdited.connect(self.hideNewCheckbox)
        # OnItemSelection
        self.address_list_widget.itemSelectionChanged.connect(partial(selected_items, self.address_list_widget, self.options))
        self.order_combobox.currentIndexChanged.connect(partial(refresh, self, self.options))
        # OnRightClick
        self.address_list_widget.customContextMenuRequested.connect(self.listItemRightClicked)

    def hideNewCheckbox(self):
        if self.to_address_edit.text() == '':
            self.new_address_checkbox.setVisible(True)
        else:
            self.new_address_checkbox.setVisible(False)

    def listItemRightClicked(self): 
        self.listMenu = QMenu()
        self.actions = [QAction("Copy"), QAction("Set Destination")]
        self.listMenu.addActions(self.actions)
        self.actions[0].triggered.connect(self.actionCopy)
        self.actions[1].triggered.connect(self.actionDest)
        self.listMenu.exec_(QCursor.pos())
        
    def actionCopy(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(str(self.address_list_widget.currentItem().text().split(' ')[0]), mode=cb.Clipboard)
        self.listMenu.close()

    def actionDest(self):
        self.to_address_edit.setText(str(self.address_list_widget.currentItem().text().split(' ')[0]))
        self.options.toaddress = str(self.address_list_widget.currentItem().text().split(' ')[0])
        self.new_address_checkbox.setVisible(False)
        self.listMenu.close()

    def notify(self, message):
        ntf = Notification(message)
        ntf.exec_()

    def pswdask(self):
        ask = PasswordPop(self)
        ask.exec_()

    def showtx(self, txid):
        tx = TxPop(txid)
        tx.exec_()

    def about(self):
        dlg = About()
        dlg.exec_()
