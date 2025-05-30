import qdarkstyle
from variable import DARKER_PRIMARY_COLOR, DARKEST_PRIMARY_COLOR, PRIMARY_COLOR

qss = f"""
    QPushButton[cssClass="specialButton"] {{ 
        color: #fff;
        background-color: {PRIMARY_COLOR};    
        border-radius: 5px;
    }}
    QPushButton[cssClass="specialButton"]:hover {{
        color: #fff;
        background-color: {DARKER_PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"]:pressed {{
        color: #fff;
        background-color: {DARKEST_PRIMARY_COLOR};
    }}
"""
def setupTheme(app):
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
    app.setStyleSheet(app.styleSheet() + qss)
    