from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
from variable import BUTTON_FONT_SIZE
from utils import isNumOrDot, isEmpty, isValidNumber, convertToNumber
from display import Display
from typing import TYPE_CHECKING
import math

if TYPE_CHECKING:    
    from display import Display
    from info import Info
    from main_window import MainWindow

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(BUTTON_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(60, 60)

class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', info: 'Info',window: 'MainWindow',*args, **kwargs):
        super().__init__(*args, **kwargs)

        self._grid_mask = [
            ["C", "D", "P", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["N", "0", ".", "="],
        ]

        self.display = display
        self.info = info
        self.window = window
        self._equation = ''
        self._equationInitialValue = 'Sua conta: '
        self._left = None
        self._right = None
        self.op = None
        
        self.equation = self._equationInitialValue
        self._makeGrid()
        

    @property
    def equation(self):
        return self._equation
    
    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def vouApagarVoce(self, text):
        print(456)

    def _makeGrid(self):
        
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self.display.backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._configLeftOp)


        for rowNumber, rowData in enumerate(self._grid_mask):
            for columnNumber, buttonText in enumerate(rowData):
                button = Button(buttonText)
                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    self.configSpecialButton(button)

                self.addWidget(button,rowNumber,columnNumber)
                slot = self._makeSlot(self._insertToDisplay, buttonText)
                self._connectButtonClicked(button, slot)
    
    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    def configSpecialButton(self, button):
        text = button.text()

        if text == 'C':
            self._connectButtonClicked(button, self._clear)

        if text in '+-/*':
            self._connectButtonClicked(
                button, 
                self._makeSlot(self._configLeftOp, text)
            )

        if text == 'P':
            self._connectButtonClicked(
                button, 
                self._makeSlot(self._configLeftOp, '^')
            )
        
        if text == '=':
            self._connectButtonClicked(button, self._eq)

        if text == 'N':
            self._connectButtonClicked(button, self._invertNumber)

        if text == 'D':
            self._connectButtonClicked(button, self.display.backspace)

    @Slot()
    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot
    
    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            return

        number = convertToNumber(displayText) * -1

        self.display.setText(str(number))

    @Slot()
    def _insertToDisplay(self, text):
        newDisplayValue = self.display.text() + text
        
        if not isValidNumber(newDisplayValue):  
            return
    
        self.display.insert(text)

    @Slot()
    def _clear(self):
        self._left = None
        self._right = None
        self.op = None
        self.equation = self._equationInitialValue
        self.display.clear()

    @Slot()
    def _configLeftOp(self, text):
        displayText = self.display.text()
        self.display.clear()

        if not isValidNumber(displayText) and self._left is None:
            self._showError('Você não digitou nada.')
            return
        
        if self._left is None:
            self._left = convertToNumber(displayText)

        self._op = text
        self.equation = f'{self._left} {self._op} ??'

    @Slot()
    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            self._showError('Sem nada para a direita')
            return
            
        self._right = float(displayText)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'error'
            
        try:
            if '^' in self.equation and isinstance(self._left, int | float):
                result = math.pow(self._left, self._right)
                result = convertToNumber(str(result))
            else:
                result = eval(self.equation)

        except ZeroDivisionError:
            self._showError('Divisão por 0')        
        except OverflowError:
            self._showError('Número muito grande')  

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._right = None
        self._left = result
        
        if result != 'error':
            self._left = None

    def _makeDialog(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        return msgBox

    def _showError(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()
    def _showInfo(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()
