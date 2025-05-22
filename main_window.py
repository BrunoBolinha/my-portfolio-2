from PySide6.QtWidgets import (QMessageBox, QMainWindow, QVBoxLayout, QWidget)

class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        #Layout basico
        self.cw = QWidget()
        self.vLayout = QVBoxLayout()
        self.cw.setLayout(self.vLayout)

        #Titulo janela
        self.setCentralWidget(self.cw)
        self.setWindowTitle('Calculadora')


        #Ajuste final
        
    def adjustFixedSize(self):
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def addWidgetToVLayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)
        
    def makeMsgBox(self):
        return QMessageBox(self)