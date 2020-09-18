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
        self.pushButton.clicked.connect(partial(sweep, self, self.options))
        self.checkBox.clicked.connect(partial(get_checkbox, self.checkBox, self.options))
        self.checkBox_3.clicked.connect(partial(get_checkbox, self.checkBox_3, self.options))
        self.pushButton_2.clicked.connect(self.about)
        # OnEditFinished
        self.lineEdit_3.editingFinished.connect(partial(get_input, self.lineEdit_3, self.options))
        self.lineEdit_7.editingFinished.connect(partial(get_input, self.lineEdit_7, self.options))
        self.lineEdit_6.editingFinished.connect(partial(get_input, self.lineEdit_6, self.options))
        # OnItemSelection
        self.listWidget.itemSelectionChanged.connect(partial(selected_items, self.listWidget, self.options))
        self.comboBox.currentIndexChanged.connect(partial(refresh, self, self.options))
        # OnRightClick
        self.listWidget.customContextMenuRequested.connect(self.listItemRightClicked)

    def setupUI(self):
        if not self.objectName():
            self.setObjectName(u"Sweeper")
        self.resize(800, 370)
        self.setFixedSize(800, 370)
        repoDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QIcon('sweeper.ico'))
        # To Address Frame
        self.frame = QFrame(self)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(450, 20, 341, 61))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.lineEdit_6 = QLineEdit(self.frame)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setGeometry(QRect(10, 30, 321, 28))
        self.label_6 = QLabel(self.frame)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(10, 10, 81, 16))
        self.label_6.setFont(QFont('Cantarell', 10))
        self.checkBox = QCheckBox(self.frame)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(250, 10, 81, 24))
        # Amount Frame
        self.frame_2 = QFrame(self)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(450, 80, 341, 61))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.lineEdit_7 = QLineEdit(self.frame_2)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setGeometry(QRect(10, 30, 321, 28))
        self.label_7 = QLabel(self.frame_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 10, 71, 16))
        self.label_7.setFont(QFont('Cantarell', 10))
        self.checkBox_3 = QCheckBox(self.frame_2)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setGeometry(QRect(250, 10, 81, 21))
        self.checkBox_3.setChecked(True)
        # Fee Frame
        self.frame_3 = QFrame(self)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(450, 140, 341, 61))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.lineEdit_3 = QLineEdit(self.frame_3)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(10, 30, 113, 28))
        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 10, 57, 16))
        self.label_3.setFont(QFont('Cantarell', 10))
        # Sweep Frame
        self.frame_4 = QFrame(self)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setGeometry(QRect(450, 200, 341, 101))
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.pushButton = QPushButton(self.frame_4)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(140, 20, 88, 28))
        # Balance GroupBox
        self.groupBox = QGroupBox(self)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(140, 240, 231, 101))
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(6, 30, 71, 16))
        self.label_2.setFont(QFont('Cantarell', 10))
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(6, 70, 71, 16))
        self.label.setFont(QFont('Cantarell', 10))
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(90, 30, 101, 16))
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_5.setFont(QFont('Cantarell', 10))
        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(80, 70, 111, 16))
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_8.setFont(QFont('Cantarell', 10))
        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(200, 30, 31, 16))
        self.label_10.setFont(QFont('Cantarell', 10))
        self.label_9 = QLabel(self.groupBox)
        self.label_9.setGeometry(QRect(200, 70, 31, 16))
        self.label_9.setFont(QFont('Cantarell', 10))
        # Order Frame
        self.frame_5 = QFrame(self)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setGeometry(QRect(10, 260, 101, 51))
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.comboBox = QComboBox(self.frame_5)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(10, 20, 78, 28))
        ordering = ['Largest', 'Smallest', 'Label']
        self.comboBox.addItems(ordering)
        self.label_11 = QLabel(self.frame_5)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(20, 0, 57, 16))
        self.label_11.setFont(QFont('Cantarell', 10))
        # Address List Frame 
        self.frame_7 = QFrame(self)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setGeometry(QRect(10, 20, 441, 221))
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.listWidget = QListWidget(self.frame_7)
        self.listWidget.setSelectionMode(QListWidget.MultiSelection)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(10, 20, 421, 191))
        self.listWidget.setFont(QFont('Monospace', 10))
        self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.label_12 = QLabel(self.frame_7)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(10, 0, 71, 16))
        self.label_12.setFont(QFont('Cantarell', 10))
        self.label_13 = QLabel(self.frame_7)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(280, 0, 51, 16))
        self.label_13.setFont(QFont('Cantarell', 10))
        self.label_14 = QLabel(self.frame_7)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(360, 0, 51, 16))
        self.label_14.setFont(QFont('Cantarell', 10))
        # About Button
        self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(690, 340, 88, 21))


    def retranslateUI(self):
        self.setWindowTitle(QCoreApplication.translate("self", u"Crown Sweeper v0.1.0 beta", None))
        self.label_6.setText(QCoreApplication.translate("self", u"To Address", None))
        self.label_7.setText(QCoreApplication.translate("self", u"Amount", None))
        self.lineEdit_7.setText(QCoreApplication.translate("self", u"0", None))
        self.checkBox_3.setText(QCoreApplication.translate("self", u"Up To", None))
        self.label_3.setText(QCoreApplication.translate("self", u"Tx Fee", None))
        self.lineEdit_3.setText(QCoreApplication.translate("self", u"0.025", None))
        self.checkBox.setText(QCoreApplication.translate("self", u"New", None))
        self.pushButton.setText(QCoreApplication.translate("self", u"Sweep", None))
        self.groupBox.setTitle(QCoreApplication.translate("self", u"Balance", None))
        self.label_2.setText(QCoreApplication.translate("self", u"Available:", None))
        self.label.setText(QCoreApplication.translate("self", u"Selected:", None))
        self.label_5.setText(QCoreApplication.translate("self", u"0", None))
        self.label_8.setText(QCoreApplication.translate("self", u"0", None))
        self.label_10.setText(QCoreApplication.translate("self", u"CRW", None))
        self.label_9.setText(QCoreApplication.translate("self", u"CRW", None))
        self.label_11.setText(QCoreApplication.translate("self", u"Order By", None))
        self.label_12.setText(QCoreApplication.translate("self", u"Address", None))
        self.label_13.setText(QCoreApplication.translate("self", u"Amount", None))
        self.label_14.setText(QCoreApplication.translate("self", u"Label", None))
        self.pushButton_2.setText(QCoreApplication.translate("self", u"About", None))
    
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
        cb.setText(str(self.listWidget.currentItem().text().split(' ')[0]), mode=cb.Clipboard)
        self.listMenu.close()

    def actionDest(self):
        self.lineEdit_6.setText(str(self.listWidget.currentItem().text().split(' ')[0]))
        self.options.toaddress = str(self.listWidget.currentItem().text().split(' ')[0])
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
