from Tkinter import *
from PIL import Image, ImageTk
from movement import Movement

class Window(Frame):
    def __init__(self, master=None):
        self.move = Movement("169.254.141.183", 9559)
        Frame.__init__(self, master)
        self.master = master
        self.labels = []
        self.init_window()
        

    def init_window(self):
        self.master.title("GUI")
        self.pack(fill=BOTH, expand=1)
        self.init_menu()
        self.init_buttons()
        self.init_left_sliders()
        self.init_right_sliders()
        self.init_head_sliders()
        self.init_hands()
        self.init_labels()

    def init_menu(self):
        # initialises the menu of the window
        main_menu = Menu(self.master)
        # parameter menu is set as the instance of the main_menu
        self.master.config(menu=main_menu)

        file = Menu(main_menu)
        # label is how the command will appear, the command is the programmatic action taken
        file.add_command(label='Exit', command=self.master.quit)
        main_menu.add_cascade(label='File', menu=file)

        edit = Menu(main_menu)
        edit.add_command(label='Show image', command=self.show_image)
        main_menu.add_cascade(label='Edit', menu=edit)

    def init_buttons(self):
        #TODO: place buttons at correct coordinates
        btn_quit = Button(self.master, text="quit", command=self.master.quit)
        btn_quit.place(x=0, y=0)

        btn_lock = Button(self.master, text="Lock head", command=self.move.lock_head)
        btn_lock.place(x=100, y=0)

        btn_release = Button(self.master, text="Release head", command=self.move.release_head)
        btn_release.place(x=200, y=0)

        
        #btn_both_arms = Button(self.master, text="Both arm control", command=self.master.quit)
        #btn_both_arms.place(x=300, y=0)
        
        # btn_walk = Button(self, text="walk", command=self.move.walk())
        # btn_walk.place(x=0, y=0)

    def init_left_sliders(self):
        #TODO: alter commands to match relevant function from movement class
        #angle sliders for joints, limited to valid rotation ranges
        elbow_slider_yaw = Scale(self.master, orient='horizontal', from_=-119, to=119, command=self.move.left_elbow_yaw)
        elbow_slider_yaw.place(x=0, y=100)
        elbow_slider_roll = Scale(self.master, orient='horizontal', from_=-88, to=0, command=self.move.left_elbow_roll)
        elbow_slider_roll.place(x=0, y=200)

        shoulder_slider_roll = Scale(self.master, orient='horizontal', from_=-18, to=76, command=self.move.left_shoulder_roll)
        shoulder_slider_roll.place(x=0, y=300)
        shoulder_slider_pitch = Scale(self.master, orient='horizontal', from_=-119, to=119, command=self.move.left_shoulder_pitch)
        shoulder_slider_pitch.set(75)
        shoulder_slider_pitch.place(x=0, y=400)

        wrist_slider_yaw = Scale(self.master, orient='horizontal', from_=-104, to=104, command=self.move.left_wrist_yaw)
        wrist_slider_yaw.place(x=0, y=500)
        pass

    def init_right_sliders(self):
        # TODO: alter commands to match relevant function from movement class
        # angle sliders for joints, limited to valid rotation ranges
        elbow_slider_yaw = Scale(self.master, orient='horizontal', from_=-119, to=119, command=self.move.right_elbow_yaw)
        elbow_slider_yaw.place(x=200, y=100)
        elbow_slider_roll = Scale(self.master, orient='horizontal', from_=0, to=88, command=self.move.right_elbow_roll)
        elbow_slider_roll.place(x=200, y=200)

        shoulder_slider_roll = Scale(self.master, orient='horizontal', from_=-76, to=18, command=self.move.right_shoulder_roll)
        shoulder_slider_roll.place(x=200, y=300)
        shoulder_slider_pitch = Scale(self.master, orient='horizontal', from_=-119, to=119, command=self.move.right_shoulder_pitch)
        shoulder_slider_pitch.set(75)
        shoulder_slider_pitch.place(x=200, y=400)

        wrist_slider_yaw = Scale(self.master, orient='horizontal', from_=-104, to=104, command=self.move.right_wrist_yaw)
        wrist_slider_yaw.place(x=200, y=500)
        pass

    def init_head_sliders(self):
        head_slider_yaw = Scale(self.master, orient='horizontal', from_=-119, to=119, command=self.move.head_swivel)
        head_slider_yaw.place(x=400, y=100)
        head_slider_pitch = Scale(self.master, orient='horizontal', from_=-38, to=29, command=self.move.head_up_down)
        head_slider_pitch.place(x=400, y=200)
        pass

    def init_hands(self):
        right_hand_slider = Scale(self.master, orient='horizontal', from_=0, to=50, command=self.move.right_hand_move)
        right_hand_slider.place(x=400, y=300)

        left_hand_slider = Scale(self.master, orient='horizontal', from_=0, to=50, command=self.move.left_hand_move)
        left_hand_slider.place(x=400, y=400)
        pass

    def init_labels(self):
        joint_angle_names = ['Left Elbow Yaw', 'Left Elbow Roll', 'Left Shoulder Roll', 'Left Shoulder Pitch', 'Left Wrist Yaw',
                             'Right Elbow Yaw', 'Right Elbow Roll', 'Right Shoulder Roll', 'Right Shoulder Pitch', 'Right Wrist Yaw', 'Head Yaw', 'Head Pitch', 'Right Hand', 'Left Hand']
        y_counter_l = 80
        y_counter_r = 80
        y_counter_m = 80
        count = 0
        for joint_name in joint_angle_names:
            print("count {} joint {}".format(count, joint_name))
            print("start of label loop")
            label = Label(self.master, text=joint_name)
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
        #TODO: get the image showing, try different loading method
        image_blue = Image.open('F:/Pictures/013.jpg')
        render = ImageTk.PhotoImage(image_blue)
        load_image_blue = Label(self, image=render)
        load_image_blue.place(x=20, y=20)
        pass

root = Tk()
root.geometry("600x700")
app = Window(root)
root.mainloop()
