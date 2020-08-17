from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PyQt5.QtWidgets import (QDialogButtonBox, QDialog, QVBoxLayout, QFormLayout, QLabel, QToolButton, QPushButton, QListWidget, 
    QFileDialog, QFrame, QLineEdit, QCheckBox, QProgressBar, QGroupBox, QComboBox, QListWidgetItem)

from logic import *
from model import Options
from functools import partial


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
<<<<<<< HEAD
<<<<<<< HEAD

        refresh(self, self.options)
        
=======
=======
>>>>>>> parent of e506851... Attemp to add checkboxes to the address list
        addresses = list()
        spendable_amount = 0
        address_summary = connect(self, self.options)
        if address_summary.items():
            for address,info in address_summary.items():
                addresses.append("%s %.8f %s"%(address, info['total'], info['account']))
                spendable_amount += info['total']

        self.label_5.setText(str(spendable_amount))
        self.listWidget.addItems(addresses)

>>>>>>> parent of e506851... Attemp to add checkboxes to the address list
        QMetaObject.connectSlotsByName(self)
    
    def hookElems(self):
        # OnClick
        self.pushButton.clicked.connect(partial(sweep, self, self.options))
        self.checkBox.clicked.connect(partial(get_checkbox, self.checkBox, self.options))
        self.checkBox_2.clicked.connect(partial(get_checkbox, self.checkBox_2, self.options))
        self.checkBox_3.clicked.connect(partial(get_checkbox, self.checkBox_3, self.options))
        # OnEditFinished
        self.lineEdit_3.editingFinished.connect(partial(get_input, self.lineEdit_3, self.options))
        self.lineEdit_7.editingFinished.connect(partial(get_input, self.lineEdit_7, self.options))
        self.lineEdit_6.editingFinished.connect(partial(get_input, self.lineEdit_6, self.options))
        # OnItemSelection
        self.listWidget.itemSelectionChanged.connect(partial(selected_items, self.listWidget, self.options))

    def setupUI(self):
        if not self.objectName():
            self.setObjectName(u"Dialog")
        self.resize(723, 369)
        # To Address Frame
        self.frame = QFrame(self)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(450, 20, 261, 61))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.lineEdit_6 = QLineEdit(self.frame)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setGeometry(QRect(10, 30, 241, 28))
        self.label_6 = QLabel(self.frame)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(10, 10, 71, 16))
        # Amount Frame
        self.frame_2 = QFrame(self)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(450, 80, 261, 61))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.lineEdit_7 = QLineEdit(self.frame_2)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setGeometry(QRect(10, 30, 241, 28))
        self.label_7 = QLabel(self.frame_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 10, 71, 16))
        self.checkBox_3 = QCheckBox(self.frame_2)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setGeometry(QRect(190, 10, 61, 21))
        # Fee Frame
        self.frame_3 = QFrame(self)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(450, 140, 261, 61))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.lineEdit_3 = QLineEdit(self.frame_3)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(10, 30, 113, 28))
        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 10, 57, 16))
        self.checkBox = QCheckBox(self.frame_3)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(190, 10, 71, 24))
        self.checkBox_2 = QCheckBox(self.frame_3)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setGeometry(QRect(190, 40, 71, 24))
        # Sweep Frame
        self.frame_4 = QFrame(self)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setGeometry(QRect(450, 200, 261, 101))
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.pushButton = QPushButton(self.frame_4)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(90, 20, 88, 28))
        self.progressBar = QProgressBar(self.frame_4)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(50, 70, 172, 23))
        self.progressBar.setValue(24)
        # Balance GroupBox
        self.groupBox = QGroupBox(self)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(140, 240, 161, 101))
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 30, 57, 16))
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 70, 57, 16))
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(70, 30, 51, 16))
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(70, 70, 51, 16))
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(130, 30, 31, 16))
        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(130, 70, 31, 16))
        # Order Frame
        self.frame_5 = QFrame(self)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setGeometry(QRect(10, 260, 101, 51))
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.comboBox = QComboBox(self.frame_5)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(10, 20, 78, 28))
        ordering = ['Newest', 'Oldest', 'Smallest', 'Largest']
        self.comboBox.addItems(ordering)
        self.label_11 = QLabel(self.frame_5)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(20, 0, 57, 16))
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
        self.label_12 = QLabel(self.frame_7)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(10, 0, 51, 16))
        self.label_13 = QLabel(self.frame_7)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(300, 0, 51, 16))
        self.label_14 = QLabel(self.frame_7)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(380, 0, 31, 16))
        # Optional Frame
        self.frame_6 = QFrame(self)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setGeometry(QRect(450, 300, 261, 51))
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)

    def retranslateUI(self):
        self.setWindowTitle(QCoreApplication.translate("self", u"Sweeper", None))
        self.label_6.setText(QCoreApplication.translate("self", u"To Address", None))
        self.label_7.setText(QCoreApplication.translate("self", u"Amount", None))
        self.lineEdit_7.setText(QCoreApplication.translate("self", u"0", None))
        self.checkBox_3.setText(QCoreApplication.translate("self", u"Up To", None))
        self.label_3.setText(QCoreApplication.translate("self", u"Tx Fee", None))
        self.lineEdit_3.setText(QCoreApplication.translate("self", u"0.025", None))
        self.checkBox.setText(QCoreApplication.translate("self", u"Testnet", None))
        self.checkBox_2.setText(QCoreApplication.translate("self", u"Dry Run", None))
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
    
    def notify(self, message):
        ntf = Notification(message)
        ntf.exec_()

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
        self.pushButton = QPushButton(self)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(110, 90, 88, 28))
        self.pushButton.clicked.connect(self.accept)

    def retranslateUI(self, message):
        self.setWindowTitle(QCoreApplication.translate("Notification", u"Notification", None))
        self.pushButton.setText(u"Ok")
        self.label.setText(message)
