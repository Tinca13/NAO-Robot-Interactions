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
        self.load_joint_sliders()
        self.init_labels()
        self.init_behaviour_frame()
        self.show()

    def init_menubar(self):
        self.main_menu = self.menuBar()

        self.file_menu = self.main_menu.addMenu("File")

        load_gui_action = QtGui.QAction("Load Camera GUI", self)
        load_gui_action.setShortcut("Ctrl+T")
        load_gui_action.setStatusTip("Loads the camera Interface")
        load_gui_action.triggered.connect(self.load_camera_gui)

        exit_action = QtGui.QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Z")
        exit_action.setStatusTip("Close the GUI")
        exit_action.triggered.connect(sys.exit)

        self.file_menu.addAction(load_gui_action)
        self.file_menu.addAction(exit_action)

        self.help_menu = self.main_menu.addMenu("Help")
        load_naoqi_docs = QtGui.QAction("Load NAOqi Help", self)
        load_naoqi_docs.setStatusTip("Loads the online NAOqi documentation")
        load_naoqi_docs.triggered.connect(lambda: gui_utils.load_webpage(self.NAO_DOCS_URL))
        self.help_menu.addAction(load_naoqi_docs)

    def init_labels(self):
        left_label = QtGui.QLabel("Left", self)
        left_label.move(self.width/10, self.height/16)
        left_label.resize(self.width/5, self.height/20)
        left_label.setStyleSheet("background-color: rgb(135,206,250)")
        left_label.setAlignment(Qt.AlignCenter)

        right_label = QtGui.QLabel("Right", self)
        right_label.move(self.width/3, self.height/16)
        right_label.resize(self.width/5, self.height/20)
        right_label.setStyleSheet("background-color: rgb(255,255,224)")
        right_label.setAlignment(Qt.AlignCenter)

    def load_joint_sliders(self):
        # To add more sliders, add an entry to the respective dictionary
        self.qsliders = {
            "left" : [
                {"name" : "Left Elbow Roll", 
                "QSlider" : None, "QLabel" : None,
                "min" : -88.5, "max" : -2, "start" : -45},
                {"name" : "Left Elbow Yaw", 
                "QSlider" : None, "QLabel" : None,
                "min" : -119.5, "max" : 119.5, "start" : 0},
                {"name" : "Left Shoulder Roll", 
                "QSlider" : None, "QLabel" : None,
                "min" : -18, "max" : 76, "start" : 0},
                {"name" : "Left Shoulder Pitch", 
                "QSlider" : None, "QLabel" : None,
                "min" : -119.5, "max" : 119.5, "start" : 0},
                {"name" : "Left Wrist Yaw", 
                "QSlider" : None, "QLabel" : None,
                "min" : -104.5, "max" : 104.5, "start" : 0}
            ],
            "right" : [
                {"name" : "Right Elbow Roll", 
                "QSlider" : None, "QLabel" : None,
                "min" : 2, "max" : 88.5, "start" : 43},
                {"name" : "Right Elbow Yaw", 
                "QSlider" : None, "QLabel" : None,
                "min" : -119.5, "max" : 119.5, "start" : 0},
                {"name" : "Right Shoulder Roll", 
                "QSlider" : None, "QLabel" : None,
                "min" : -76, "max" : 18, "start" : 0},
                {"name" : "Right Shoulder Pitch", 
                "QSlider" : None, "QLabel" : None,
                "min" : -119.5, "max" : 119.5, "start" : 0},
                {"name" : "Right Wrist Yaw", 
                "QSlider" : None, "QLabel" : None,
                "min" : -104.5, "max" : 104.5, "start" : 0}
            ]
        }

        for key in self.qsliders:
            for idx, slider_dict in enumerate(self.qsliders[key]):
                self.set_sliders(idx, slider_dict, key)     

    def set_sliders(self, idx, slider_dict, key):
        slider_dict["QSlider"] = QtGui.QSlider(Qt.Horizontal, self)
        slider = slider_dict["QSlider"]
        x_pos = self.width/10

        if key == "right":
            x_pos = self.width/3

        slider.move(x_pos, (self.height/8)*(idx+1))
        slider.resize(self.width/5, self.height/20)
        slider.setMinimum(slider_dict["min"])
        slider.setMaximum(slider_dict["max"])
        slider.setValue(slider_dict["start"])
        slider.setTickPosition(QtGui.QSlider.TicksBelow)
        # FIXME: change calculation since it causes issues with combined negative and positive values
        tick_interval = (slider_dict["min"] - slider_dict["max"]) / 10
        slider.setTickInterval(round(tick_interval))

        slider_dict["QLabel"] = QtGui.QLabel("", self)
        label = slider_dict["QLabel"]
        label.setText("{} : {}".format(slider_dict["name"], slider_dict["start"]))
        label.move(x_pos+(self.width/15), (self.height/8)*(idx+1)+30)
        label.resize(self.width/5, self.height/20)

    def init_buttons(self):
        self.head_lock_button = QtGui.QPushButton("Toggle Head Lock", self)
        self.head_lock_button.move(self.width/10, self.height - (self.height/10))
        self.head_lock_button.resize(self.width/5, self.height/20)
        self.head_lock_button.clicked.connect(self.toggle_head_lock)
        self.head_lock_label = QtGui.QLabel("Head status: Unlocked", self)
        self.head_lock_label.move(self.width/3, self.height - (self.height/10))
        self.head_lock_label.resize(self.width/5, self.height/20)
        self.head_lock_label.setAlignment(Qt.AlignCenter)
        # red 240,128,128
        self.head_lock_label.setStyleSheet("background-color: rgb(204,255,204)")

        self.button_list = []
        self.current_dict = self.behaviour_dict
        self.update_buttons()
    
    def update_buttons(self):
        for button in self.button_list:
            button.deleteLater()

        self.button_list = []
        for idx, behaviour in enumerate(self.current_dict):
            temp_button = QtGui.QPushButton(behaviour, self)
            temp_button.resize(self.width/5, self.height/20)
            temp_button.move(self.width - (self.width / 3), (self.height / 10)*(idx+2))
            temp_button.show()
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

    def load_camera_gui(self):
        print("DEBUG: loading camera GUI not implemented yet")

    def cb_update(self):
        if self.behaviour_combobox.currentText() == "Behaviours":
            self.current_dict = self.behaviour_dict
        elif self.behaviour_combobox.currentText() == "Dances":
            self.current_dict = self.dance_dict
        print(self.current_dict)
        self.update_buttons()
        print("DEBUG: changed index")

    def toggle_head_lock(self):
        # TODO: add robot API toggle head lock code here
        button = QtGui.QPushButton("test", self)
        button.move(100, 100)
        button.resize(100, 30)
        gui_utils.toggle_label_status(self.head_lock_label, 
                                    ("Head status: Unlocked", "Head status: Locked"),
                                    ("(204,255,204)", "(240,128,128)"))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ex = Interface(position=(50,50))
    sys.exit(app.exec_())