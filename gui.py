from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PyQt5.QtWidgets import (QDialogButtonBox, QDialog, QVBoxLayout, QFormLayout, QLabel, QToolButton, QPushButton, QListWidget, 
    QFileDialog, QFrame, QLineEdit, QCheckBox, QGroupBox, QComboBox, QListWidgetItem, QApplication, QMenu, QAction)
from PyQt5.QtGui import (QFont, QCursor, QIcon)

from logic import *
from model import Options
from functools import partial
import os


class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.options = Options()
        #print("Using %s in %s"%(self.options.conffile, self.options.datadir))
        self.setupUI()
        self.hookElems()
        self.retranslateUI()
        if not try_conn(self, self.options):
            raise RuntimeError("Can't connect to crownd")

        refresh(self, self.options)

        QMetaObject.connectSlotsByName(self)
    
    def hookElems(self):
        # OnClick
        self.sweep_button.clicked.connect(partial(sweep, self, self.options))
        self.new_address_checkbox.clicked.connect(partial(get_checkbox, self.new_address_checkbox, self.options))
        self.upto_checkbox.clicked.connect(partial(get_checkbox, self.upto_checkbox, self.options))
        self.about_button.clicked.connect(self.about)
        # OnEditFinished
        self.fee_edit.editingFinished.connect(partial(get_input, self.fee_edit, self.options))
        self.amount_edit.editingFinished.connect(partial(get_input, self.amount_edit, self.options))
        self.to_address_edit.editingFinished.connect(partial(get_input, self.to_address_edit, self.options))
        self.to_address_edit.editingFinished.connect(self.hideNewCheckbox)
        # OnItemSelection
        self.address_list_widget.itemSelectionChanged.connect(partial(selected_items, self.address_list_widget, self.options))
        self.order_combobox.currentIndexChanged.connect(partial(refresh, self, self.options))
        # OnRightClick
        self.address_list_widget.customContextMenuRequested.connect(self.listItemRightClicked)

    def setupUI(self):
        if not self.objectName():
            self.setObjectName(u"Sweeper")
        self.resize(800, 370)
        self.setFixedSize(800, 370)
        self.setWindowIcon(QIcon('sweeper.ico'))
        # To Address Frame
        self.to_address_frame = QFrame(self)
        self.to_address_frame.setObjectName(u"to_address_frame")
        self.to_address_frame.setGeometry(QRect(450, 20, 341, 61))
        self.to_address_frame.setFrameShape(QFrame.StyledPanel)
        self.to_address_frame.setFrameShadow(QFrame.Raised)
        self.to_address_edit = QLineEdit(self.to_address_frame)
        self.to_address_edit.setObjectName(u"to_address_edit")
        self.to_address_edit.setGeometry(QRect(10, 30, 321, 28))
        self.to_address_label = QLabel(self.to_address_frame)
        self.to_address_label.setObjectName(u"to_address_label")
        self.to_address_label.setGeometry(QRect(10, 10, 81, 16))
        self.to_address_label.setFont(QFont('Cantarell', 10))
        self.new_address_checkbox = QCheckBox(self.to_address_frame)
        self.new_address_checkbox.setObjectName(u"new_address_checkbox")
        self.new_address_checkbox.setGeometry(QRect(250, 10, 81, 24))
        # Amount Frame
        self.amount_frame = QFrame(self)
        self.amount_frame.setObjectName(u"amount_frame")
        self.amount_frame.setGeometry(QRect(450, 80, 341, 61))
        self.amount_frame.setFrameShape(QFrame.StyledPanel)
        self.amount_frame.setFrameShadow(QFrame.Raised)
        self.amount_edit = QLineEdit(self.amount_frame)
        self.amount_edit.setObjectName(u"amount_edit")
        self.amount_edit.setGeometry(QRect(10, 30, 321, 28))
        self.amount_label = QLabel(self.amount_frame)
        self.amount_label.setObjectName(u"amount_label")
        self.amount_label.setGeometry(QRect(10, 10, 71, 16))
        self.amount_label.setFont(QFont('Cantarell', 10))
        self.upto_checkbox = QCheckBox(self.amount_frame)
        self.upto_checkbox.setObjectName(u"upto_checkbox")
        self.upto_checkbox.setGeometry(QRect(250, 10, 81, 21))
        self.upto_checkbox.setChecked(True)
        # Fee Frame
        self.fee_frame = QFrame(self)
        self.fee_frame.setObjectName(u"fee_frame")
        self.fee_frame.setGeometry(QRect(450, 140, 341, 61))
        self.fee_frame.setFrameShape(QFrame.StyledPanel)
        self.fee_frame.setFrameShadow(QFrame.Raised)
        self.fee_edit = QLineEdit(self.fee_frame)
        self.fee_edit.setObjectName(u"fee_edit")
        self.fee_edit.setGeometry(QRect(10, 30, 113, 28))
        self.fee_label = QLabel(self.fee_frame)
        self.fee_label.setObjectName(u"fee_label")
        self.fee_label.setGeometry(QRect(10, 10, 57, 16))
        self.fee_label.setFont(QFont('Cantarell', 10))
        # Sweep Frame
        self.sweep_frame = QFrame(self)
        self.sweep_frame.setObjectName(u"sweep_frame")
        self.sweep_frame.setGeometry(QRect(450, 200, 341, 101))
        self.sweep_frame.setFrameShape(QFrame.StyledPanel)
        self.sweep_frame.setFrameShadow(QFrame.Raised)
        self.sweep_button = QPushButton(self.sweep_frame)
        self.sweep_button.setObjectName(u"sweep_button")
        self.sweep_button.setGeometry(QRect(140, 20, 88, 28))
        # Balance GroupBox
        self.balance_groupbox = QGroupBox(self)
        self.balance_groupbox.setObjectName(u"balance_groupbox")
        self.balance_groupbox.setGeometry(QRect(140, 240, 231, 101))
        self.available_static_label = QLabel(self.balance_groupbox)
        self.available_static_label.setObjectName(u"available_static_label")
        self.available_static_label.setGeometry(QRect(6, 30, 71, 16))
        self.available_static_label.setFont(QFont('Cantarell', 10))
        self.selected_static_label = QLabel(self.balance_groupbox)
        self.selected_static_label.setObjectName(u"selected_static_label")
        self.selected_static_label.setGeometry(QRect(6, 70, 71, 16))
        self.selected_static_label.setFont(QFont('Cantarell', 10))
        self.available_label = QLabel(self.balance_groupbox)
        self.available_label.setObjectName(u"available_label")
        self.available_label.setGeometry(QRect(90, 30, 101, 16))
        self.available_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.available_label.setFont(QFont('Cantarell', 10))
        self.selected_label = QLabel(self.balance_groupbox)
        self.selected_label.setObjectName(u"selected_label")
        self.selected_label.setGeometry(QRect(80, 70, 111, 16))
        self.selected_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.selected_label.setFont(QFont('Cantarell', 10))
        self.crw_label1 = QLabel(self.balance_groupbox)
        self.crw_label1.setObjectName(u"crw_label1")
        self.crw_label1.setGeometry(QRect(200, 30, 31, 16))
        self.crw_label1.setFont(QFont('Cantarell', 10))
        self.crw_label2 = QLabel(self.balance_groupbox)
        self.crw_label2.setObjectName(u"crw_label2")
        self.crw_label2.setGeometry(QRect(200, 70, 31, 16))
        self.crw_label2.setFont(QFont('Cantarell', 10))
        # Order Frame
        self.order_frame = QFrame(self)
        self.order_frame.setObjectName(u"order_frame")
        self.order_frame.setGeometry(QRect(10, 260, 101, 51))
        self.order_frame.setFrameShape(QFrame.StyledPanel)
        self.order_frame.setFrameShadow(QFrame.Raised)
        self.order_combobox = QComboBox(self.order_frame)
        self.order_combobox.setObjectName(u"order_combobox")
        self.order_combobox.setGeometry(QRect(10, 20, 78, 28))
        ordering = ['Largest', 'Smallest', 'Label']
        self.order_combobox.addItems(ordering)
        self.order_label = QLabel(self.order_frame)
        self.order_label.setObjectName(u"order_label")
        self.order_label.setGeometry(QRect(20, 0, 57, 16))
        self.order_label.setFont(QFont('Cantarell', 10))
        # Address List Frame 
        self.address_list_frame = QFrame(self)
        self.address_list_frame.setObjectName(u"address_list_frame")
        self.address_list_frame.setGeometry(QRect(10, 20, 441, 221))
        self.address_list_frame.setFrameShape(QFrame.StyledPanel)
        self.address_list_frame.setFrameShadow(QFrame.Raised)
        self.address_list_widget = QListWidget(self.address_list_frame)
        self.address_list_widget.setSelectionMode(QListWidget.MultiSelection)
        self.address_list_widget.setObjectName(u"address_list_widget")
        self.address_list_widget.setGeometry(QRect(10, 20, 421, 191))
        self.address_list_widget.setFont(QFont('Monospace', 10))
        self.address_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.address_list_address_label = QLabel(self.address_list_frame)
        self.address_list_address_label.setObjectName(u"address_list_address_label")
        self.address_list_address_label.setGeometry(QRect(10, 0, 71, 16))
        self.address_list_address_label.setFont(QFont('Cantarell', 10))
        # About Button
        self.about_button = QPushButton(self)
        self.about_button.setObjectName(u"about_button")
        self.about_button.setGeometry(QRect(690, 340, 88, 21))


    def retranslateUI(self):
        self.setWindowTitle(QCoreApplication.translate("self", u"Crown Sweeper v0.1.0 beta", None))
        self.to_address_label.setText(QCoreApplication.translate("self", u"To Address", None))
        self.amount_label.setText(QCoreApplication.translate("self", u"Amount", None))
        self.amount_edit.setText(QCoreApplication.translate("self", u"0", None))
        self.upto_checkbox.setText(QCoreApplication.translate("self", u"Up To", None))
        self.fee_label.setText(QCoreApplication.translate("self", u"Tx Fee", None))
        self.fee_edit.setText(QCoreApplication.translate("self", u"0.025", None))
        self.new_address_checkbox.setText(QCoreApplication.translate("self", u"New", None))
        self.sweep_button.setText(QCoreApplication.translate("self", u"Sweep", None))
        self.balance_groupbox.setTitle(QCoreApplication.translate("self", u"Balance", None))
        self.available_static_label.setText(QCoreApplication.translate("self", u"Available:", None))
        self.selected_static_label.setText(QCoreApplication.translate("self", u"Selected:", None))
        self.available_label.setText(QCoreApplication.translate("self", u"0", None))
        self.selected_label.setText(QCoreApplication.translate("self", u"0", None))
        self.crw_label1.setText(QCoreApplication.translate("self", u"CRW", None))
        self.crw_label2.setText(QCoreApplication.translate("self", u"CRW", None))
        self.order_label.setText(QCoreApplication.translate("self", u"Order By", None))
        self.address_list_address_label.setText(QCoreApplication.translate("self", u"Address", None))
        self.about_button.setText(QCoreApplication.translate("self", u"About", None))
    
    def hideNewCheckbox(self):
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

class Notification(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setupUI()
        self.retranslateUI(message)

    def setupUI(self):
        if not self.objectName():
            self.setObjectName(u"Notification")
        self.resize(309, 137)
        self.label = QLabel(self)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 20, 251, 51))
        self.label.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.label.setFont(QFont('Cantarell', 10))
        self.pushButton = QPushButton(self)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(110, 90, 88, 28))
        self.pushButton.clicked.connect(self.accept)

    def retranslateUI(self, message):
        self.setWindowTitle(QCoreApplication.translate("self", u"Notification", None))
        self.pushButton.setText(u"Ok")
        self.label.setText(message)

class PasswordPop(QDialog):
    def __init__(self, parent):
        super().__init__(None)
        self.setupUi()
        self.hookElems()
        self.retranslateUi()
        self.parent = parent
        if self.parent.options.pswdcanceled:
            self.parent.options.pswdcanceled = False

    def hookElems(self):
        self.buttonBox.accepted.connect(self.getpswd)
        self.buttonBox.rejected.connect(self.cancel)

    def setupUi(self):
        if not self.objectName():
            self.setObjectName(u"Password")
        self.resize(309, 137)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(70, 90, 171, 31))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(70, 50, 171, 28))
        self.lineEdit.setFrame(True)
        self.lineEdit.setEchoMode(QLineEdit.Password)
        self.label = QLabel(self)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 291, 20))
        self.label.setLayoutDirection(Qt.LeftToRight)
        self.label.setAlignment(Qt.AlignCenter)

        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("self", u"Password", None))
        self.label.setText(QCoreApplication.translate("self", u"Please enter your wallet passphrase:", None))

    def getpswd(self):
        self.parent.options.passphrase = self.lineEdit.text()
        self.accept()

    def cancel(self):
        self.parent.options.pswdcanceled = True
        self.close()

class TxPop(QDialog):
    def __init__(self, txid, parent=None):
        super().__init__(parent)
        self.setupUi()
        self.hookElems()
        self.retranslateUi(txid)

    def hookElems(self):
        self.pushButton.clicked.connect(self.copytoclip)
        self.pushButton_2.clicked.connect(self.accept)

    def setupUi(self):
        if not self.objectName():
            self.setObjectName(u"Tx")
        self.resize(400, 137)
        self.pushButton = QPushButton(self)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(90, 90, 88, 28))
        self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(210, 90, 88, 28))
        self.label = QLabel(self)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(6, 30, 391, 21))
            
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, txid):
        self.setWindowTitle(QCoreApplication.translate("self", u"Tx", None))
        self.label.setText(QCoreApplication.translate("self", u"".join(txid), None))
        self.pushButton.setText(QCoreApplication.translate("self", u"Copy", None))
        self.pushButton_2.setText(QCoreApplication.translate("self", u"Close", None))

    def copytoclip(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.label.text(), mode=cb.Clipboard)

class About(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        self.retranslateUi()
        self.hookElems()

    def hookElems(self):
        self.pushButton.clicked.connect(self.accept)

    def setupUi(self):
        if not self.objectName():
            self.setObjectName(u"About")
        self.setWindowIcon(QIcon('sweeper.ico'))
        self.resize(358, 300)
        self.label = QLabel(self)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 341, 16))
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel(self)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 70, 341, 20))
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_3 = QLabel(self)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 110, 341, 16))
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_4 = QLabel(self)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 170, 341, 16))
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_5 = QLabel(self)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 200, 341, 16))
        self.label_5.setAlignment(Qt.AlignCenter)
        self.pushButton = QPushButton(self)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(140, 250, 88, 28))
        
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("self", u"About", None))
        self.label.setText(QCoreApplication.translate("self", u"Crown Sweeper v0.1.0 beta", None))
        self.label_2.setText(QCoreApplication.translate("self", u"(c) Copyright 2020 The Crown Developers", None))
        self.label_3.setText(QCoreApplication.translate("self", u"Released under the MIT License.", None))
        self.label_4.setText(QCoreApplication.translate("self", u"Sweeper icon based on work by", None))
        self.label_5.setText(QCoreApplication.translate("self", u"Freepik at Flaticon.com", None))
        self.pushButton.setText(QCoreApplication.translate("self", u"Close", None))
