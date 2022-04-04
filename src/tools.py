from PyQt6.QtWidgets import QPushButton, QGridLayout
import random
from functools import partial

def get_random_int(min: int, max: int):
    '''min and max are included'''
    return random.randint(min, max)

def create_buttons(icons, iconSize, toolTips, slot=None):
    btnStyleSheet = get_button_stylesheet()
    buttons = [QPushButton(icon, '', None) for icon in icons]
    for button, toolTip in zip(buttons, toolTips):
            button.setCheckable(True)
            button.setChecked(False)
            button.setEnabled(True)
            button.setToolTip(toolTip)
            button.setIconSize(iconSize)
            button.setStyleSheet(btnStyleSheet)
            if slot:
                button.clicked.connect(partial(slot, button))
    return buttons

def create_grid(buttons, columns):
    grid = QGridLayout()
    rows = int(len(buttons) / columns + 1)
    for i in range(rows):
        for j in range(columns):
            index = i * columns + j
            if index >= len(buttons):
                break
            grid.addWidget(buttons[index], i, j)
    return grid

def get_button_stylesheet():
    return """
    QPushButton {background-color: red;}
    QPushButton::checked {background-color: #B0B0B0}
    """
