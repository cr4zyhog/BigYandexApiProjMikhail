import sys

from PyQt6 import uic  # Импортируем uic
from PyQt6.QtGui import QIntValidator, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QSlider
from io import BytesIO
import requests
from PIL import Image
import os


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('form.ui', self)  # Загружаем дизайн
        self.count_id = 0
        self.initUI()

    def initUI(self):
        only_int = QIntValidator()
        only_int.setRange(-2147483648, 2147483647)

        self.shirota_line.setValidator(only_int)

        self.dolgota_line.setValidator(only_int)

        self.horizontalSlider.setTickInterval(300)

        self.search_button.clicked.connect(self.show_im)

        self.horizontalSlider.sliderReleased.connect(self.show_im)

    def show_im(self):
        shirota = self.shirota_line.text()
        dolgota = self.dolgota_line.text()

        delta = str(3 - self.horizontalSlider.value() / 100)
        # apikey = "1254fb15-ad8f-4203-b8c5-131f37c0b498"
        apikey = '5815d7d2-6bbe-424d-a32d-028b8c596fa2'

        # Собираем параметры для запроса к StaticMapsAPI:
        map_params = {
            "ll": f'{shirota},{dolgota}',
            "spn": ",".join([delta, delta]),
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
