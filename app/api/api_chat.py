from PyQt6.QtWidgets import QListWidget, QLabel, QTextEdit, QPushButton, QWidget, QMessageBox
from PyQt6.QtCore import QTimer
from app.api.api_mensajes import enviarWTS, get_mensaj_chat, get_one_mensaj, update_mensaj_chat
from app.api.chat import Ui_Form

class CustomDialog(QWidget):
    def __init__(self, parent=None):
        super(CustomDialog, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('Chat')
        self.setFixedSize(561, 301)

        self.listado = self.findChild(QListWidget, "listChat")
        self.on_timer_timeout()
        self.listado.itemClicked.connect(self.mostrar_datos)

        self.enviar = self.findChild(QPushButton, "enviar")
        self.enviar.clicked.connect(self.enviar_respuesta)

        self.number_en = self.findChild(QLabel, "nro_re")
        self.number_en.hide()

        self.mensaje_re = self.findChild(QLabel, "mensa_re")
        self.mensaje_re.setWordWrap(True)
        self.mensaje_re.hide()

        self.respuesta = self.findChild(QTextEdit, "respuesta")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_timer_timeout)
        self.timer.start(6000) # Timer triggers every 60000 milliseconds (1 minute)

    def enviar_respuesta(self):
        num = self.number_en.text()
        respuesta = self.respuesta.toPlainText()
        ide, status = enviarWTS(respuesta, num)
        # self.close()

    def on_timer_timeout(self):
        self.listado.clear()
        data, error = get_mensaj_chat()
        if error == None:
            for elemento in data:
                n_tel = elemento['N_TEL']
                id_msj = elemento['ID']
                self.listado.addItem(n_tel + '-' + str(id_msj))

    def mostrar_datos(self, item):
        self.respuesta.clear()
        texto_seleccionado = item.text()
        texto_seleccionado = texto_seleccionado.split('-')
        mensaje, error = get_one_mensaj(int(texto_seleccionado[1]))
        if error == None:
            n_tel = mensaje['N_TEL']
            body = mensaje['BODY']
            self.number_en.setText(n_tel)
            self.number_en.show()
            self.mensaje_re.setText(body)
            self.mensaje_re.show()
            update_mensaj_chat(int(texto_seleccionado[1]))
            self.on_timer_timeout()
