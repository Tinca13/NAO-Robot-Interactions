import sys
import gui_utils
from PyQt4 import QtGui
from PyQt4.QtCore import Qt

class Interface(QtGui.QMainWindow):
    def __init__(self, position = (10, 10), size = (1280, 720)):
        super(Interface, self).__init__()
        self.title = "NAO Robot GUI (v0.1)"
        self.NAO_DOCS_URL = "http://doc.aldebaran.com/2-1/home_nao.html"
        # TEMPORARY, MOVE TO OTHER FILE FOR STORAGE
        self.dance_dict = {"thriller": "new_thriller-40424e/new_thriller",
                           "disco": "disco-dd565c/disco",
                           "arm dance": "arm_dance-074ba5/arm_dance",
                           "tai chi": "taichi-cd9975/GangnamStyle",
                           "gangnam style": "gangnam_style-2b4c5b/GangnamStyle (1)"}
        self.behaviour_dict = {"sneeze": "sneezes-4c12b5/Sneezes",
                               "pushups": "pushupsz-cc23cb/pushups",
                               "hello": "hello-bde0d2/blow_kisses",
                               "blow kiss": "blow_kisses-b60c2b/blow_kisses",
                               "air guitar": "air_guitar-f1b1e7/air_guitar"}
        self.init_ui(position, size)

    def init_ui(self, position, size):
        self.setWindowTitle(self.title)
        self.width = size[0]; self.height = size[1]
        self.setGeometry(position[0], position[1], self.width, self.height)
        self.statusBar().showMessage("DEBUG version 0.1 -- NAOqi GUI")
        self.init_menubar()
        self.init_behaviour_frame()
        self.load_joint_sliders()
        self.show()

    def init_menubar(self):
        self.main_menu = self.menuBar()

        self.file_menu = self.main_menu.addMenu("File")
        exit_action = QtGui.QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Z")
        exit_action.setStatusTip("Close the GUI")
        exit_action.triggered.connect(sys.exit)
        self.file_menu.addAction(exit_action)

        self.help_menu = self.main_menu.addMenu("Help")
        load_naoqi_docs = QtGui.QAction("Load NAOqi Help", self)
        load_naoqi_docs.setStatusTip("Loads the online NAOqi documentation")
        load_naoqi_docs.triggered.connect(lambda: gui_utils.load_webpage(self.NAO_DOCS_URL))
        self.help_menu.addAction(load_naoqi_docs)

    def load_joint_sliders(self):
        self.left_right_checkbox = QtGui.QCheckBox("Left", self)
        self.left_right_checkbox.move(self.width/10, self.height/20)
        self.left_right_checkbox.toggled.connect(self.switch_control_side)

        self.r_elbow_roll_slider = QtGui.QSlider(Qt.Horizontal, self)
        self.r_elbow_yaw_slider = QtGui.QSlider(Qt.Horizontal, self)
        self.r_shoulder_roll_slider = QtGui.QSlider(Qt.Horizontal, self)
        self.r_shoulder_yaw_slider = QtGui.QSlider(Qt.Horizontal, self)
        self.r_wrist_yaw_slider = QtGui.QSlider(Qt.Horizontal, self)

        self.l_elbow_roll_slider = QtGui.QSlider(Qt.Horizontal, self)
        self.l_elbow_yaw_slider = QtGui.QSlider(Qt.Horizontal, self)
        self.l_shoulder_roll_slider = QtGui.QSlider(Qt.Horizontal, self)
        self.l_shoulder_yaw_slider = QtGui.QSlider(Qt.Horizontal, self)
        self.l_wrist_yaw_slider = QtGui.QSlider(Qt.Horizontal, self)

        qsliders = {
            "left" : [self.l_elbow_roll_slider, self.l_elbow_yaw_slider, self.l_shoulder_roll_slider,
                    self.l_shoulder_yaw_slider, self.l_wrist_yaw_slider],
            "right" : [self.r_elbow_roll_slider, self.r_elbow_yaw_slider, self.r_shoulder_roll_slider, 
                    self.r_shoulder_yaw_slider, self.r_wrist_yaw_slider]
        }

        for key in qsliders:
            for idx, slider in enumerate(qsliders[key]):
                slider_x_pos = self.width/10
                if key == "right":
                    slider_x_pos = self.width/3
                slider.move(slider_x_pos, (self.height/8)*(idx+1))
                slider.resize(self.width/5, self.height/20)

    def init_buttons(self):
        self.button_list = []
        self.update_buttons(self.behaviour_dict)
        
    def update_buttons(self, current_dict):
        if len(self.button_list) > 0:
            for button in self.button_list:
                button.deleteLater()

        print(current_dict)
        for idx, behaviour in enumerate(current_dict):
            temp_button = QtGui.QPushButton(behaviour, self)
            temp_button.resize(self.width/5, self.height/20)
            temp_button.move(self.width - (self.width / 3), (self.height / 10)*(idx+2))
            self.button_list.append(temp_button)

    def init_behaviour_frame(self):
        self.behaviour_combobox = QtGui.QComboBox(self)
        # TODO: insert behaviour dictionary contents here
        self.behaviour_combobox.addItems(["Behaviours", "Dances"])
        self.behaviour_combobox.currentIndexChanged.connect(self.cb_update)
        # FIXME: dynamic scaling rather than hard coding
        self.behaviour_combobox.resize(self.width/5, self.height/20)
        self.behaviour_combobox.move(self.width - (self.width/3), self.height/10)
        self.init_buttons()

    def load_combobox_elements(self):
        # TODO: allow behaviour dicts to be accessed from everywhere
        pass

    def cb_update(self):
        if self.behaviour_combobox.currentText() == "Behaviours":
            current_dict = self.behaviour_dict
        elif self.behaviour_combobox.currentText() == "Dances":
            current_dict = self.dance_dict
        self.update_buttons(current_dict)
        print("DEBUG: changed index")

    def switch_control_side(self):
        gui_utils.toggle_checkbox_state(self.left_right_checkbox, ["Left", "Right"])

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ex = Interface(position=(50,50))
    sys.exit(app.exec_())