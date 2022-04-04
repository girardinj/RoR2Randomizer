import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QWidget, QComboBox, QCheckBox, QPushButton, QSpinBox
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QStackedLayout
from PyQt6.QtGui import QIcon

from functools import partial

import tools

class AbilityWidget(QWidget):
    def __init__(self, survivor_name, survivor_icon):
        super().__init__()
        self.init_ui(survivor_name, survivor_icon)
    
    def init_ui(self, survivor_name, survivor_icon):
        
        layoutsAbilities = [
            QHBoxLayout(), # main
            QHBoxLayout(), # secondary
            QHBoxLayout(), # utility
            QHBoxLayout(), # special
        ]
        
        layout = QVBoxLayout(self)
        layout.addWidget(btn)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('RoR2 randomize my game !')
        
        self.init_data()
        
        layout = QHBoxLayout(self)
        
        layoutLeft = self.set_left_side()
        layoutRight = self.set_right_side()
        
        layout.addLayout(layoutLeft)
        layout.addLayout(layoutRight)
        
        self.set_default_values_gui()

    def init_data(self):
        # gamemodes
        self.gamemodes_names = [
            'Normal',
            'Eclipse',
            'Simulacrum'
        ]
        self.gamemodes_icons = [QIcon(f'icons/gamemodes/{gamemode}.png') for gamemode in self.gamemodes_names]
        self.manually_select_gamemode = True
        
        # survivors
        self.survivors_names = [
            'Commando',
            'Huntress',
            'Bandit',
            'MUL-T',
            'Engineer',
            'Artificer',
            'Mercenary',
            'REX',
            'Loader',
            'Captain',
            'Acrid',
            'Raigunner',
            'Void Fiend',
        ]
        self.survivors_icons = [QIcon(f'icons/survivors/{survivor}.png') for survivor in self.survivors_names]
        self.manually_select_survivor = False
        
        # artifacts
        self.artifacts_names = [
            'None',
            'Chaos',
            'Command',
            'Death',
            'Dissonance',
            'Enigma',
            'Evolution',
            'Frailty',
            'Glass',
            'Honor',
            'Kin',
            'Metamorphosis',
            'Sacrifice',
            'Soul',
            'Spite',
            'Swarms',
            'Vengeance',
        ]
        self.artifacts_icons = [QIcon(f'icons/artifacts/{artifact}.png') for artifact in self.artifacts_names]
        self.manually_select_artifact = True
        
    def set_left_side(self):
        # survivor        
        self.cbSurvivorLeft = QComboBox()
        for survivor, icon in zip(self.survivors_names, self.survivors_icons):
            self.cbSurvivorLeft.addItem(icon, survivor) 
        self.cbSurvivorLeft.currentIndexChanged.connect(partial(self.cbSurvivorIndexChanged, self.cbSurvivorLeft))
        
        self.layoutAbilities = QStackedLayout()
        
        for survivor, icon in zip(self.survivors_names, self.survivors_icons):
            self.layoutAbilities.addWidget(AbilityWidget(survivor, icon))
        
        btnRandomizeAbilities = QPushButton('Randomize abilities')
        
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

        # survivor
        self.cbxSurvivor = QCheckBox('Manually select survivor')
        self.cbxSurvivor.toggled.connect(self.cbxSurvivorToggled)
        
        self.cbSurvivorRight = QComboBox()
        for survivor, icon in zip(self.survivors_names, self.survivors_icons):
            self.cbSurvivorRight.addItem(icon, survivor)
        self.cbSurvivorRight.currentIndexChanged.connect(partial(self.cbSurvivorIndexChanged, self.cbSurvivorRight))
        
        self.survivors_buttons = tools.create_buttons(self.survivors_icons, QSize(30, 30), self.survivors_names, self.btnSurvivorToggled)
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
        
        self.artifacts_buttons = tools.create_buttons(self.artifacts_icons, QSize(30, 30), self.artifacts_names)
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
        
        # layout survivor
        layoutSurvivor = QVBoxLayout()
        layoutSurvivor.setAlignment(Qt.AlignmentFlag.AlignTop)
        layoutSurvivor.addWidget(self.cbxSurvivor)
        layoutSurvivor.addWidget(self.cbSurvivorRight)
        layoutSurvivor.addLayout(gridSurvivor)
        layoutChoices.addLayout(layoutSurvivor)
        
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
        # isTheOnlyOneChecked are there because
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
                    
            

def main():
    app = QApplication(sys.argv)
    
    main_window = MainWindow()
    main_window.show()
    
    sys.exit(app.exec())

main()
