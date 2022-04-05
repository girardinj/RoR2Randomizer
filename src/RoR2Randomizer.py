import os
import re
import sys
from functools import partial

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
                             QDialogButtonBox, QFrame, QGridLayout,
                             QHBoxLayout, QLabel, QPushButton, QSpinBox,
                             QStackedLayout, QStyle, QVBoxLayout, QWidget)

import tools

BUTTON_ICON_SIZE = QSize(50, 50)
BUTTON_ICON_BORDER_SIZE = QSize(10, 10)
ICON_FORMAT = '.webp'

class OkDialog(QDialog):
    def __init__(self, title, content, icon, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(icon)
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttonBox.accepted.connect(self.accept)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(content))
        layout.addWidget(buttonBox)

    def accept(self):
        return super().accept()

    @staticmethod
    def critical(widget, text):
        return OkDialog('Error', text, widget.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical))

class AbilityWidget(QWidget):
    def __init__(self, survivor_name, survivor_icon):
        super().__init__()
        self.survivor_name = survivor_name
        self.init_ui()
    
    def init_ui(self):

        layoutMain = QGridLayout(self)
        layoutMain.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.fill_layout(layoutMain)

        self.set_default_values_gui()

    def fill_layout(self, mainLayout):
        
        try:
            with(open(f'icons/abilities/{self.survivor_name}/abilities.txt', 'r')) as f:
                abilities_names = f.read().splitlines()
        except:
            OkDialog.critical(self, f'Missing abilities.txt file for {self.survivor_name}!').exec()
            exit(-1)

        folder_icon_abilities = [x for x in os.listdir(f'icons/abilities/{self.survivor_name}') if x.endswith(ICON_FORMAT)]

        if len(abilities_names) != len(folder_icon_abilities):
            OkDialog.critical(self, f'Missing icons abilities or too much abilities in abilities.txt for {self.survivor_name}!').exec()
            exit(-1)

        abilities = [
            'Primary',
            'Secondary',
            'Utility',
            'Special',
        ]

        # used for some black magic sorcery when the survivor has two misc abilities
        has_two_misc = False
        is_first_misc = True
        if self.survivor_name == 'MUL-T':
            abilities.insert(1, 'Misc')
            abilities_names = abilities_names[:-4] + abilities_names
            has_two_misc = True
        elif self.survivor_name == 'Acrid' or self.survivor_name == 'Railgunner' or self.survivor_name == 'Void Fiend':
            abilities.insert(0, 'Misc')
        elif self.survivor_name == 'Captain':
            abilities.insert(4, 'Misc1')
            abilities.insert(5, 'Misc2')
            abilities_names = abilities_names + abilities_names[-4:] # add the misc abilities to the end of the list a second time
            has_two_misc = True


        self.dict_abilities_buttons = {ability.lower(): [] for ability in abilities}

        for i in range(len(abilities)):
            title = abilities[i]
            mainLayout.addWidget(QLabel(title) , i, 0)
            self.add_to_array(folder_icon_abilities, abilities_names, mainLayout, i, 1, title.lower(), has_two_misc, is_first_misc)
            if has_two_misc:
                if i == 0 and self.survivor_name == 'MUL-T' or i == 4 and self.survivor_name == 'Captain':
                    is_first_misc = False
        

    def get_array(self, abilities, title):
        # we do some sorcery here for the survivors who have two misc abilities
        if self.survivor_name == 'MUL-T' and re.match('^misc', title):
            matcher = '^primary'
        elif re.match('^misc', title):
            matcher = '^misc'
        else:
            matcher = f'^{title}'
        return [ability for ability in abilities if re.match(matcher, ability)]

    def add_to_array(self, folder_icon_abilities, abilities_names, layout, row, column, matcher, has_two_misc = False, is_first_misc = False):
        for item in self.get_array(folder_icon_abilities, matcher):
            name = item.split('.')[0]
            icon = QIcon(f'icons/abilities/{self.survivor_name}/{item}')
            button = QPushButton(icon, '')
            button.setCheckable(True)
            button.setChecked(False)
            button.setEnabled(True)
            button.setIconSize(BUTTON_ICON_SIZE - BUTTON_ICON_BORDER_SIZE) # add border
            button.setFixedSize(BUTTON_ICON_SIZE)
            button.setStyleSheet(tools.get_button_stylesheet())
            button.setToolTip(abilities_names.pop(0))
            # double misc abilities, the return of the sorcery
            
            if re.match('^misc', name):
                if has_two_misc:
                    if is_first_misc:
                        name = 'misc1_'
                    else:
                        name = 'misc2_'
                  
            elif self.survivor_name == 'MUL-T' and re.match('^primary', name):
                if not is_first_misc:
                        name = 'misc_'
            
            self.dict_abilities_buttons[name[:-1]].append(button)
            button.clicked.connect(partial(self.on_button_clicked, name[:-1], button))
            layout.addWidget(button, row, column)
            column += 1

    def set_default_values_gui(self):
        for key, buttons in self.dict_abilities_buttons.items():
            if len(buttons) == 0:
                pass# print(f'missing icon for {key} ability in {self.survivor_name}!')
            else:
                buttons[0].setChecked(True)
                for button in buttons[1:]:
                    button.setChecked(False)

    def on_button_clicked(self, key, sender):
        # isTheOnlyOneChecked is there because
        # you can't have no survivor selected
        isTheOnlyOneChecked = True
        for button in self.dict_abilities_buttons[key]:
            if button != sender and button.isChecked():
                button.setChecked(False)
                isTheOnlyOneChecked = False

        if isTheOnlyOneChecked:
            sender.setChecked(True)

    def randomize_abilities(self):
        for _, buttons in self.dict_abilities_buttons.items():
            if len(buttons) <= 1:
                pass
            else:
                max = len(buttons)
                index = tools.get_random_int(0, max -1)
                for i in range(max):
                    if i == index:
                        buttons[i].setChecked(True)
                    else:
                        buttons[i].setChecked(False)
        
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('RoR2 randomize my game !')
        self.setWindowIcon(QIcon(f'icons/ror2-logo{ICON_FORMAT}'))
        
        self.init_data()
        
        layout = QHBoxLayout(self)
        
        layoutLeft = self.set_left_side()
        layoutRight = self.set_right_side()

        layoutLeft.setContentsMargins(10, 0, 10, 0)
        layoutRight.setContentsMargins(10, 0, 10, 0)

        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.VLine)

        layout.addLayout(layoutLeft)
        layout.addStretch()
        layout.addWidget(frame)
        layout.addStretch()
        layout.addLayout(layoutRight)
        
        self.set_default_values_gui()

    def import_list_and_icons(self, list_name, icons_folder):
        try:
            with open(f'src/{list_name}', 'r') as f:
                list_names = f.read().splitlines()
        except:
            OkDialog.critical(self, f'Missing {list_name}.txt file!').exec()
            exit(-1)

        try:
            icons = []
            for name in list_names:
                icon = QIcon()
                pixmap = QPixmap(f'icons/{icons_folder}/{name}{ICON_FORMAT}')
                icon.addPixmap(pixmap, QIcon.Mode.Normal)
                icon.addPixmap(pixmap, QIcon.Mode.Disabled)
                icons.append(icon)
            # icons = [QIcon(f'icons/{icons_folder}/{name}{ICON_FORMAT}') for name in list_names]
        except:
            OkDialog.critical(self, f'Missing {icons_folder} icons!').exec()
            exit(-1)
        
        if len(list_names) != len(icons):
            OkDialog.critical(self, f'Missing icons or too much things in {list_name}!').exec()
            exit(-1)

        return list_names, icons

    def init_data(self):
        # gamemodes
        self.gamemodes_names, self.gamemodes_icons = self.import_list_and_icons('gamemodes_list.txt', 'gamemodes')
        self.manually_select_gamemode = True
        
        # survivors
        self.survivors_names, self.survivors_icons = self.import_list_and_icons('survivors_list.txt', 'survivors')
        self.manually_select_survivor = False
        
        # artifacts
        self.artifacts_names, self.artifacts_icons = self.import_list_and_icons('artifacts_list.txt', 'artifacts')
        self.manually_select_artifact = True
        
    def set_left_side(self):
        # survivor abilities
        self.cbSurvivorLeft = QComboBox()
        for survivor, icon in zip(self.survivors_names, self.survivors_icons):
            self.cbSurvivorLeft.addItem(icon, survivor) 
        self.cbSurvivorLeft.currentIndexChanged.connect(partial(self.cbSurvivorIndexChanged, self.cbSurvivorLeft))
        
        self.layoutAbilities = QStackedLayout()
        
        for survivor, icon in zip(self.survivors_names, self.survivors_icons):
            self.layoutAbilities.addWidget(AbilityWidget(survivor, icon))
        
        btnRandomizeAbilities = QPushButton('Randomize abilities')
        btnRandomizeAbilities.clicked.connect(self.randomize_abilities)
        layout = QVBoxLayout()
        layout.addWidget(self.cbSurvivorLeft)
        layout.addLayout(self.layoutAbilities)
        layout.addWidget(btnRandomizeAbilities)
        
        return layout
    
    def set_right_side(self):
        
        # gamemode
        self.cbxGamemode = QCheckBox('Manually select game mode')
        self.cbxGamemode.toggled.connect(self.cbxGamemodeToggled)
        
        self.cbGamemode = QComboBox()
        for gamemode, gamemode_icon in zip(self.gamemodes_names, self.gamemodes_icons):
            self.cbGamemode.addItem(gamemode_icon, gamemode)
        # self.cbGamemode.currentIndexChanged.connect(self.cbGamemodeIndexChanged)

        # survivor
        self.cbxSurvivor = QCheckBox('Manually select survivor')
        self.cbxSurvivor.toggled.connect(self.cbxSurvivorToggled)
        
        self.cbSurvivorRight = QComboBox()
        for survivor, icon in zip(self.survivors_names, self.survivors_icons):
            self.cbSurvivorRight.addItem(icon, survivor)
        self.cbSurvivorRight.currentIndexChanged.connect(partial(self.cbSurvivorIndexChanged, self.cbSurvivorRight))
        
        self.survivors_buttons = tools.create_buttons(self.survivors_icons, BUTTON_ICON_SIZE, BUTTON_ICON_BORDER_SIZE, self.survivors_names, self.btnSurvivorToggled)
        gridSurvivor = tools.create_grid(self.survivors_buttons, 8)
        
        # artifact
        self.cbxArtifact = QCheckBox('Manually select artifact')
        self.cbxArtifact.toggled.connect(self.cbxArtifactToggled)
        
        layoutArtifactLuck = QHBoxLayout()
        self.cbArtifactLuck = QComboBox()
        self.cbArtifactLuck.addItems([
            'Uniform luck (1/max for each)',
            'Madness (1/2 for each)',
            'Custom'
        ])
        self.cbArtifactLuck.currentIndexChanged.connect(self.cbArtifactLuckChanged)
        self.sbCustomArtifactLuck = QSpinBox()
        self.sbCustomArtifactLuck.setRange(0, 100)
        
        layoutArtifactLuck.addWidget(self.cbArtifactLuck)
        layoutArtifactLuck.addWidget(self.sbCustomArtifactLuck)
        
        self.artifacts_buttons = tools.create_buttons(self.artifacts_icons, BUTTON_ICON_SIZE, BUTTON_ICON_BORDER_SIZE, self.artifacts_names)
        gridArtifact = tools.create_grid(self.artifacts_buttons, 4)
        
        # start button
        btnRandomizeGame = QPushButton('Let\'s randomize !')
        btnRandomizeGame.clicked.connect(self.randomize_game)
        
        # layout
        layoutChoices = QHBoxLayout()
        
        # layout gamemode
        layoutGamemode = QVBoxLayout()
        layoutGamemode.setAlignment(Qt.AlignmentFlag.AlignTop)
        layoutGamemode.addWidget(self.cbxGamemode)
        layoutGamemode.addWidget(self.cbGamemode)
        layoutChoices.addLayout(layoutGamemode)

        layoutChoices.addSpacing(10)

        # layout survivor
        layoutSurvivor = QVBoxLayout()
        layoutSurvivor.setAlignment(Qt.AlignmentFlag.AlignTop)
        layoutSurvivor.addWidget(self.cbxSurvivor)
        layoutSurvivor.addWidget(self.cbSurvivorRight)
        layoutSurvivor.addLayout(gridSurvivor)
        layoutChoices.addLayout(layoutSurvivor)
        
        layoutChoices.addSpacing(10)

        # layout artifact
        layoutArtifact = QVBoxLayout()
        layoutArtifact.setAlignment(Qt.AlignmentFlag.AlignTop)
        layoutArtifact.addWidget(self.cbxArtifact)
        layoutArtifact.addLayout(layoutArtifactLuck)
        layoutArtifact.addLayout(gridArtifact)
        layoutChoices.addLayout(layoutArtifact)
        
    
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addLayout(layoutChoices)
        layout.addWidget(btnRandomizeGame)
                
        
        return layout

    def set_default_values_gui(self):
        
        # default options
        self.cbGamemode.setCurrentIndex(0)
        self.cbxGamemode.setChecked(self.manually_select_gamemode)
        self.cbxGamemodeToggled(self.manually_select_gamemode)
        
        survivor_index = 0
        self.survivors_buttons[survivor_index].click()
        self.cbxSurvivor.setChecked(self.manually_select_survivor)
        self.cbxSurvivorToggled(self.manually_select_survivor)
        
        self.cbArtifactLuck.setCurrentIndex(0)
        self.sbCustomArtifactLuck.setVisible(False)
        self.cbxArtifact.setChecked(self.manually_select_artifact)
        self.cbxArtifactToggled(self.manually_select_artifact)

    # better when it is always visible
    # def cbGamemodeIndexChanged(self, index):
    #     visible = index == 0
    #     self.cbxArtifact.setVisible(visible)
    #     self.cbArtifactLuck.setVisible(visible)
    #     for btn in self.artifacts_buttons:
    #         btn.setVisible(visible)

    def cbxGamemodeToggled(self, checked):
        self.manually_select_gamemode = checked
        self.cbGamemode.setEnabled(checked)

    def cbSurvivorIndexChanged(self, sender, index):
        self.survivors_buttons[index].click()
        self.layoutAbilities.setCurrentIndex(index)
        if sender == self.cbSurvivorLeft:
            self.cbSurvivorRight.setCurrentIndex(index)
        elif sender == self.cbSurvivorRight:
            self.cbSurvivorLeft.setCurrentIndex(index)
        else:
            raise 'how did you get there ?'

    def cbxSurvivorToggled(self, checked):
        self.manually_select_survivor = checked
        self.cbSurvivorLeft.setEnabled(checked)
        self.cbSurvivorRight.setEnabled(checked)
        for button in self.survivors_buttons:
            button.setEnabled(checked)
    
    def btnSurvivorToggled(self, btn, checked):
        # isTheOnlyOneChecked is there because
        # you can't have no survivor selected
        i = 0
        isTheOnlyOneChecked = True
        for button in self.survivors_buttons:
            if button == btn:
                self.cbSurvivorRight.setCurrentIndex(i)
            elif button.isChecked():
                button.setChecked(False)
                isTheOnlyOneChecked = False
            i += 1
        
        if isTheOnlyOneChecked:
            btn.setChecked(True)
    
    def cbxArtifactToggled(self, checked):
        self.manually_select_artifact = checked
        self.cbArtifactLuck.setEnabled(not checked)
        self.sbCustomArtifactLuck.setEnabled(not checked)
        for button in self.artifacts_buttons:
            button.setEnabled(checked)

    def cbArtifactLuckChanged(self, index):
        '''
        index:
        0 => Uniform luck (1/max for each)
        1 => Madness (1/2 for each)
        2 => Custom
        '''
        if index == 2:
            self.sbCustomArtifactLuck.setVisible(True)
        else:
            self.sbCustomArtifactLuck.setVisible(False)
    
    def randomize_game(self):
        if not self.manually_select_gamemode:
            max = self.cbGamemode.count()
            gamemode_index = tools.get_random_int(0, max - 1)
            self.cbGamemode.setCurrentIndex(gamemode_index)
            
        if not self.manually_select_survivor:
            max = len(self.survivors_buttons)
            survivor_index = tools.get_random_int(0, max - 1)
            self.cbxSurvivorToggled(True)
            self.survivors_buttons[survivor_index].click()
            self.cbxSurvivorToggled(False)
            
        if not self.manually_select_artifact:
            # we draw a random number between 0 and 100, and we use it to select each artifact
            # ex. we got 54% chance of it to activate
            # random.randint(0, 99) < 54 ? activate : don't activate
            btn_to_activate = []
            luck_mode = self.cbArtifactLuck.currentIndex()
            # index:
            # 0 => Uniform luck (1/max for each)
            # 1 => Madness (1/2 for each)
            # 2 => Custom
            self.cbxArtifactToggled(True)
            if luck_mode == 0:
                max = len(self.artifacts_buttons)
            elif luck_mode == 1:
                max = 50
            elif luck_mode == 2:
                max = self.sbCustomArtifactLuck.value()
            else:
                raise 'Implement luck mode %d' % luck_mode
            
            for i in range(len(self.artifacts_buttons)):
                activate = tools.get_random_int(0, 99) < max
                if activate:
                    btn_to_activate.append(i)
            self.cbxArtifactToggled(False)
            
            for i in range(len(self.artifacts_buttons)):
                self.artifacts_buttons[i].setChecked(i in btn_to_activate)

    def randomize_abilities(self):
        self.layoutAbilities.currentWidget().randomize_abilities()

def main():
    app = QApplication(sys.argv)
    
    main_window = MainWindow()
    main_window.show()
    
    sys.exit(app.exec())

main()
