import sys

from buttons import ButtonsGrid
from main_window import MainWindow
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from variable import WINDOW_ICON_PATH
from display import Display
from info import Info
from styles import setupTheme

if __name__ == '__main__':

    #Cria aplicação
    app = QApplication(sys.argv)
    setupTheme(app)
    window = MainWindow()
    
    #Icone
    icon = QIcon(str(WINDOW_ICON_PATH))                  
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)    

    #Info
    info = Info('Sua conta: ')
    window.addWidgetToVLayout(info)

    display = Display()
    window.addWidgetToVLayout(display)    

    #Grid   
    buttonsGrid = ButtonsGrid(display, info, window)
    window.vLayout.addLayout(buttonsGrid)
    

    #Executar
    window.adjustFixedSize()
    window.show()

    app.exec()