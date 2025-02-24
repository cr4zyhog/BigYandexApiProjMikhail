import sys

from PyQt6 import uic  # Импортируем uic
from PyQt6.QtGui import QIntValidator, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QSlider
from PyQt6.QtCore import Qt
from io import BytesIO
import requests
from PIL import Image
import os


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('form.ui', self)  # Загружаем дизайн
        self.count_id = 0
        self.delta = 1
        self.delta_coord = 1
        self.initUI()

    def initUI(self):
        only_int = QIntValidator()
        only_int.setRange(-2147483648, 2147483647)

        self.shirota_line.setValidator(only_int)

        self.dolgota_line.setValidator(only_int)

        self.mashtab.setValidator(only_int)

        self.search_button.clicked.connect(self.show_im)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp:
            self.delta -= 0.05
            self.mashtab.setText(str(self.delta))
            self.show_im()
        if event.key() == Qt.Key.Key_PageDown:
            self.delta += 0.05
            self.mashtab.setText(str(self.delta))
            self.show_im()
        if event.key() == Qt.Key.Key_Right:
            self.shirota_line.setText(str(float(self.shirota_line.text()) + (self.delta_coord * self.delta)))
            self.show_im()
        if event.key() == Qt.Key.Key_Left:
            self.shirota_line.setText(str(float(self.shirota_line.text()) - (self.delta_coord * self.delta)))
            self.show_im()
        if event.key() == Qt.Key.Key_Up:
            self.dolgota_line.setText(str(float(self.dolgota_line.text()) + (self.delta_coord * self.delta)))
            self.show_im()
        if event.key() == Qt.Key.Key_Down:
            self.dolgota_line.setText(str(float(self.dolgota_line.text()) - (self.delta_coord * self.delta)))
            self.show_im()

    def show_im(self):
        shirota = self.shirota_line.text()
        dolgota = self.dolgota_line.text()

        delta = str(self.delta)
        apikey = "1254fb15-ad8f-4203-b8c5-131f37c0b498"

        # Собираем параметры для запроса к StaticMapsAPI:
        map_params = {
            "ll": f'{shirota},{dolgota}',
            "spn": ','.join([self.mashtab.text(), self.mashtab.text()]),
            "apikey": apikey,
        }

        map_api_server = "https://static-maps.yandex.ru/v1"
        # ... и выполняем запрос
        response = requests.get(map_api_server, params=map_params)
        fileie = f'map_{self.count_id}.png'
        with open(fileie, 'wb') as file:
            file.write(response.content)
        opened_image = QPixmap(fileie)
        self.karta.setPixmap(opened_image)
        os.remove(fileie)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
