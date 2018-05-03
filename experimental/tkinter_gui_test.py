#from Tkinter import *
import Tkinter as tk
import time
import webbrowser
from PIL import Image, ImageTk
#commented for testing as requires almath and alproxy
from movement import Movement

class Window(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.is_standing = True
        # can change ip if required, port must not be changed
        self.move = Movement("169.254.141.183", 9559)
        self.labels = []
        self.init_window()

    def init_window(self):
        self.master.title("Robot GUI")
        self.pack(fill=tk.BOTH, expand=1)
        self.init_menu()
        self.init_buttons()
        self.init_left_sliders()
        self.init_right_sliders()
        self.init_labels()
        self.init_hands()
        self.init_head_sliders()

    def init_menu(self):
        # initialises the menu of the window
        main_menu = tk.Menu(self.master)
        # parameter menu is set as the instance of the main_menu
        self.master.config(menu=main_menu)

        file = tk.Menu(main_menu)
        # label is how the command will appear, the command is the programmatic action taken
        file.add_command(label='Exit', command=self.master.quit)
        main_menu.add_cascade(label='File', menu=file)

        '''edit = tk.Menu(main_menu)
        edit.add_command(label='Show image', command=self.show_image)
        main_menu.add_cascade(label='Edit', menu=edit)'''

        help = tk.Menu(main_menu)
        help.add_command(label='Joint Help', command=self.show_slider_help)
        help.add_command(label='Preset Methods', command=self.show_presets)
        main_menu.add_cascade(label='Help', menu=help)

        presets = tk.Menu(main_menu)
        presets.add_command(label='Show Preset Methods', command=self.open_presets)
        main_menu.add_cascade(label='Presets', menu=presets)

    def init_buttons(self):
        #TODO: place buttons at correct coordinates
        btn_quit = tk.Button(self.master, text="quit", command=self.master.quit)
        btn_quit.place(x=0, y=0)

        btn_lock = tk.Button(self.master, text="Lock head", command=self.move.lock_head)
        btn_lock.place(x=100, y=0)

        btn_release = tk.Button(self.master, text="Release head", command=self.move.release_head)
        btn_release.place(x=200, y=0)
        #btn_reset = tk.Button(self.master, text="Reset", command=self.move.toggle_autonomous_movement)
        #btn_reset.place(x=300, y=0)

        # btn_walk = Button(self, text="walk", command=self.move.walk())
        # btn_walk.place(x=0, y=0)

    def init_left_sliders(self):
        #TODO: alter commands to match relevant function from movement class
        #angle sliders for joints, limited to valid rotation ranges
        elbow_slider_yaw = tk.Scale(self.master, orient='horizontal', from_=-119, to=119, command=self.move.left_elbow_yaw)
        elbow_slider_yaw.place(x=0, y=100)
        elbow_slider_roll = tk.Scale(self.master, orient='horizontal', from_=-88, to=0, command=self.move.left_elbow_roll)
        elbow_slider_roll.place(x=0, y=200)

        shoulder_slider_roll = tk.Scale(self.master, orient='horizontal', from_=-18, to=76, command=self.move.left_shoulder_roll)
        shoulder_slider_roll.place(x=0, y=300)
        shoulder_slider_pitch = tk.Scale(self.master, orient='horizontal', from_=-119, to=119, command=self.move.left_shoulder_pitch)
        shoulder_slider_pitch.set(75)
        shoulder_slider_pitch.place(x=0, y=400)

        wrist_slider_yaw = tk.Scale(self.master, orient='horizontal', from_=-104, to=104, command=self.move.left_wrist_yaw)
        wrist_slider_yaw.place(x=0, y=500)
        pass

    def init_right_sliders(self):
        # TODO: alter commands to match relevant function from movement class
        # angle sliders for joints, limited to valid rotation ranges
        elbow_slider_yaw = tk.Scale(self.master, orient='horizontal', from_=-119, to=119, command=self.move.right_elbow_yaw)
        elbow_slider_yaw.place(x=200, y=100)
        elbow_slider_roll = tk.Scale(self.master, orient='horizontal', from_=0, to=88, command=self.move.right_elbow_roll)
        elbow_slider_roll.place(x=200, y=200)

        shoulder_slider_roll = tk.Scale(self.master, orient='horizontal', from_=-76, to=18, command=self.move.right_shoulder_roll)
        shoulder_slider_roll.place(x=200, y=300)
        shoulder_slider_pitch = tk.Scale(self.master, orient='horizontal', from_=-119, to=119, command=self.move.right_shoulder_pitch)
        shoulder_slider_pitch.set(75)
        shoulder_slider_pitch.place(x=200, y=400)

        wrist_slider_yaw = tk.Scale(self.master, orient='horizontal', from_=-104, to=104, command=self.move.right_wrist_yaw)
        wrist_slider_yaw.place(x=200, y=500)
        pass

    def init_head_sliders(self):
        head_slider_yaw = tk.Scale(self.master, orient='horizontal', from_=-119, to=119, command=self.move.head_swivel)
        head_slider_yaw.place(x=400, y=100)
        head_slider_pitch = tk.Scale(self.master, orient='horizontal', from_=-38, to=29, command=self.move.head_up_down)
        head_slider_pitch.place(x=400, y=200)
        pass

    def init_hands(self):
        right_hand_slider = tk.Scale(self.master, orient='horizontal', from_=0, to=50, command=self.move.right_hand_move)
        right_hand_slider.place(x=400, y=300)

        left_hand_slider = tk.Scale(self.master, orient='horizontal', from_=0, to=50, command=self.move.left_hand_move)
        left_hand_slider.place(x=400, y=400)
        pass

    def init_labels(self):
        joint_angle_names = ['Left Elbow Yaw', 'Left Elbow Roll', 'Left Shoulder Roll', 'Left Shoulder Pitch',
                             'Left Wrist Yaw', 'Right Elbow Yaw', 'Right Elbow Roll', 'Right Shoulder Roll',
                             'Right Shoulder Pitch', 'Right Wrist Yaw', 'Head Yaw', 'Head Pitch', 'Right Hand',
                             'Left Hand']
        y_counter_l = 80
        y_counter_r = 80
        y_counter_m = 80
        count = 0
        for joint_name in joint_angle_names:
            print("count {} joint {}".format(count, joint_name))
            print("start of label loop")
            label = tk.Label(self.master, text=joint_name)
            if count <= 4:
                print("placing left labels")
                label.place(x=0, y=y_counter_l)
                y_counter_l += 100
            elif count > 4 and count <= 9:
                print("placing middle labels")
                label.place(x=200, y=y_counter_m)
                y_counter_m += 100
            else:
                print("placing right labels")
                label.place(x=400, y=y_counter_r)
                y_counter_r += 100
            count += 1
            self.labels.append(label)
        pass

    def print_slider_value(self, val):
        print(val)
        pass

    def show_image(self):
        # TODO: get the image showing, try different loading method
        image_blue = Image.open('F:/Pictures/013.jpg')
        render = ImageTk.PhotoImage(image_blue)
        load_image_blue = Label(self, image=render)
        load_image_blue.place(x=20, y=20)
        pass

    def show_slider_help(self):
        top_level = tk.Toplevel()
        slider_label = tk.Label(top_level, text="Each of the labelled sliders can be changed to\n"
                                                " manipulate the joints of the robot.\nMove the re"
                                                "levant slider to control where it moves!\n"
                                                "Follow this link to see what each type of movement"
                                                "does:", height=5, width=50)
        hyperlink_label = tk.Label(top_level, text=r"http://doc.aldebaran.com/2-1/family/robots/joints_robot.html",
                                   fg="blue", cursor="hand2", height=2, width=50)
        slider_label.pack()
        hyperlink_label.pack()
        hyperlink_label.bind("<Button-1>", self.open_browser)
        pass

    def show_presets(self):
        top_level = tk.Toplevel()
        preset_label = tk.Label(top_level, text="There are several preset methods that can be\n"
                                                "run using the 'presets' drop-down in the main menu.\n"
                                                "There are several presets available including:\n"
                                                "-Walk\n-Wave\n-Sit\n-Stand\n-Lying Back\n"
                                                "-Lying Belly\n-Crouch", height=12, width=50)
        preset_label.pack()
        pass

    def open_presets(self):
        # TODO: add relevant commands to the buttons from movement class and toggle autonomous movement
        #self.move.toggle_autonomous_movement()
        top_level = tk.Toplevel()
        top_level.geometry("200x210")
        btn_walk_fw = tk.Button(top_level, text="Walk Forwards", command=self.move.walk_fw_set)
        btn_walk_fw.config(height=1, width=30)
        btn_walk_bk = tk.Button(top_level, text="Walk Backwards", command=self.move.walk_bk_set)
        btn_walk_bk.config(height=1, width=30)
        btn_wave = tk.Button(top_level, text="Wave", command=self.move.right_wave_start)
        btn_wave.config(height=1, width=30)
        btn_sit = tk.Button(top_level, text="Sit/Stand", command=self.stand_toggle)
        btn_sit.config(height=1, width=30)
        btn_lying_back = tk.Button(top_level, text="Lying Back", command=self.move.lying_back)
        btn_lying_back.config(height=1, width=30)
        btn_lying_belly = tk.Button(top_level, text="Lying Belly", command=self.move.lying_belly)
        btn_lying_belly.config(height=1, width=30)
        btn_crouch = tk.Button(top_level, text="Crouch", command=self.move.crouch)
        btn_crouch.config(height=1, width=30)

        # packs all of the buttons by going through the children of the top_level window
        for btn in sorted(top_level.children):
            top_level.children[btn].pack()
        pass

    def stand_toggle(self):
        # TODO: call movement stand and sit methods
        if self.is_standing:
            # TODO: insert sitting method
            self.move.posture("Sit")
            self.is_standing = False
        else:
            # TODO: insert standing method
            self.move.posture("Stand")
            self.is_standing = True
        pass

    def open_browser(self, event):
        webbrowser.open_new(event.widget.cget("text"))

root = tk.Tk()
root.geometry("600x700")
app = Window(root)
root.mainloop()
