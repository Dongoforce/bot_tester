import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QComboBox, QMessageBox, QFileDialog, \
    QTableWidget, QTableWidgetItem, QDateTimeEdit, QTextEdit
from PyQt5.QtGui import QIcon, QPixmap
from  PyQt5.QtCore import QDateTime
from bot_controller import *
from xls_parser import *
from _datetime import datetime
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Nike bot'
        self.left = 600
        self.top = 300
        self.width = 670
        self.height = 480
        self.all_extensions = ["xlsx", "xlsm", "xlsb", "xls", "xlam"]
        self.browser = "firefox"
        self.my_threads = []
        self.current_date = ''
        self.data = []
        self.initUI()
        # req_proxy = RequestProxy()
        # self.proxies = req_proxy.get_proxy_list()
        # # self.rus_proxies = []
        # for proxy in self.proxies:
        #     if proxy.country == 'Russian Federation':
        #         print(proxy.country)
        #         self.rus_proxies.append(proxy)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)

        # Create widget
        label = QLabel(self)

        self.lable_file = QLabel(self)
        self.lable_file.setStyleSheet("background-color:red;")
        self.lable_file.setText("File is not uploaded")
        self.lable_file.setGeometry(470, 30, 135, 30)

        self.button_file = QPushButton(self)
        self.button_file.setStyleSheet("background-color:#301b28;color:#ddc5a2;")
        self.button_file.setGeometry(470, 60, 135, 40)
        self.button_file.setText("Brows file")
        self.button_file.clicked.connect(lambda: self.openFileNameDialog())

        self.button_start = QPushButton(self)
        self.button_start.setGeometry(470, 250, 135, 40)
        self.button_start.setText("Start")
        self.button_start.setStyleSheet("background-color:#301b28;color:#ddc5a2;")
        self.button_start.clicked.connect(lambda: self.create_threads(self.browser, self.data))
        self.button_start.setDisabled(True)

        self.button_close = QPushButton(self)
        self.button_close.setStyleSheet("background-color:#301b28;color:#ddc5a2;")
        self.button_close.setGeometry(470, 290, 135, 40)
        self.button_close.setText("Close")
        self.button_close.clicked.connect(lambda: self.close_browsers())

        self.label_brows = QLabel(self)
        self.label_brows.setGeometry(470, 120, 135, 30)
        self.label_brows.setStyleSheet("color:#301b28;")
        self.label_brows.setText("Choose browser:")

        self.combo = QComboBox(self)
        self.combo.addItems(["firefox", "chrome", "opera"])
        self.combo.setGeometry(470, 150, 135, 40)
        self.combo.setStyleSheet("background-color:#301b28;color:#ddc5a2;")
        self.combo.activated[str].connect(self.setBrowser)

        self.table = QTableWidget(self)
        self.table.setGeometry(0, 0, 450, 400)
        self.table.setStyleSheet("background-color:#301b28;color:#ddc5a2;")
        self.table.setColumnCount(7)
        self.table.setRowCount(1)
        self.table.setItem(0, 0, QTableWidgetItem("Login"))
        self.table.setItem(0, 1, QTableWidgetItem("Password"))
        self.table.setItem(0, 2, QTableWidgetItem("Middle name"))
        self.table.setItem(0, 3, QTableWidgetItem("Card number"))
        self.table.setItem(0, 4, QTableWidgetItem("Date"))
        self.table.setItem(0, 5, QTableWidgetItem("Cvv"))
        self.table.setItem(0, 6, QTableWidgetItem("Url"))

        self.date_field = QDateTimeEdit(self)
        self.date_field.setGeometry(470, 350, 165, 40)
        self.date_field.setStyleSheet("background-color:#301b28;color:#ddc5a2;")
        self.date_field.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.date_field.setMinimumDateTime(QDateTime.currentDateTime())

        self.url = QTextEdit(self)
        self.url.setGeometry(10, 430, 400, 30)
        self.url.setStyleSheet("background-color:#301b28;color:#ddc5a2;")

        self.url_text = QLabel(self)
        self.url_text.setGeometry(10, 400, 400, 30)
        self.url_text.setStyleSheet("color:#301b28;")
        self.url_text.setText("Url:")

        self.button_url = QPushButton(self)
        self.button_url.setStyleSheet("background-color:#301b28;color:#ddc5a2;")
        self.button_url.setGeometry(410, 430, 100, 30)
        self.button_url.setText("ADD")
        self.button_url.clicked.connect(lambda: self.add_url())

        self.usr_text = QLabel(self)
        self.usr_text.setGeometry(520, 430, 80, 30)
        self.usr_text.setStyleSheet("color:#301b28;")
        self.usr_text.setText("User count:")

        self.users = QTextEdit(self)
        self.users.setGeometry(600, 430, 40, 30)
        self.users.setStyleSheet("background-color:#301b28;color:#ddc5a2;")

        pixmap = QPixmap('static/back.jpeg').scaled(self.width, self.height)
        label.setPixmap(pixmap)

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "", options=options)
        extension = fileName.split(".")[-1]

        if fileName and extension in self.all_extensions:
            self.start(fileName)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setStyleSheet("background-color:#301b28;color:#ddc5a2;")
            msg.setText("Wrong file format!")
            msg.setInformativeText('Only excel file format')
            msg.setWindowTitle("Error")
            msg.exec_()

    def setBrowser(self, browser):
        self.browser = browser

    def start(self, name):
        self.lable_file.setStyleSheet("background-color:green;")
        self.lable_file.setText("    File is uploaded")
        self.data = pars_xls(name)
        if self.data != "Wrong header params, should be:  Login, Password, Middle_name, Card_number, Date, Cvv":
            self.table.setRowCount(len(self.data))
            self.user_count = len(self.data) - 1
            self.users.setText(str(self.user_count))
            self.fill_table()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setStyleSheet("background-color:#301b28;color:#ddc5a2;")
            msg.setText("Wrong file format!")
            msg.setInformativeText(
                "Wrong header params, should be:  Login, Password, Middle_name, Card_number, Date, Cvv")
            msg.setWindowTitle("Error")
            msg.exec_()

    def fill_table(self):
        self.table.setItem(0, 0, QTableWidgetItem("Login"))
        self.table.setItem(0, 1, QTableWidgetItem("Password"))
        self.table.setItem(0, 2, QTableWidgetItem("Middle name"))
        self.table.setItem(0, 3, QTableWidgetItem("Card number"))
        self.table.setItem(0, 4, QTableWidgetItem("Date"))
        self.table.setItem(0, 5, QTableWidgetItem("Cvv"))
        self.table.setItem(0, 6, QTableWidgetItem("Url"))
        for i in range(len(self.data) - 1):
            for j in range(len(self.data[i])):
                self.table.setItem(i + 1, j, QTableWidgetItem(self.data[i][j]))

    def create_threads(self, browser, data):
        self.button_start.setDisabled(True)
        k = len(self.my_threads)
        self.user_count = int(self.users.toPlainText())
        drop_time = int(datetime.fromisoformat(self.date_field.dateTime().toString("yyyy-MM-dd HH:mm:ss")).timestamp())

        for i in data:
            # proxy = self.rus_proxies[k].get_address()
            self.my_threads.append(
                bot_on_thread(url=i[6], browser=browser, login=i[0], password=i[1], middle_name=i[2], cardNumber=i[3],
                              cardExpiry=i[4], cardCvc=i[5], drop_time=drop_time))
            self.my_threads[k].start()
            k += 1

            if k == self.user_count:
                break

    def close_browsers(self):
        for i in self.my_threads:
            try:
                i.close_browser()
            except:
                del i
                continue
            del i
        self.my_threads = []
        self.button_start.setDisabled(False)

    def add_url(self):
        if len(self.data) != 0:
            for i in range(len(self.data)):
                self.data[i].append(self.url.toPlainText())
                self.table.setItem(i + 1, 6, QTableWidgetItem(self.url.toPlainText()))
            self.button_start.setDisabled(False)
            print(self.data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
