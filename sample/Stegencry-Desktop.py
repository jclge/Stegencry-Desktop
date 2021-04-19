from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout, QCheckBox, QDialog, QInputDialog, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QFile, QIODevice, QTextStream, pyqtSignal
from PyQt5.QtGui import QCursor
from Stegencry import encrypt, decrypt
from sys import argv

class DialogCustom(QDialog):
    def __init__(self):
        super(DialogCustom, self).__init__()
        uic.loadUi('dialog_custom.ui', self)
        self.__init_main_variables()
        self.__link_checkboxes()

    def __init_main_variables(self):
        self.__steg = True
        self.__rgb = False
        self.__enc = True

    def get_elements(self):
        return (self.__enc, self.__rgb, self.__steg)

    def __link_checkboxes(self):
        self.checkBox.stateChanged.connect(self.__stegano_changed)
        self.checkBox_2.stateChanged.connect(self.__rgb_changed)
        self.checkBox_3.stateChanged.connect(self.__enc_changed)

    def __rgb_changed(self):
        if (self.checkBox_2.isChecked() == False):
            self.__rgb = False
            self.checkBox.setEnabled(True)
        else:
            self.__rgb = True
            self.checkBox.setEnabled(False)

    def __stegano_changed(self):
        if (self.checkBox.isChecked() == False):
            self.__steg = False
            self.checkBox_2.setEnabled(True)
        else:
            self.__steg = True
            self.checkBox_2.setEnabled(False)

    def __enc_changed(self):
        if (self.checkBox_3.isChecked() == False):
            self.__enc = False
        else:
            self.__enc = True

class StegencryDesktop(QMainWindow):
    def __init__(self):
        super(StegencryDesktop, self).__init__()
        uic.loadUi('stegencrydesktop.ui', self)
        self.__define_main_elements()
        self.__set_image()
        self.__init_labels()
        self.__set_labels()
        self.__set_dialog_custom()
        self.__link_buttons()
        self.__link_actions()
        self.__define_stylesheet()
        self.show()

    def __init_labels(self):
        self.encryption_label.setAlignment(Qt.AlignCenter)

    def __define_stylesheet(self):
        stream = QFile("Stegencry.qss")
        stream.open(QIODevice.ReadOnly)
        self.setStyleSheet(QTextStream(stream).readAll())

    def __define_main_elements(self):
        self.__slave = None
        self.__key = None
        self.__enc = None
        self.__path = "image.png"

    def __link_buttons(self):
        self.__link_image_buttons()
        self.__link_enc_buttons()

    def __link_actions(self):
        self.__link_file_actions()
        self.__link_key_actions()
        self.__link_custom_actions()

    def __custom(self):
        self.__dialog.exec_()

    def __link_custom_actions(self):
        self.actionCustom_Dialog.triggered.connect(self.__custom)

    def __link_key_actions(self):
        self.actionSet_Key_2.triggered.connect(self.__set_key)

    def __set_key(self):
        i, okPressed = QInputDialog.getText(self, "Set the key / password", "Enter key here:")
        if (okPressed):
            self.__key = i
            return (True)
        else:
            return (False)

    def __link_enc_buttons(self):
        self.encrypt_button.clicked.connect(self.__encrypt)
        self.encrypt_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.decrypt_button.clicked.connect(self.__decrypt)
        self.decrypt_button.setCursor(QCursor(Qt.PointingHandCursor))

    def __process_encrypt(self, elements):
        if (elements[0] == True):
            self.__enc.shuffle_pixels()
        if (elements[1] == True):
            self.__enc.encrypt_rgb()
        if (elements[2] == True):
            self.__enc.steganography()

    def __encrypt(self):
        self.__enc = encrypt()
        self.__enc.set_master(self.__path)
        if (self.__manage_missing_elements() == False):
            return
        self.__process_encrypt(self.__dialog.get_elements())
        self.__enc.set_output("res.png")
        self.__enc.save_image()
        self.__path = ("res.png")
        self.__set_image()
        self.__set_labels()

    def __manage_missing_elements(self):
        if (self.__slave != None):
            self.__enc.set_slave(self.__slave)
        if (self.__key == None and self.__set_key()):
            self.__enc.set_key(self.__key)
            return (True)
        elif (self.__key != None):
            self.__enc.set_key(self.__key)
            return (True)
        else:
            return False

    def __process_decrypt(self, elements):
        if (elements[2] == True):
            self.__enc.steganography()
        if (elements[1] == True):
            self.__enc.decrypt_rgb()
        if (elements[0] == True):
            self.__enc.unshuffle_pixels()

    def __decrypt(self):
        self.__enc = decrypt()
        self.__enc.set_master(self.__path)
        if (self.__manage_missing_elements() == False):
            return
        self.__process_decrypt(self.__dialog.get_elements())
        self.__enc.set_output("res.png")
        self.__enc.save_image()
        self.__path = ("res.png")
        self.__set_image()
        self.__set_labels()

    def __open_slave(self):
        browse = QFileDialog().getOpenFileName()
        if (browse[0] != ''):
            self.__slave = browse[0]

    def __save(self):
        name = QFileDialog.getSaveFileName(self, 'Save File', '', '*.jpg *.png *.jpeg')
        self.__enc.set_output(name[0])
        self.__enc.save_image()

    def __link_file_actions(self):
        self.actionOpen_Image.triggered.connect(self.__open)
        self.actionReset.triggered.connect(self.__reset)
        self.actionSave.triggered.connect(self.__save)
        self.actionOpen_Child.triggered.connect(self.__open_slave)

    def __reset(self):
        self.__path = "image.png"
        self.__set_image()
        self.__set_labels()
        del self.__dialog
        self.__set_dialog_custom()

    def __set_dialog_custom(self):
        self.__dialog = DialogCustom()

    def __link_image_buttons(self):
        self.add_image_encryption.setCursor(QCursor(Qt.PointingHandCursor))
        self.add_image_encryption.clicked.connect(self.__open)

    def __set_labels(self):
        self.encryption_label.setPixmap(self.__image)

    def __open(self):
        browse = QFileDialog().getOpenFileName()
        if (browse[0] != ''):
            self.__path = browse[0]
            self.__set_image()
            self.__set_labels()

    def __set_image(self):
        self.__image = QPixmap(self.__path)
        self.__image = self.__image.scaledToHeight(591)

app = QApplication(argv)
window = StegencryDesktop()
app.exec_()