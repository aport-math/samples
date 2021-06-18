# Import modules
import tkinter as tk
import math
import numpy as np

class DrawingRig(object):
    def __init__(self):
        # Draw the basic canvas
        self.window = tk.Tk()   # create the window
        self.w = 1200    # window width
        self.h = 900     # window height
        self.wb = 300    # sidebar width
        ws = self.window.winfo_screenwidth()    # screen width
        hs = self.window.winfo_screenheight()   # screen height
        self.window.geometry('%dx%d+%d+%d' % (self.w, self.h, 0.5*(ws - self.w), 0.2*(hs - self.h)))    # screen dimensions and placement
        self.window.title('2D Drawing Rig')     # title of the window
        self.canvas = tk.Canvas(self.window, width = self.w, height = self.h)     # create the drawing canvas
        self.canvas.pack()      # initialize the canvas

        # Draw separating lines
        self.canvas.create_line(self.wb, 0, self.wb, self.h)
        self.canvas.create_line(0, self.h/80 + 6*self.h/20, self.wb, self.h/80 + 6*self.h/20)

        # Create the export button
        self.button_export = tk.Button(self.window, text='Export', font = ('Arial Bold', int(self.wb/15)), command=self.export_canvas)
        self.button_export.pack()
        self.button_export.place(x = 0.9*self.w, y = 0.9*self.h, anchor = 'n')

        # Create a window label in the middle top of the window
        lbl_title = tk.Label(self.window, text = '2D Drawing Rig',\
            font = ('Arial Bold', int(self.wb/15)))
        lbl_title.place(x = self.wb/2, y = self.h/80, anchor = 'n')

        # Initial parameter inputs
        self.df_core_x = 0
        self.df_core_y = 0
        self.df_core_z = 0

        self.df_lb_y = 0
        self.df_lb_z = 0

        self.df_neck_x = 0
        self.df_neck_y = 0
        self.df_neck_z = 0

        self.df_head_y = 0

        self.df_shoulder_l_x = 0
        self.df_shoulder_l_z = 0
        self.df_shoulder_r_x = 0
        self.df_shoulder_r_z = 0

        self.df_ua_l_x = 0
        self.df_ua_l_y = 0
        self.df_ua_r_x = 0
        self.df_ua_r_y = 0

        self.df_elbow_l_y = 0
        self.df_elbow_l_z = 0
        self.df_elbow_r_y = 0
        self.df_elbow_r_z = 0

        self.df_wrist_l_x = 0
        self.df_wrist_l_y = 0
        self.df_wrist_r_x = 0
        self.df_wrist_r_y = 0

        self.df_hand_l_x = 0
        self.df_hand_r_x = 0

        self.df_hip_l_x = 0
        self.df_hip_l_y = 0
        self.df_hip_l_z = 0
        self.df_hip_r_x = 0
        self.df_hip_r_y = 0
        self.df_hip_r_z = 0

        self.df_knee_l_y = 0
        self.df_knee_r_y = 0

        self.df_ankle_l_x = 0
        self.df_ankle_l_y = 0
        self.df_ankle_r_x = 0
        self.df_ankle_r_y = 0

        self.df_foot_l_y = 0
        self.df_foot_r_y = 0

        # Size scale parameter
        self.len_scale = self.h/10

        # Create unmoved vectors for each piece
        self.v_lb = self.len_scale*np.array([[0], [0], [-1]])
        self.v_ub = self.len_scale*np.array([[0], [0], [-1]])
        self.v_neck = self.len_scale*np.array([[0], [0], [-1.1]])
        self.v_shoulder_l = self.len_scale*np.array([[0], [0.4], [-0.9]])
        self.v_shoulder_r = self.len_scale*np.array([[0], [-0.4], [-0.9]])
        self.v_ua_l = self.len_scale*np.array([[0], [0.6], [0]])
        self.v_ua_r = self.len_scale*np.array([[0], [-0.6], [0]])
        self.v_elbow_l = self.len_scale*np.array([[0], [0], [1.2]])
        self.v_elbow_r = self.len_scale*np.array([[0], [0], [1.2]])
        self.v_wrist_l = self.len_scale*np.array([[0], [0], [0.8]])
        self.v_wrist_r = self.len_scale*np.array([[0], [0], [0.8]])
        self.v_hand_l = self.len_scale*np.array([[0], [0], [0.4]])
        self.v_hand_r = self.len_scale*np.array([[0], [0], [0.4]])
        self.v_fingers_l = self.len_scale*np.array([[0], [0], [0.4]])
        self.v_fingers_r = self.len_scale*np.array([[0], [0], [0.4]])
        self.v_hip_l = self.len_scale*np.array([[0], [0.4], [0.4]])
        self.v_hip_r = self.len_scale*np.array([[0], [-0.4], [0.4]])
        self.v_knee_l = self.len_scale*np.array([[0], [0], [1.4]])
        self.v_knee_r = self.len_scale*np.array([[0], [0], [1.4]])
        self.v_ankle_l = self.len_scale*np.array([[0], [0], [1.2]])
        self.v_ankle_r = self.len_scale*np.array([[0], [0], [1.2]])
        self.v_foot_l = self.len_scale*np.array([[-0.6], [0], [0]])
        self.v_foot_r = self.len_scale*np.array([[-0.6], [0], [0]])
        self.v_toes_l = self.len_scale*np.array([[-0.3], [0], [0]])
        self.v_toes_r = self.len_scale*np.array([[-0.3], [0], [0]])

        # Radius parameters
        self.rad_core = self.len_scale*0.06
        self.rad_lb = self.len_scale*0.06
        self.rad_neck = self.len_scale*0.06
        self.rad_head = self.len_scale*0.6
        self.rad_shoulder = self.len_scale*0.06
        self.rad_ua = self.len_scale*0.25
        self.rad_elbow = self.len_scale*0.20
        self.rad_wrist = self.len_scale*0.15
        self.rad_hand = self.len_scale*0.08
        self.rad_hip = self.len_scale*0.3
        self.rad_knee = self.len_scale*0.22
        self.rad_ankle = self.len_scale*0.15
        self.rad_foot = self.len_scale*0.10

        # Draw the shapes
        self.draw_ui()
        self.calculate_positions()
        self.all_shape_ids = []
        self.draw_shapes()

        # Initialize the window
        self.window.mainloop()

    def export_canvas(self):
        # Export the canvas
        self.canvas.postscript(file = 'export.ps', colormode = 'color')

    def draw_ui(self):
        # Bar width
        self.bar_width = 3/5*self.wb

        # Always draw the core rotation part
        lbl_df_core = tk.Label(self.window, text = 'Core Rotation', font = ('Arial Bold', int(self.wb/25)))
        lbl_df_core.place(x = self.wb/2, y = self.h/80 + 1*self.h/20, anchor = 'n')

        lbl_df_core_x = tk.Label(self.window, text = 'X Rotation', font = ('Arial Bold', int(self.wb/32)))
        lbl_df_core_x.place(x = self.wb/2, y = self.h/80 + 1.5*self.h/20, anchor = 'n')
        self.range_df_core_x = [-6.4, 6.4]
        self.resolution_df_core_x = 0.2
        self.bar_df_core_x = tk.Scale(self.window, from_=self.range_df_core_x[0], to=self.range_df_core_x[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_core_x, command=self.set_bar_df_core_x, width = 10)
        self.bar_df_core_x.pack()
        self.bar_df_core_x.place(x = self.wb/2, y = self.h/80 + 1.9*self.h/20, anchor = 'n')
        self.bar_df_core_x.set(self.df_core_x)
        self.button_l_df_core_x = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_core_x)
        self.button_l_df_core_x.pack()
        self.button_l_df_core_x.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 2.2*self.h/20, anchor = 'n')
        self.button_r_df_core_x = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_core_x)
        self.button_r_df_core_x.pack()
        self.button_r_df_core_x.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 2.2*self.h/20, anchor = 'n')

        lbl_df_core_y = tk.Label(self.window, text = 'Y Rotation', font = ('Arial Bold', int(self.wb/32)))
        lbl_df_core_y.place(x = self.wb/2, y = self.h/80 + 2.9*self.h/20, anchor = 'n')
        self.range_df_core_y = [-6.4, 6.4]
        self.resolution_df_core_y = 0.2
        self.bar_df_core_y = tk.Scale(self.window, from_=self.range_df_core_y[0], to=self.range_df_core_y[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_core_y, command=self.set_bar_df_core_y, width = 10)
        self.bar_df_core_y.pack()
        self.bar_df_core_y.place(x = self.wb/2, y = self.h/80 + 3.3*self.h/20, anchor = 'n')
        self.bar_df_core_y.set(self.df_core_y)
        self.button_l_df_core_y = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_core_y)
        self.button_l_df_core_y.pack()
        self.button_l_df_core_y.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 3.6*self.h/20, anchor = 'n')
        self.button_r_df_core_y = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_core_y)
        self.button_r_df_core_y.pack()
        self.button_r_df_core_y.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 3.6*self.h/20, anchor = 'n')

        lbl_df_core_z = tk.Label(self.window, text = 'Z Rotation', font = ('Arial Bold', int(self.wb/32)))
        lbl_df_core_z.place(x = self.wb/2, y = self.h/80 + 4.3*self.h/20, anchor = 'n')
        self.range_df_core_z = [-6.4, 6.4]
        self.resolution_df_core_z = 0.2
        self.bar_df_core_z = tk.Scale(self.window, from_=self.range_df_core_z[0], to=self.range_df_core_z[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_core_z, command=self.set_bar_df_core_z, width = 10)
        self.bar_df_core_z.pack()
        self.bar_df_core_z.place(x = self.wb/2, y = self.h/80 + 4.7*self.h/20, anchor = 'n')
        self.bar_df_core_z.set(self.df_core_z)
        self.button_l_df_core_z = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_core_z)
        self.button_l_df_core_z.pack()
        self.button_l_df_core_z.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 5*self.h/20, anchor = 'n')
        self.button_r_df_core_z = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_core_z)
        self.button_r_df_core_z.pack()
        self.button_r_df_core_z.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 5*self.h/20, anchor = 'n')

        # Create a drop down for the other button sets
        self.other_button_ids = []
        lbl_option_selection = tk.Label(self.window, text = 'Body Part Selection', font = ('Arial Bold', int(self.wb/25)))
        lbl_option_selection.place(x = self.wb/2, y = self.h/80 + 6.2*self.h/20, anchor = 'n')
        selection_option_list = ['Head and Neck', 'Upper Torso', 'Left Arm', 'Right Arm', 'Left Leg', 'Right Leg', 'Hands and Feet']
        self.drop_var = tk.StringVar()
        self.drop_var.set('Head and Neck')
        self.drop_menu = tk.OptionMenu(self.window, self.drop_var, *selection_option_list, command=self.drop_down_action)
        self.drop_menu.place(x = self.wb/2, y = self.h/80 + 6.8*self.h/20, anchor = 'n')
        self.drop_down_action('Head and Neck')

    def drop_down_action(self, value):
        # Delete the old buttons
        while len(self.other_button_ids) > 0:
            self.other_button_ids.pop(0).destroy()

        # Draw the remaining button sets
        if value == 'Head and Neck':
            lbl_df_head = tk.Label(self.window, text = 'Head Rotation', font = ('Arial Bold', int(self.wb/25)))
            lbl_df_head.place(x = self.wb/2, y = self.h/80 + 7.8*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_head)

            lbl_df_head_y = tk.Label(self.window, text = 'Up                          Down', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_head_y.place(x = self.wb/2, y = self.h/80 + 8.3*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_head_y)
            self.range_df_head_y = [-1.1, 1.1]
            self.resolution_df_head_y = 0.1
            self.bar_df_head_y = tk.Scale(self.window, from_=self.range_df_head_y[0], to=self.range_df_head_y[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_head_y, command=self.set_bar_df_head_y, width = 10)
            self.bar_df_head_y.pack()
            self.bar_df_head_y.place(x = self.wb/2, y = self.h/80 + 8.7*self.h/20, anchor = 'n')
            self.bar_df_head_y.set(self.df_head_y)
            self.button_l_df_head_y = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_head_y)
            self.button_l_df_head_y.pack()
            self.button_l_df_head_y.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 9*self.h/20, anchor = 'n')
            self.button_r_df_head_y = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_head_y)
            self.button_r_df_head_y.pack()
            self.button_r_df_head_y.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 9*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_head_y)
            self.other_button_ids.append(self.button_l_df_head_y)
            self.other_button_ids.append(self.button_r_df_head_y)

            lbl_df_neck = tk.Label(self.window, text = 'Neck Rotation', font = ('Arial Bold', int(self.wb/25)))
            lbl_df_neck.place(x = self.wb/2, y = self.h/80 + 10*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_neck)

            lbl_df_neck_x = tk.Label(self.window, text = 'Lean Right             Lean Left', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_neck_x.place(x = self.wb/2, y = self.h/80 + 10.5*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_neck_x)
            self.range_df_neck_x = [-0.8, 0.8]
            self.resolution_df_neck_x = 0.1
            self.bar_df_neck_x = tk.Scale(self.window, from_=self.range_df_neck_x[0], to=self.range_df_neck_x[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_neck_x, command=self.set_bar_df_neck_x, width = 10)
            self.bar_df_neck_x.pack()
            self.bar_df_neck_x.place(x = self.wb/2, y = self.h/80 + 10.9*self.h/20, anchor = 'n')
            self.bar_df_neck_x.set(self.df_neck_x)
            self.button_l_df_neck_x = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_neck_x)
            self.button_l_df_neck_x.pack()
            self.button_l_df_neck_x.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 11.2*self.h/20, anchor = 'n')
            self.button_r_df_neck_x = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_neck_x)
            self.button_r_df_neck_x.pack()
            self.button_r_df_neck_x.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 11.2*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_neck_x)
            self.other_button_ids.append(self.button_l_df_neck_x)
            self.other_button_ids.append(self.button_r_df_neck_x)

            lbl_df_neck_y = tk.Label(self.window, text = 'Up                          Down', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_neck_y.place(x = self.wb/2, y = self.h/80 + 11.9*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_neck_y)
            self.range_df_neck_y = [-0.6, 1.1]
            self.resolution_df_neck_y = 0.1
            self.bar_df_neck_y = tk.Scale(self.window, from_=self.range_df_neck_y[0], to=self.range_df_neck_y[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_neck_y, command=self.set_bar_df_neck_y, width = 10)
            self.bar_df_neck_y.pack()
            self.bar_df_neck_y.place(x = self.wb/2, y = self.h/80 + 12.3*self.h/20, anchor = 'n')
            self.bar_df_neck_y.set(self.df_neck_y)
            self.button_l_df_neck_y = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_neck_y)
            self.button_l_df_neck_y.pack()
            self.button_l_df_neck_y.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 12.6*self.h/20, anchor = 'n')
            self.button_r_df_neck_y = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_neck_y)
            self.button_r_df_neck_y.pack()
            self.button_r_df_neck_y.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 12.6*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_neck_y)
            self.other_button_ids.append(self.button_l_df_neck_y)
            self.other_button_ids.append(self.button_r_df_neck_y)

            lbl_df_neck_z = tk.Label(self.window, text = 'Turn Right             Turn Left', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_neck_z.place(x = self.wb/2, y = self.h/80 + 13.3*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_neck_z)
            self.range_df_neck_z = [-1.6, 1.6]
            self.resolution_df_neck_z = 0.1
            self.bar_df_neck_z = tk.Scale(self.window, from_=self.range_df_neck_z[0], to=self.range_df_neck_z[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_neck_z, command=self.set_bar_df_neck_z, width = 10)
            self.bar_df_neck_z.pack()
            self.bar_df_neck_z.place(x = self.wb/2, y = self.h/80 + 13.7*self.h/20, anchor = 'n')
            self.bar_df_neck_z.set(self.df_neck_z)
            self.button_l_df_neck_z = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_neck_z)
            self.button_l_df_neck_z.pack()
            self.button_l_df_neck_z.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 14*self.h/20, anchor = 'n')
            self.button_r_df_neck_z = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_neck_z)
            self.button_r_df_neck_z.pack()
            self.button_r_df_neck_z.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 14*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_neck_z)
            self.other_button_ids.append(self.button_l_df_neck_z)
            self.other_button_ids.append(self.button_r_df_neck_z)

        if value == 'Upper Torso':
            lbl_df_lb = tk.Label(self.window, text = 'Back Rotation', font = ('Arial Bold', int(self.wb/25)))
            lbl_df_lb.place(x = self.wb/2, y = self.h/80 + 7.8*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_lb)

            lbl_df_lb_y = tk.Label(self.window, text = 'Up                          Down', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_lb_y.place(x = self.wb/2, y = self.h/80 + 8.3*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_lb_y)
            self.range_df_lb_y = [-0.8, 1.1]
            self.resolution_df_lb_y = 0.1
            self.bar_df_lb_y = tk.Scale(self.window, from_=self.range_df_lb_y[0], to=self.range_df_lb_y[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_lb_y, command=self.set_bar_df_lb_y, width = 10)
            self.bar_df_lb_y.pack()
            self.bar_df_lb_y.place(x = self.wb/2, y = self.h/80 + 8.7*self.h/20, anchor = 'n')
            self.bar_df_lb_y.set(self.df_lb_y)
            self.button_l_df_lb_y = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_lb_y)
            self.button_l_df_lb_y.pack()
            self.button_l_df_lb_y.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 9*self.h/20, anchor = 'n')
            self.button_r_df_lb_y = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_lb_y)
            self.button_r_df_lb_y.pack()
            self.button_r_df_lb_y.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 9*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_lb_y)
            self.other_button_ids.append(self.button_l_df_lb_y)
            self.other_button_ids.append(self.button_r_df_lb_y)

            lbl_df_lb_z = tk.Label(self.window, text = 'Turn Right             Turn Left', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_lb_z.place(x = self.wb/2, y = self.h/80 + 9.7*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_lb_z)
            self.range_df_lb_z = [-0.8, 0.8]
            self.resolution_df_lb_z = 0.1
            self.bar_df_lb_z = tk.Scale(self.window, from_=self.range_df_lb_z[0], to=self.range_df_lb_z[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_lb_z, command=self.set_bar_df_lb_z, width = 10)
            self.bar_df_lb_z.pack()
            self.bar_df_lb_z.place(x = self.wb/2, y = self.h/80 + 10.1*self.h/20, anchor = 'n')
            self.bar_df_lb_z.set(self.df_lb_z)
            self.button_l_df_lb_z = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_lb_z)
            self.button_l_df_lb_z.pack()
            self.button_l_df_lb_z.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 10.4*self.h/20, anchor = 'n')
            self.button_r_df_lb_z = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_lb_z)
            self.button_r_df_lb_z.pack()
            self.button_r_df_lb_z.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 10.4*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_lb_z)
            self.other_button_ids.append(self.button_l_df_lb_z)
            self.other_button_ids.append(self.button_r_df_lb_z)

            lbl_df_shoulder_l = tk.Label(self.window, text = 'Left Shoulder Rotation', font = ('Arial Bold', int(self.wb/25)))
            lbl_df_shoulder_l.place(x = self.wb/2, y = self.h/80 + 11.4*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_shoulder_l)

            lbl_df_shoulder_l_x = tk.Label(self.window, text = 'Up                          Down', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_shoulder_l_x.place(x = self.wb/2, y = self.h/80 + 11.9*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_shoulder_l_x)
            self.range_df_shoulder_l_x = [-0.6, 0.3]
            self.resolution_df_shoulder_l_x = 0.1
            self.bar_df_shoulder_l_x = tk.Scale(self.window, from_=self.range_df_shoulder_l_x[0], to=self.range_df_shoulder_l_x[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_shoulder_l_x, command=self.set_bar_df_shoulder_l_x, width = 10)
            self.bar_df_shoulder_l_x.pack()
            self.bar_df_shoulder_l_x.place(x = self.wb/2, y = self.h/80 + 12.3*self.h/20, anchor = 'n')
            self.bar_df_shoulder_l_x.set(self.df_shoulder_l_x)
            self.button_l_df_shoulder_l_x = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_shoulder_l_x)
            self.button_l_df_shoulder_l_x.pack()
            self.button_l_df_shoulder_l_x.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 12.6*self.h/20, anchor = 'n')
            self.button_r_df_shoulder_l_x = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_shoulder_l_x)
            self.button_r_df_shoulder_l_x.pack()
            self.button_r_df_shoulder_l_x.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 12.6*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_shoulder_l_x)
            self.other_button_ids.append(self.button_l_df_shoulder_l_x)
            self.other_button_ids.append(self.button_r_df_shoulder_l_x)

            lbl_df_shoulder_l_z = tk.Label(self.window, text = 'Forward                 Backward', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_shoulder_l_z.place(x = self.wb/2, y = self.h/80 + 13.3*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_shoulder_l_z)
            self.range_df_shoulder_l_z = [-0.6, 0.4]
            self.resolution_df_shoulder_l_z = 0.1
            self.bar_df_shoulder_l_z = tk.Scale(self.window, from_=self.range_df_shoulder_l_z[0], to=self.range_df_shoulder_l_z[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_shoulder_l_z, command=self.set_bar_df_shoulder_l_z, width = 10)
            self.bar_df_shoulder_l_z.pack()
            self.bar_df_shoulder_l_z.place(x = self.wb/2, y = self.h/80 + 13.7*self.h/20, anchor = 'n')
            self.bar_df_shoulder_l_z.set(self.df_shoulder_l_z)
            self.button_l_df_shoulder_l_z = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_shoulder_l_z)
            self.button_l_df_shoulder_l_z.pack()
            self.button_l_df_shoulder_l_z.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 14*self.h/20, anchor = 'n')
            self.button_r_df_shoulder_l_z = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_shoulder_l_z)
            self.button_r_df_shoulder_l_z.pack()
            self.button_r_df_shoulder_l_z.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 14*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_shoulder_l_z)
            self.other_button_ids.append(self.button_l_df_shoulder_l_z)
            self.other_button_ids.append(self.button_r_df_shoulder_l_z)

            lbl_df_shoulder_r = tk.Label(self.window, text = 'Right Shoulder Rotation', font = ('Arial Bold', int(self.wb/25)))
            lbl_df_shoulder_r.place(x = self.wb/2, y = self.h/80 + 15*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_shoulder_r)

            lbl_df_shoulder_r_x = tk.Label(self.window, text = 'Down                          Up', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_shoulder_r_x.place(x = self.wb/2, y = self.h/80 + 15.5*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_shoulder_r_x)
            self.range_df_shoulder_r_x = [-0.3, 0.6]
            self.resolution_df_shoulder_r_x = 0.1
            self.bar_df_shoulder_r_x = tk.Scale(self.window, from_=self.range_df_shoulder_r_x[0], to=self.range_df_shoulder_r_x[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_shoulder_r_x, command=self.set_bar_df_shoulder_r_x, width = 10)
            self.bar_df_shoulder_r_x.pack()
            self.bar_df_shoulder_r_x.place(x = self.wb/2, y = self.h/80 + 15.9*self.h/20, anchor = 'n')
            self.bar_df_shoulder_r_x.set(self.df_shoulder_r_x)
            self.button_l_df_shoulder_r_x = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_shoulder_r_x)
            self.button_l_df_shoulder_r_x.pack()
            self.button_l_df_shoulder_r_x.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 16.2*self.h/20, anchor = 'n')
            self.button_r_df_shoulder_r_x = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_shoulder_r_x)
            self.button_r_df_shoulder_r_x.pack()
            self.button_r_df_shoulder_r_x.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 16.2*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_shoulder_r_x)
            self.other_button_ids.append(self.button_l_df_shoulder_r_x)
            self.other_button_ids.append(self.button_r_df_shoulder_r_x)

            lbl_df_shoulder_r_z = tk.Label(self.window, text = 'Backward                 Forward', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_shoulder_r_z.place(x = self.wb/2, y = self.h/80 + 16.9*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_shoulder_r_z)
            self.range_df_shoulder_r_z = [-0.4, 0.6]
            self.resolution_df_shoulder_r_z = 0.1
            self.bar_df_shoulder_r_z = tk.Scale(self.window, from_=self.range_df_shoulder_r_z[0], to=self.range_df_shoulder_r_z[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_shoulder_r_z, command=self.set_bar_df_shoulder_r_z, width = 10)
            self.bar_df_shoulder_r_z.pack()
            self.bar_df_shoulder_r_z.place(x = self.wb/2, y = self.h/80 + 17.3*self.h/20, anchor = 'n')
            self.bar_df_shoulder_r_z.set(self.df_shoulder_r_z)
            self.button_l_df_shoulder_r_z = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_shoulder_r_z)
            self.button_l_df_shoulder_r_z.pack()
            self.button_l_df_shoulder_r_z.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 17.6*self.h/20, anchor = 'n')
            self.button_r_df_shoulder_r_z = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_shoulder_r_z)
            self.button_r_df_shoulder_r_z.pack()
            self.button_r_df_shoulder_r_z.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 17.6*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_shoulder_r_z)
            self.other_button_ids.append(self.button_l_df_shoulder_r_z)
            self.other_button_ids.append(self.button_r_df_shoulder_r_z)

        if value == 'Left Arm':
            lbl_df_ua_l = tk.Label(self.window, text = 'Left Upper Arm Rotation', font = ('Arial Bold', int(self.wb/25)))
            lbl_df_ua_l.place(x = self.wb/2, y = self.h/80 + 7.8*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_ua_l)

            lbl_df_ua_l_x = tk.Label(self.window, text = 'Side Lift             Side Lower', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_ua_l_x.place(x = self.wb/2, y = self.h/80 + 8.3*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_ua_l_x)
            self.range_df_ua_l_x = [-2.8, 0.3]
            self.resolution_df_ua_l_x = 0.1
            self.bar_df_ua_l_x = tk.Scale(self.window, from_=self.range_df_ua_l_x[0], to=self.range_df_ua_l_x[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_ua_l_x, command=self.set_bar_df_ua_l_x, width = 10)
            self.bar_df_ua_l_x.pack()
            self.bar_df_ua_l_x.place(x = self.wb/2, y = self.h/80 + 8.7*self.h/20, anchor = 'n')
            self.bar_df_ua_l_x.set(self.df_ua_l_x)
            self.button_l_df_ua_l_x = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_ua_l_x)
            self.button_l_df_ua_l_x.pack()
            self.button_l_df_ua_l_x.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 9*self.h/20, anchor = 'n')
            self.button_r_df_ua_l_x = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_ua_l_x)
            self.button_r_df_ua_l_x.pack()
            self.button_r_df_ua_l_x.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 9*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_ua_l_x)
            self.other_button_ids.append(self.button_l_df_ua_l_x)
            self.other_button_ids.append(self.button_r_df_ua_l_x)

            lbl_df_ua_l_y = tk.Label(self.window, text = 'Forward                 Backward', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_ua_l_y.place(x = self.wb/2, y = self.h/80 + 9.7*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_ua_l_y)
            self.range_df_ua_l_y = [-2.8, 2.8]
            self.resolution_df_ua_l_y = 0.2
            self.bar_df_ua_l_y = tk.Scale(self.window, from_=self.range_df_ua_l_y[0], to=self.range_df_ua_l_y[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_ua_l_y, command=self.set_bar_df_ua_l_y, width = 10)
            self.bar_df_ua_l_y.pack()
            self.bar_df_ua_l_y.place(x = self.wb/2, y = self.h/80 + 10.1*self.h/20, anchor = 'n')
            self.bar_df_ua_l_y.set(self.df_ua_l_y)
            self.button_l_df_ua_l_y = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_ua_l_y)
            self.button_l_df_ua_l_y.pack()
            self.button_l_df_ua_l_y.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 10.4*self.h/20, anchor = 'n')
            self.button_r_df_ua_l_y = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_ua_l_y)
            self.button_r_df_ua_l_y.pack()
            self.button_r_df_ua_l_y.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 10.4*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_ua_l_y)
            self.other_button_ids.append(self.button_l_df_ua_l_y)
            self.other_button_ids.append(self.button_r_df_ua_l_y)

            lbl_df_elbow_l = tk.Label(self.window, text = 'Left Elbow Rotation', font = ('Arial Bold', int(self.wb/25)))
            lbl_df_elbow_l.place(x = self.wb/2, y = self.h/80 + 11.4*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_elbow_l)

            lbl_df_elbow_l_y = tk.Label(self.window, text = 'Bend                  Straighten', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_elbow_l_y.place(x = self.wb/2, y = self.h/80 + 11.9*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_elbow_l_y)
            self.range_df_elbow_l_y = [-2.7, 0.1]
            self.resolution_df_elbow_l_y = 0.1
            self.bar_df_elbow_l_y = tk.Scale(self.window, from_=self.range_df_elbow_l_y[0], to=self.range_df_elbow_l_y[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_elbow_l_y, command=self.set_bar_df_elbow_l_y, width = 10)
            self.bar_df_elbow_l_y.pack()
            self.bar_df_elbow_l_y.place(x = self.wb/2, y = self.h/80 + 12.3*self.h/20, anchor = 'n')
            self.bar_df_elbow_l_y.set(self.df_elbow_l_y)
            self.button_l_df_elbow_l_y = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_elbow_l_y)
            self.button_l_df_elbow_l_y.pack()
            self.button_l_df_elbow_l_y.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 12.6*self.h/20, anchor = 'n')
            self.button_r_df_elbow_l_y = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_elbow_l_y)
            self.button_r_df_elbow_l_y.pack()
            self.button_r_df_elbow_l_y.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 12.6*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_elbow_l_y)
            self.other_button_ids.append(self.button_l_df_elbow_l_y)
            self.other_button_ids.append(self.button_r_df_elbow_l_y)

            lbl_df_elbow_l_z = tk.Label(self.window, text = 'Twist In               Twist Out', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_elbow_l_z.place(x = self.wb/2, y = self.h/80 + 13.3*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_elbow_l_z)
            self.range_df_elbow_l_z = [-2.8, 1.6]
            self.resolution_df_elbow_l_z = 0.1
            self.bar_df_elbow_l_z = tk.Scale(self.window, from_=self.range_df_elbow_l_z[0], to=self.range_df_elbow_l_z[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_elbow_l_z, command=self.set_bar_df_elbow_l_z, width = 10)
            self.bar_df_elbow_l_z.pack()
            self.bar_df_elbow_l_z.place(x = self.wb/2, y = self.h/80 + 13.7*self.h/20, anchor = 'n')
            self.bar_df_elbow_l_z.set(self.df_elbow_l_z)
            self.button_l_df_elbow_l_z = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_elbow_l_z)
            self.button_l_df_elbow_l_z.pack()
            self.button_l_df_elbow_l_z.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 14*self.h/20, anchor = 'n')
            self.button_r_df_elbow_l_z = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_elbow_l_z)
            self.button_r_df_elbow_l_z.pack()
            self.button_r_df_elbow_l_z.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 14*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_elbow_l_z)
            self.other_button_ids.append(self.button_l_df_elbow_l_z)
            self.other_button_ids.append(self.button_r_df_elbow_l_z)

            lbl_df_wrist_l = tk.Label(self.window, text = 'Left Wrist Rotation', font = ('Arial Bold', int(self.wb/25)))
            lbl_df_wrist_l.place(x = self.wb/2, y = self.h/80 + 15*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_wrist_l)

            lbl_df_wrist_l_x = tk.Label(self.window, text = 'Curl Out                 Curl In', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_wrist_l_x.place(x = self.wb/2, y = self.h/80 + 15.5*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_wrist_l_x)
            self.range_df_wrist_l_x = [-1.2, 1.2]
            self.resolution_df_wrist_l_x = 0.1
            self.bar_df_wrist_l_x = tk.Scale(self.window, from_=self.range_df_wrist_l_x[0], to=self.range_df_wrist_l_x[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_wrist_l_x, command=self.set_bar_df_wrist_l_x, width = 10)
            self.bar_df_wrist_l_x.pack()
            self.bar_df_wrist_l_x.place(x = self.wb/2, y = self.h/80 + 15.9*self.h/20, anchor = 'n')
            self.bar_df_wrist_l_x.set(self.df_wrist_l_x)
            self.button_l_df_wrist_l_x = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_wrist_l_x)
            self.button_l_df_wrist_l_x.pack()
            self.button_l_df_wrist_l_x.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 16.2*self.h/20, anchor = 'n')
            self.button_r_df_wrist_l_x = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_wrist_l_x)
            self.button_r_df_wrist_l_x.pack()
            self.button_r_df_wrist_l_x.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 16.2*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_wrist_l_x)
            self.other_button_ids.append(self.button_l_df_wrist_l_x)
            self.other_button_ids.append(self.button_r_df_wrist_l_x)

            lbl_df_wrist_l_y = tk.Label(self.window, text = 'Forward                 Backward', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_wrist_l_y.place(x = self.wb/2, y = self.h/80 + 16.9*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_wrist_l_y)
            self.range_df_wrist_l_y = [-0.6, 0.6]
            self.resolution_df_wrist_l_y = 0.1
            self.bar_df_wrist_l_y = tk.Scale(self.window, from_=self.range_df_wrist_l_y[0], to=self.range_df_wrist_l_y[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_wrist_l_y, command=self.set_bar_df_wrist_l_y, width = 10)
            self.bar_df_wrist_l_y.pack()
            self.bar_df_wrist_l_y.place(x = self.wb/2, y = self.h/80 + 17.3*self.h/20, anchor = 'n')
            self.bar_df_wrist_l_y.set(self.df_wrist_l_y)
            self.button_l_df_wrist_l_y = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_wrist_l_y)
            self.button_l_df_wrist_l_y.pack()
            self.button_l_df_wrist_l_y.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 17.6*self.h/20, anchor = 'n')
            self.button_r_df_wrist_l_y = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_wrist_l_y)
            self.button_r_df_wrist_l_y.pack()
            self.button_r_df_wrist_l_y.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 17.6*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_wrist_l_y)
            self.other_button_ids.append(self.button_l_df_wrist_l_y)
            self.other_button_ids.append(self.button_r_df_wrist_l_y)

        if value == 'Right Arm':
            lbl_df_ua_r = tk.Label(self.window, text = 'Right Upper Arm Rotation', font = ('Arial Bold', int(self.wb/25)))
            lbl_df_ua_r.place(x = self.wb/2, y = self.h/80 + 7.8*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_ua_r)

            lbl_df_ua_r_x = tk.Label(self.window, text = 'Side Lower             Side Lift', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_ua_r_x.place(x = self.wb/2, y = self.h/80 + 8.3*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_ua_r_x)
            self.range_df_ua_r_x = [-0.3, 2.8]
            self.resolution_df_ua_r_x = 0.1
            self.bar_df_ua_r_x = tk.Scale(self.window, from_=self.range_df_ua_r_x[0], to=self.range_df_ua_r_x[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_ua_r_x, command=self.set_bar_df_ua_r_x, width = 10)
            self.bar_df_ua_r_x.pack()
            self.bar_df_ua_r_x.place(x = self.wb/2, y = self.h/80 + 8.7*self.h/20, anchor = 'n')
            self.bar_df_ua_r_x.set(self.df_ua_r_x)
            self.button_l_df_ua_r_x = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_ua_r_x)
            self.button_l_df_ua_r_x.pack()
            self.button_l_df_ua_r_x.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 9*self.h/20, anchor = 'n')
            self.button_r_df_ua_r_x = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_ua_r_x)
            self.button_r_df_ua_r_x.pack()
            self.button_r_df_ua_r_x.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 9*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_ua_r_x)
            self.other_button_ids.append(self.button_l_df_ua_r_x)
            self.other_button_ids.append(self.button_r_df_ua_r_x)

            lbl_df_ua_r_y = tk.Label(self.window, text = 'Forward                 Backward', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_ua_r_y.place(x = self.wb/2, y = self.h/80 + 9.7*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_ua_r_y)
            self.range_df_ua_r_y = [-2.8, 2.8]
            self.resolution_df_ua_r_y = 0.2
            self.bar_df_ua_r_y = tk.Scale(self.window, from_=self.range_df_ua_r_y[0], to=self.range_df_ua_r_y[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_ua_r_y, command=self.set_bar_df_ua_r_y, width = 10)
            self.bar_df_ua_r_y.pack()
            self.bar_df_ua_r_y.place(x = self.wb/2, y = self.h/80 + 10.1*self.h/20, anchor = 'n')
            self.bar_df_ua_r_y.set(self.df_ua_r_y)
            self.button_l_df_ua_r_y = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_ua_r_y)
            self.button_l_df_ua_r_y.pack()
            self.button_l_df_ua_r_y.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 10.4*self.h/20, anchor = 'n')
            self.button_r_df_ua_r_y = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_ua_r_y)
            self.button_r_df_ua_r_y.pack()
            self.button_r_df_ua_r_y.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 10.4*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_ua_r_y)
            self.other_button_ids.append(self.button_l_df_ua_r_y)
            self.other_button_ids.append(self.button_r_df_ua_r_y)

            lbl_df_elbow_r = tk.Label(self.window, text = 'Right Elbow Rotation', font = ('Arial Bold', int(self.wb/25)))
            lbl_df_elbow_r.place(x = self.wb/2, y = self.h/80 + 11.4*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_elbow_r)

            lbl_df_elbow_r_y = tk.Label(self.window, text = 'Bend                  Straighten', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_elbow_r_y.place(x = self.wb/2, y = self.h/80 + 11.9*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_elbow_r_y)
            self.range_df_elbow_r_y = [-2.8, 0.1]
            self.resolution_df_elbow_r_y = 0.1
            self.bar_df_elbow_r_y = tk.Scale(self.window, from_=self.range_df_elbow_r_y[0], to=self.range_df_elbow_r_y[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_elbow_r_y, command=self.set_bar_df_elbow_r_y, width = 10)
            self.bar_df_elbow_r_y.pack()
            self.bar_df_elbow_r_y.place(x = self.wb/2, y = self.h/80 + 12.3*self.h/20, anchor = 'n')
            self.bar_df_elbow_r_y.set(self.df_elbow_r_y)
            self.button_l_df_elbow_r_y = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_elbow_r_y)
            self.button_l_df_elbow_r_y.pack()
            self.button_l_df_elbow_r_y.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 12.6*self.h/20, anchor = 'n')
            self.button_r_df_elbow_r_y = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_elbow_r_y)
            self.button_r_df_elbow_r_y.pack()
            self.button_r_df_elbow_r_y.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 12.6*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_elbow_r_y)
            self.other_button_ids.append(self.button_l_df_elbow_r_y)
            self.other_button_ids.append(self.button_r_df_elbow_r_y)

            lbl_df_elbow_r_z = tk.Label(self.window, text = 'Twist Out               Twist In', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_elbow_r_z.place(x = self.wb/2, y = self.h/80 + 13.3*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_elbow_r_z)
            self.range_df_elbow_r_z = [-1.6, 2.8]
            self.resolution_df_elbow_r_z = 0.1
            self.bar_df_elbow_r_z = tk.Scale(self.window, from_=self.range_df_elbow_r_z[0], to=self.range_df_elbow_r_z[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_elbow_r_z, command=self.set_bar_df_elbow_r_z, width = 10)
            self.bar_df_elbow_r_z.pack()
            self.bar_df_elbow_r_z.place(x = self.wb/2, y = self.h/80 + 13.7*self.h/20, anchor = 'n')
            self.bar_df_elbow_r_z.set(self.df_elbow_r_z)
            self.button_l_df_elbow_r_z = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_elbow_r_z)
            self.button_l_df_elbow_r_z.pack()
            self.button_l_df_elbow_r_z.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 14*self.h/20, anchor = 'n')
            self.button_r_df_elbow_r_z = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_elbow_r_z)
            self.button_r_df_elbow_r_z.pack()
            self.button_r_df_elbow_r_z.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 14*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_elbow_r_z)
            self.other_button_ids.append(self.button_l_df_elbow_r_z)
            self.other_button_ids.append(self.button_r_df_elbow_r_z)

            lbl_df_wrist_r = tk.Label(self.window, text = 'Right Wrist Rotation', font = ('Arial Bold', int(self.wb/25)))
            lbl_df_wrist_r.place(x = self.wb/2, y = self.h/80 + 15*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_wrist_r)

            lbl_df_wrist_r_x = tk.Label(self.window, text = 'Curl In                 Curl Out', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_wrist_r_x.place(x = self.wb/2, y = self.h/80 + 15.5*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_wrist_r_x)
            self.range_df_wrist_r_x = [-1.2, 1.2]
            self.resolution_df_wrist_r_x = 0.1
            self.bar_df_wrist_r_x = tk.Scale(self.window, from_=self.range_df_wrist_r_x[0], to=self.range_df_wrist_r_x[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_wrist_r_x, command=self.set_bar_df_wrist_r_x, width = 10)
            self.bar_df_wrist_r_x.pack()
            self.bar_df_wrist_r_x.place(x = self.wb/2, y = self.h/80 + 15.9*self.h/20, anchor = 'n')
            self.bar_df_wrist_r_x.set(self.df_wrist_r_x)
            self.button_l_df_wrist_r_x = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_wrist_r_x)
            self.button_l_df_wrist_r_x.pack()
            self.button_l_df_wrist_r_x.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 16.2*self.h/20, anchor = 'n')
            self.button_r_df_wrist_r_x = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_wrist_r_x)
            self.button_r_df_wrist_r_x.pack()
            self.button_r_df_wrist_r_x.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 16.2*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_wrist_r_x)
            self.other_button_ids.append(self.button_l_df_wrist_r_x)
            self.other_button_ids.append(self.button_r_df_wrist_r_x)

            lbl_df_wrist_r_y = tk.Label(self.window, text = 'Forward                 Backward', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_wrist_r_y.place(x = self.wb/2, y = self.h/80 + 16.9*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_wrist_r_y)
            self.range_df_wrist_r_y = [-0.6, 0.6]
            self.resolution_df_wrist_r_y = 0.1
            self.bar_df_wrist_r_y = tk.Scale(self.window, from_=self.range_df_wrist_r_y[0], to=self.range_df_wrist_r_y[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_wrist_r_y, command=self.set_bar_df_wrist_r_y, width = 10)
            self.bar_df_wrist_r_y.pack()
            self.bar_df_wrist_r_y.place(x = self.wb/2, y = self.h/80 + 17.3*self.h/20, anchor = 'n')
            self.bar_df_wrist_r_y.set(self.df_wrist_r_y)
            self.button_l_df_wrist_r_y = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_wrist_r_y)
            self.button_l_df_wrist_r_y.pack()
            self.button_l_df_wrist_r_y.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 17.6*self.h/20, anchor = 'n')
            self.button_r_df_wrist_r_y = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_wrist_r_y)
            self.button_r_df_wrist_r_y.pack()
            self.button_r_df_wrist_r_y.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 17.6*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_wrist_r_y)
            self.other_button_ids.append(self.button_l_df_wrist_r_y)
            self.other_button_ids.append(self.button_r_df_wrist_r_y)

        if value == 'Left Leg':
            lbl_df_hip_l = tk.Label(self.window, text = 'Left Hip Rotation', font = ('Arial Bold', int(self.wb/25)))
            lbl_df_hip_l.place(x = self.wb/2, y = self.h/80 + 7.8*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_hip_l)

            lbl_df_hip_l_x = tk.Label(self.window, text = 'Side Lift             Side Lower', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_hip_l_x.place(x = self.wb/2, y = self.h/80 + 8.3*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_hip_l_x)
            self.range_df_hip_l_x = [-1.8, 0.6]
            self.resolution_df_hip_l_x = 0.1
            self.bar_df_hip_l_x = tk.Scale(self.window, from_=self.range_df_hip_l_x[0], to=self.range_df_hip_l_x[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_hip_l_x, command=self.set_bar_df_hip_l_x, width = 10)
            self.bar_df_hip_l_x.pack()
            self.bar_df_hip_l_x.place(x = self.wb/2, y = self.h/80 + 8.7*self.h/20, anchor = 'n')
            self.bar_df_hip_l_x.set(self.df_hip_l_x)
            self.button_l_df_hip_l_x = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_hip_l_x)
            self.button_l_df_hip_l_x.pack()
            self.button_l_df_hip_l_x.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 9*self.h/20, anchor = 'n')
            self.button_r_df_hip_l_x = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_hip_l_x)
            self.button_r_df_hip_l_x.pack()
            self.button_r_df_hip_l_x.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 9*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_hip_l_x)
            self.other_button_ids.append(self.button_l_df_hip_l_x)
            self.other_button_ids.append(self.button_r_df_hip_l_x)

            lbl_df_hip_l_y = tk.Label(self.window, text = 'Forward                 Backward', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_hip_l_y.place(x = self.wb/2, y = self.h/80 + 9.7*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_hip_l_y)
            self.range_df_hip_l_y = [-2.8, 0.8]
            self.resolution_df_hip_l_y = 0.1
            self.bar_df_hip_l_y = tk.Scale(self.window, from_=self.range_df_hip_l_y[0], to=self.range_df_hip_l_y[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_hip_l_y, command=self.set_bar_df_hip_l_y, width = 10)
            self.bar_df_hip_l_y.pack()
            self.bar_df_hip_l_y.place(x = self.wb/2, y = self.h/80 + 10.1*self.h/20, anchor = 'n')
            self.bar_df_hip_l_y.set(self.df_hip_l_y)
            self.button_l_df_hip_l_y = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_hip_l_y)
            self.button_l_df_hip_l_y.pack()
            self.button_l_df_hip_l_y.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 10.4*self.h/20, anchor = 'n')
            self.button_r_df_hip_l_y = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_hip_l_y)
            self.button_r_df_hip_l_y.pack()
            self.button_r_df_hip_l_y.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 10.4*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_hip_l_y)
            self.other_button_ids.append(self.button_l_df_hip_l_y)
            self.other_button_ids.append(self.button_r_df_hip_l_y)

            lbl_df_hip_l_z = tk.Label(self.window, text = 'Twist In               Twist Out', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_hip_l_z.place(x = self.wb/2, y = self.h/80 + 11.1*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_hip_l_z)
            self.range_df_hip_l_z = [-1.1, 1.6]
            self.resolution_df_hip_l_z = 0.1
            self.bar_df_hip_l_z = tk.Scale(self.window, from_=self.range_df_hip_l_z[0], to=self.range_df_hip_l_z[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_hip_l_z, command=self.set_bar_df_hip_l_z, width = 10)
            self.bar_df_hip_l_z.pack()
            self.bar_df_hip_l_z.place(x = self.wb/2, y = self.h/80 + 11.5*self.h/20, anchor = 'n')
            self.bar_df_hip_l_z.set(self.df_hip_l_z)
            self.button_l_df_hip_l_z = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_hip_l_z)
            self.button_l_df_hip_l_z.pack()
            self.button_l_df_hip_l_z.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 11.8*self.h/20, anchor = 'n')
            self.button_r_df_hip_l_z = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_hip_l_z)
            self.button_r_df_hip_l_z.pack()
            self.button_r_df_hip_l_z.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 11.8*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_hip_l_z)
            self.other_button_ids.append(self.button_l_df_hip_l_z)
            self.other_button_ids.append(self.button_r_df_hip_l_z)

            lbl_df_knee_l = tk.Label(self.window, text = 'Left Knee Rotation', font = ('Arial Bold', int(self.wb/25)))
            lbl_df_knee_l.place(x = self.wb/2, y = self.h/80 + 12.8*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_knee_l)

            lbl_df_knee_l_y = tk.Label(self.window, text = 'Straighten                  Bend', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_knee_l_y.place(x = self.wb/2, y = self.h/80 + 13.3*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_knee_l_y)
            self.range_df_knee_l_y = [-0.1, 2.1]
            self.resolution_df_knee_l_y = 0.1
            self.bar_df_knee_l_y = tk.Scale(self.window, from_=self.range_df_knee_l_y[0], to=self.range_df_knee_l_y[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_knee_l_y, command=self.set_bar_df_knee_l_y, width = 10)
            self.bar_df_knee_l_y.pack()
            self.bar_df_knee_l_y.place(x = self.wb/2, y = self.h/80 + 13.7*self.h/20, anchor = 'n')
            self.bar_df_knee_l_y.set(self.df_knee_l_y)
            self.button_l_df_knee_l_y = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_knee_l_y)
            self.button_l_df_knee_l_y.pack()
            self.button_l_df_knee_l_y.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 14*self.h/20, anchor = 'n')
            self.button_r_df_knee_l_y = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_knee_l_y)
            self.button_r_df_knee_l_y.pack()
            self.button_r_df_knee_l_y.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 14*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_knee_l_y)
            self.other_button_ids.append(self.button_l_df_knee_l_y)
            self.other_button_ids.append(self.button_r_df_knee_l_y)

            lbl_df_ankle_l = tk.Label(self.window, text = 'Left Ankle Rotation', font = ('Arial Bold', int(self.wb/25)))
            lbl_df_ankle_l.place(x = self.wb/2, y = self.h/80 + 15*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_ankle_l)

            lbl_df_ankle_l_x = tk.Label(self.window, text = 'Curl Out                 Curl In', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_ankle_l_x.place(x = self.wb/2, y = self.h/80 + 15.5*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_ankle_l_x)
            self.range_df_ankle_l_x = [-1.2, 1.2]
            self.resolution_df_ankle_l_x = 0.1
            self.bar_df_ankle_l_x = tk.Scale(self.window, from_=self.range_df_ankle_l_x[0], to=self.range_df_ankle_l_x[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_ankle_l_x, command=self.set_bar_df_ankle_l_x, width = 10)
            self.bar_df_ankle_l_x.pack()
            self.bar_df_ankle_l_x.place(x = self.wb/2, y = self.h/80 + 15.9*self.h/20, anchor = 'n')
            self.bar_df_ankle_l_x.set(self.df_ankle_l_x)
            self.button_l_df_ankle_l_x = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_ankle_l_x)
            self.button_l_df_ankle_l_x.pack()
            self.button_l_df_ankle_l_x.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 16.2*self.h/20, anchor = 'n')
            self.button_r_df_ankle_l_x = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_ankle_l_x)
            self.button_r_df_ankle_l_x.pack()
            self.button_r_df_ankle_l_x.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 16.2*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_ankle_l_x)
            self.other_button_ids.append(self.button_l_df_ankle_l_x)
            self.other_button_ids.append(self.button_r_df_ankle_l_x)

            lbl_df_ankle_l_y = tk.Label(self.window, text = 'Bend                      Extend', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_ankle_l_y.place(x = self.wb/2, y = self.h/80 + 16.9*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_ankle_l_y)
            self.range_df_ankle_l_y = [-0.6, 1.6]
            self.resolution_df_ankle_l_y = 0.1
            self.bar_df_ankle_l_y = tk.Scale(self.window, from_=self.range_df_ankle_l_y[0], to=self.range_df_ankle_l_y[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_ankle_l_y, command=self.set_bar_df_ankle_l_y, width = 10)
            self.bar_df_ankle_l_y.pack()
            self.bar_df_ankle_l_y.place(x = self.wb/2, y = self.h/80 + 17.3*self.h/20, anchor = 'n')
            self.bar_df_ankle_l_y.set(self.df_ankle_l_y)
            self.button_l_df_ankle_l_y = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_ankle_l_y)
            self.button_l_df_ankle_l_y.pack()
            self.button_l_df_ankle_l_y.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 17.6*self.h/20, anchor = 'n')
            self.button_r_df_ankle_l_y = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_ankle_l_y)
            self.button_r_df_ankle_l_y.pack()
            self.button_r_df_ankle_l_y.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 17.6*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_ankle_l_y)
            self.other_button_ids.append(self.button_l_df_ankle_l_y)
            self.other_button_ids.append(self.button_r_df_ankle_l_y)

        if value == 'Right Leg':
            lbl_df_hip_r = tk.Label(self.window, text = 'Right Hip Rotation', font = ('Arial Bold', int(self.wb/25)))
            lbl_df_hip_r.place(x = self.wb/2, y = self.h/80 + 7.8*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_hip_r)

            lbl_df_hip_r_x = tk.Label(self.window, text = 'Side Lower             Side Lift', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_hip_r_x.place(x = self.wb/2, y = self.h/80 + 8.3*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_hip_r_x)
            self.range_df_hip_r_x = [-0.6, 1.8]
            self.resolution_df_hip_r_x = 0.1
            self.bar_df_hip_r_x = tk.Scale(self.window, from_=self.range_df_hip_r_x[0], to=self.range_df_hip_r_x[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_hip_r_x, command=self.set_bar_df_hip_r_x, width = 10)
            self.bar_df_hip_r_x.pack()
            self.bar_df_hip_r_x.place(x = self.wb/2, y = self.h/80 + 8.7*self.h/20, anchor = 'n')
            self.bar_df_hip_r_x.set(self.df_hip_r_x)
            self.button_l_df_hip_r_x = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_hip_r_x)
            self.button_l_df_hip_r_x.pack()
            self.button_l_df_hip_r_x.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 9*self.h/20, anchor = 'n')
            self.button_r_df_hip_r_x = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_hip_r_x)
            self.button_r_df_hip_r_x.pack()
            self.button_r_df_hip_r_x.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 9*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_hip_r_x)
            self.other_button_ids.append(self.button_l_df_hip_r_x)
            self.other_button_ids.append(self.button_r_df_hip_r_x)

            lbl_df_hip_r_y = tk.Label(self.window, text = 'Forward                 Backward', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_hip_r_y.place(x = self.wb/2, y = self.h/80 + 9.7*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_hip_r_y)
            self.range_df_hip_r_y = [-2.8, 0.8]
            self.resolution_df_hip_r_y = 0.1
            self.bar_df_hip_r_y = tk.Scale(self.window, from_=self.range_df_hip_r_y[0], to=self.range_df_hip_r_y[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_hip_r_y, command=self.set_bar_df_hip_r_y, width = 10)
            self.bar_df_hip_r_y.pack()
            self.bar_df_hip_r_y.place(x = self.wb/2, y = self.h/80 + 10.1*self.h/20, anchor = 'n')
            self.bar_df_hip_r_y.set(self.df_hip_r_y)
            self.button_l_df_hip_r_y = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_hip_r_y)
            self.button_l_df_hip_r_y.pack()
            self.button_l_df_hip_r_y.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 10.4*self.h/20, anchor = 'n')
            self.button_r_df_hip_r_y = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_hip_r_y)
            self.button_r_df_hip_r_y.pack()
            self.button_r_df_hip_r_y.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 10.4*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_hip_r_y)
            self.other_button_ids.append(self.button_l_df_hip_r_y)
            self.other_button_ids.append(self.button_r_df_hip_r_y)

            lbl_df_hip_r_z = tk.Label(self.window, text = 'Twist Out               Twist In', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_hip_r_z.place(x = self.wb/2, y = self.h/80 + 11.1*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_hip_r_z)
            self.range_df_hip_r_z = [-1.6, 1.1]
            self.resolution_df_hip_r_z = 0.1
            self.bar_df_hip_r_z = tk.Scale(self.window, from_=self.range_df_hip_r_z[0], to=self.range_df_hip_r_z[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_hip_r_z, command=self.set_bar_df_hip_r_z, width = 10)
            self.bar_df_hip_r_z.pack()
            self.bar_df_hip_r_z.place(x = self.wb/2, y = self.h/80 + 11.5*self.h/20, anchor = 'n')
            self.bar_df_hip_r_z.set(self.df_hip_r_z)
            self.button_l_df_hip_r_z = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_hip_r_z)
            self.button_l_df_hip_r_z.pack()
            self.button_l_df_hip_r_z.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 11.8*self.h/20, anchor = 'n')
            self.button_r_df_hip_r_z = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_hip_r_z)
            self.button_r_df_hip_r_z.pack()
            self.button_r_df_hip_r_z.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 11.8*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_hip_r_z)
            self.other_button_ids.append(self.button_l_df_hip_r_z)
            self.other_button_ids.append(self.button_r_df_hip_r_z)

            lbl_df_knee_r = tk.Label(self.window, text = 'Right Knee Rotation', font = ('Arial Bold', int(self.wb/25)))
            lbl_df_knee_r.place(x = self.wb/2, y = self.h/80 + 12.8*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_knee_r)

            lbl_df_knee_r_y = tk.Label(self.window, text = 'Straighten                  Bend', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_knee_r_y.place(x = self.wb/2, y = self.h/80 + 13.3*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_knee_r_y)
            self.range_df_knee_r_y = [-0.1, 2.1]
            self.resolution_df_knee_r_y = 0.1
            self.bar_df_knee_r_y = tk.Scale(self.window, from_=self.range_df_knee_r_y[0], to=self.range_df_knee_r_y[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_knee_r_y, command=self.set_bar_df_knee_r_y, width = 10)
            self.bar_df_knee_r_y.pack()
            self.bar_df_knee_r_y.place(x = self.wb/2, y = self.h/80 + 13.7*self.h/20, anchor = 'n')
            self.bar_df_knee_r_y.set(self.df_knee_r_y)
            self.button_l_df_knee_r_y = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_knee_r_y)
            self.button_l_df_knee_r_y.pack()
            self.button_l_df_knee_r_y.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 14*self.h/20, anchor = 'n')
            self.button_r_df_knee_r_y = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_knee_r_y)
            self.button_r_df_knee_r_y.pack()
            self.button_r_df_knee_r_y.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 14*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_knee_r_y)
            self.other_button_ids.append(self.button_l_df_knee_r_y)
            self.other_button_ids.append(self.button_r_df_knee_r_y)

            lbl_df_ankle_r = tk.Label(self.window, text = 'Right Ankle Rotation', font = ('Arial Bold', int(self.wb/25)))
            lbl_df_ankle_r.place(x = self.wb/2, y = self.h/80 + 15*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_ankle_r)

            lbl_df_ankle_r_x = tk.Label(self.window, text = 'Curl In                 Curl Out', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_ankle_r_x.place(x = self.wb/2, y = self.h/80 + 15.5*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_ankle_r_x)
            self.range_df_ankle_r_x = [-1.2, 1.2]
            self.resolution_df_ankle_r_x = 0.1
            self.bar_df_ankle_r_x = tk.Scale(self.window, from_=self.range_df_ankle_r_x[0], to=self.range_df_ankle_r_x[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_ankle_r_x, command=self.set_bar_df_ankle_r_x, width = 10)
            self.bar_df_ankle_r_x.pack()
            self.bar_df_ankle_r_x.place(x = self.wb/2, y = self.h/80 + 15.9*self.h/20, anchor = 'n')
            self.bar_df_ankle_r_x.set(self.df_ankle_r_x)
            self.button_l_df_ankle_r_x = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_ankle_r_x)
            self.button_l_df_ankle_r_x.pack()
            self.button_l_df_ankle_r_x.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 16.2*self.h/20, anchor = 'n')
            self.button_r_df_ankle_r_x = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_ankle_r_x)
            self.button_r_df_ankle_r_x.pack()
            self.button_r_df_ankle_r_x.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 16.2*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_ankle_r_x)
            self.other_button_ids.append(self.button_l_df_ankle_r_x)
            self.other_button_ids.append(self.button_r_df_ankle_r_x)

            lbl_df_ankle_r_y = tk.Label(self.window, text = 'Bend                      Extend', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_ankle_r_y.place(x = self.wb/2, y = self.h/80 + 16.9*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_ankle_r_y)
            self.range_df_ankle_r_y = [-0.6, 1.6]
            self.resolution_df_ankle_r_y = 0.1
            self.bar_df_ankle_r_y = tk.Scale(self.window, from_=self.range_df_ankle_r_y[0], to=self.range_df_ankle_r_y[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_ankle_r_y, command=self.set_bar_df_ankle_r_y, width = 10)
            self.bar_df_ankle_r_y.pack()
            self.bar_df_ankle_r_y.place(x = self.wb/2, y = self.h/80 + 17.3*self.h/20, anchor = 'n')
            self.bar_df_ankle_r_y.set(self.df_ankle_r_y)
            self.button_l_df_ankle_r_y = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_ankle_r_y)
            self.button_l_df_ankle_r_y.pack()
            self.button_l_df_ankle_r_y.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 17.6*self.h/20, anchor = 'n')
            self.button_r_df_ankle_r_y = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_ankle_r_y)
            self.button_r_df_ankle_r_y.pack()
            self.button_r_df_ankle_r_y.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 17.6*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_ankle_r_y)
            self.other_button_ids.append(self.button_l_df_ankle_r_y)
            self.other_button_ids.append(self.button_r_df_ankle_r_y)

        if value == 'Hands and Feet':
            lbl_df_hand = tk.Label(self.window, text = 'Hand Rotation', font = ('Arial Bold', int(self.wb/25)))
            lbl_df_hand.place(x = self.wb/2, y = self.h/80 + 7.8*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_hand)

            lbl_df_hand_l_x = tk.Label(self.window, text = 'Extend Left            Bend Left', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_hand_l_x.place(x = self.wb/2, y = self.h/80 + 8.3*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_hand_l_x)
            self.range_df_hand_l_x = [-0.3, 2.6]
            self.resolution_df_hand_l_x = 0.1
            self.bar_df_hand_l_x = tk.Scale(self.window, from_=self.range_df_hand_l_x[0], to=self.range_df_hand_l_x[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_hand_l_x, command=self.set_bar_df_hand_l_x, width = 10)
            self.bar_df_hand_l_x.pack()
            self.bar_df_hand_l_x.place(x = self.wb/2, y = self.h/80 + 8.7*self.h/20, anchor = 'n')
            self.bar_df_hand_l_x.set(self.df_hand_l_x)
            self.button_l_df_hand_l_x = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_hand_l_x)
            self.button_l_df_hand_l_x.pack()
            self.button_l_df_hand_l_x.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 9*self.h/20, anchor = 'n')
            self.button_r_df_hand_l_x = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_hand_l_x)
            self.button_r_df_hand_l_x.pack()
            self.button_r_df_hand_l_x.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 9*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_hand_l_x)
            self.other_button_ids.append(self.button_l_df_hand_l_x)
            self.other_button_ids.append(self.button_r_df_hand_l_x)

            lbl_df_hand_r_x = tk.Label(self.window, text = 'Bend Right          Extend Right', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_hand_r_x.place(x = self.wb/2, y = self.h/80 + 9.7*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_hand_r_x)
            self.range_df_hand_r_x = [-2.6, 0.3]
            self.resolution_df_hand_r_x = 0.1
            self.bar_df_hand_r_x = tk.Scale(self.window, from_=self.range_df_hand_r_x[0], to=self.range_df_hand_r_x[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_hand_r_x, command=self.set_bar_df_hand_r_x, width = 10)
            self.bar_df_hand_r_x.pack()
            self.bar_df_hand_r_x.place(x = self.wb/2, y = self.h/80 + 10.1*self.h/20, anchor = 'n')
            self.bar_df_hand_r_x.set(self.df_hand_r_x)
            self.button_l_df_hand_r_x = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_hand_r_x)
            self.button_l_df_hand_r_x.pack()
            self.button_l_df_hand_r_x.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 10.4*self.h/20, anchor = 'n')
            self.button_r_df_hand_r_x = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_hand_r_x)
            self.button_r_df_hand_r_x.pack()
            self.button_r_df_hand_r_x.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 10.4*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_hand_r_x)
            self.other_button_ids.append(self.button_l_df_hand_r_x)
            self.other_button_ids.append(self.button_r_df_hand_r_x)

            lbl_df_foot = tk.Label(self.window, text = 'Foot Rotation', font = ('Arial Bold', int(self.wb/25)))
            lbl_df_foot.place(x = self.wb/2, y = self.h/80 + 11.4*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_foot)

            lbl_df_foot_l_y = tk.Label(self.window, text = 'Bend Back Left      Curl In Left', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_foot_l_y.place(x = self.wb/2, y = self.h/80 + 11.9*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_foot_l_y)
            self.range_df_foot_l_y = [-1.6, 1.6]
            self.resolution_df_foot_l_y = 0.1
            self.bar_df_foot_l_y = tk.Scale(self.window, from_=self.range_df_foot_l_y[0], to=self.range_df_foot_l_y[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_foot_l_y, command=self.set_bar_df_foot_l_y, width = 10)
            self.bar_df_foot_l_y.pack()
            self.bar_df_foot_l_y.place(x = self.wb/2, y = self.h/80 + 12.3*self.h/20, anchor = 'n')
            self.bar_df_foot_l_y.set(self.df_foot_l_y)
            self.button_l_df_foot_l_y = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_foot_l_y)
            self.button_l_df_foot_l_y.pack()
            self.button_l_df_foot_l_y.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 12.6*self.h/20, anchor = 'n')
            self.button_r_df_foot_l_y = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_foot_l_y)
            self.button_r_df_foot_l_y.pack()
            self.button_r_df_foot_l_y.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 12.6*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_foot_l_y)
            self.other_button_ids.append(self.button_l_df_foot_l_y)
            self.other_button_ids.append(self.button_r_df_foot_l_y)

            lbl_df_foot_r_y = tk.Label(self.window, text = 'Bend Back Right    Curl In Right', font = ('Arial Bold', int(self.wb/32)))
            lbl_df_foot_r_y.place(x = self.wb/2, y = self.h/80 + 13.3*self.h/20, anchor = 'n')
            self.other_button_ids.append(lbl_df_foot_r_y)
            self.range_df_foot_r_y = [-1.6, 1.6]
            self.resolution_df_foot_r_y = 0.1
            self.bar_df_foot_r_y = tk.Scale(self.window, from_=self.range_df_foot_r_y[0], to=self.range_df_foot_r_y[1], orient=tk.HORIZONTAL, length=self.bar_width, resolution=self.resolution_df_foot_r_y, command=self.set_bar_df_foot_r_y, width = 10)
            self.bar_df_foot_r_y.pack()
            self.bar_df_foot_r_y.place(x = self.wb/2, y = self.h/80 + 13.7*self.h/20, anchor = 'n')
            self.bar_df_foot_r_y.set(self.df_foot_r_y)
            self.button_l_df_foot_r_y = tk.Button(self.window, text='<==', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_l_df_foot_r_y)
            self.button_l_df_foot_r_y.pack()
            self.button_l_df_foot_r_y.place(x = self.wb/2 - 1.2*self.bar_width/2, y = self.h/80 + 14*self.h/20, anchor = 'n')
            self.button_r_df_foot_r_y = tk.Button(self.window, text='==>', font = ('Arial Bold', int(self.wb/35)), command=self.set_button_r_df_foot_r_y)
            self.button_r_df_foot_r_y.pack()
            self.button_r_df_foot_r_y.place(x = self.wb/2 + 1.2*self.bar_width/2, y = self.h/80 + 14*self.h/20, anchor = 'n')
            self.other_button_ids.append(self.bar_df_foot_r_y)
            self.other_button_ids.append(self.button_l_df_foot_r_y)
            self.other_button_ids.append(self.button_r_df_foot_r_y)

    def set_bar_df_core_x(self, event):
        self.df_core_x = self.bar_df_core_x.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_core_x(self):
        if self.bar_df_core_x.get() - self.resolution_df_core_x >= 1.01*self.range_df_core_x[0]:
            self.df_core_x += -self.resolution_df_core_x
            self.bar_df_core_x.set(self.df_core_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_core_x(self):
        if self.df_core_x + self.resolution_df_core_x <= 1.01*self.range_df_core_x[1]:
            self.df_core_x += self.resolution_df_core_x
            self.bar_df_core_x.set(self.df_core_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_core_y(self, event):
        self.df_core_y = self.bar_df_core_y.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_core_y(self):
        if self.bar_df_core_y.get() - self.resolution_df_core_y >= 1.01*self.range_df_core_y[0]:
            self.df_core_y += -self.resolution_df_core_y
            self.bar_df_core_y.set(self.df_core_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_core_y(self):
        if self.bar_df_core_y.get() + self.resolution_df_core_y <= 1.01*self.range_df_core_y[1]:
            self.df_core_y += self.resolution_df_core_y
            self.bar_df_core_y.set(self.df_core_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_core_z(self, event):
        self.df_core_z = self.bar_df_core_z.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_core_z(self):
        if self.bar_df_core_z.get() - self.resolution_df_core_z >= 1.01*self.range_df_core_z[0]:
            self.df_core_z += -self.resolution_df_core_z
            self.bar_df_core_z.set(self.df_core_z)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_core_z(self):
        if self.bar_df_core_z.get() + self.resolution_df_core_z <= 1.01*self.range_df_core_z[1]:
            self.df_core_z += self.resolution_df_core_z
            self.bar_df_core_z.set(self.df_core_z)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_head_y(self, event):
        self.df_head_y = self.bar_df_head_y.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_head_y(self):
        if self.bar_df_head_y.get() - self.resolution_df_head_y >= 1.01*self.range_df_head_y[0]:
            self.df_head_y += -self.resolution_df_head_y
            self.bar_df_head_y.set(self.df_head_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_head_y(self):
        if self.bar_df_head_y.get() + self.resolution_df_head_y <= 1.01*self.range_df_head_y[1]:
            self.df_head_y += self.resolution_df_head_y
            self.bar_df_head_y.set(self.df_head_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_neck_x(self, event):
        self.df_neck_x = self.bar_df_neck_x.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_neck_x(self):
        if self.bar_df_neck_x.get() - self.resolution_df_neck_x >= 1.01*self.range_df_neck_x[0]:
            self.df_neck_x += -self.resolution_df_neck_x
            self.bar_df_neck_x.set(self.df_neck_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_neck_x(self):
        if self.bar_df_neck_x.get() + self.resolution_df_neck_x <= 1.01*self.range_df_neck_x[1]:
            self.df_neck_x += self.resolution_df_neck_x
            self.bar_df_neck_x.set(self.df_neck_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_neck_y(self, event):
        self.df_neck_y = self.bar_df_neck_y.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_neck_y(self):
        if self.bar_df_neck_y.get() - self.resolution_df_neck_y >= 1.01*self.range_df_neck_y[0]:
            self.df_neck_y += -self.resolution_df_neck_y
            self.bar_df_neck_y.set(self.df_neck_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_neck_y(self):
        if self.bar_df_neck_y.get() + self.resolution_df_neck_y <= 1.01*self.range_df_neck_y[1]:
            self.df_neck_y += self.resolution_df_neck_y
            self.bar_df_neck_y.set(self.df_neck_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_neck_z(self, event):
        self.df_neck_z = self.bar_df_neck_z.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_neck_z(self):
        if self.bar_df_neck_z.get() - self.resolution_df_neck_z >= 1.01*self.range_df_neck_z[0]:
            self.df_neck_z += -self.resolution_df_neck_z
            self.bar_df_neck_z.set(self.df_neck_z)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_neck_z(self):
        if self.bar_df_neck_z.get() + self.resolution_df_neck_z <= 1.01*self.range_df_neck_z[1]:
            self.df_neck_z += self.resolution_df_neck_z
            self.bar_df_neck_z.set(self.df_neck_z)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_lb_y(self, event):
        self.df_lb_y = self.bar_df_lb_y.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_lb_y(self):
        if self.bar_df_lb_y.get() - self.resolution_df_lb_y >= 1.01*self.range_df_lb_y[0]:
            self.df_lb_y += -self.resolution_df_lb_y
            self.bar_df_lb_y.set(self.df_lb_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_lb_y(self):
        if self.bar_df_lb_y.get() + self.resolution_df_lb_y <= 1.01*self.range_df_lb_y[1]:
            self.df_lb_y += self.resolution_df_lb_y
            self.bar_df_lb_y.set(self.df_lb_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_lb_z(self, event):
        self.df_lb_z = self.bar_df_lb_z.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_lb_z(self):
        if self.bar_df_lb_z.get() - self.resolution_df_lb_z >= 1.01*self.range_df_lb_z[0]:
            self.df_lb_z += -self.resolution_df_lb_z
            self.bar_df_lb_z.set(self.df_lb_z)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_lb_z(self):
        if self.bar_df_lb_z.get() + self.resolution_df_lb_z <= 1.01*self.range_df_lb_z[1]:
            self.df_lb_z += self.resolution_df_lb_z
            self.bar_df_lb_z.set(self.df_lb_z)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_shoulder_l_x(self, event):
        self.df_shoulder_l_x = self.bar_df_shoulder_l_x.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_shoulder_l_x(self):
        if self.bar_df_shoulder_l_x.get() - self.resolution_df_shoulder_l_x >= 1.01*self.range_df_shoulder_l_x[0]:
            self.df_shoulder_l_x += -self.resolution_df_shoulder_l_x
            self.bar_df_shoulder_l_x.set(self.df_shoulder_l_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_shoulder_l_x(self):
        if self.bar_df_shoulder_l_x.get() + self.resolution_df_shoulder_l_x <= 1.01*self.range_df_shoulder_l_x[1]:
            self.df_shoulder_l_x += self.resolution_df_shoulder_l_x
            self.bar_df_shoulder_l_x.set(self.df_shoulder_l_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_shoulder_l_z(self, event):
        self.df_shoulder_l_z = self.bar_df_shoulder_l_z.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_shoulder_l_z(self):
        if self.bar_df_shoulder_l_z.get() - self.resolution_df_shoulder_l_z >= 1.01*self.range_df_shoulder_l_z[0]:
            self.df_shoulder_l_z += -self.resolution_df_shoulder_l_z
            self.bar_df_shoulder_l_z.set(self.df_shoulder_l_z)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_shoulder_l_z(self):
        if self.bar_df_shoulder_l_z.get() + self.resolution_df_shoulder_l_z <= 1.01*self.range_df_shoulder_l_z[1]:
            self.df_shoulder_l_z += self.resolution_df_shoulder_l_z
            self.bar_df_shoulder_l_z.set(self.df_shoulder_l_z)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_shoulder_r_x(self, event):
        self.df_shoulder_r_x = self.bar_df_shoulder_r_x.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_shoulder_r_x(self):
        if self.bar_df_shoulder_r_x.get() - self.resolution_df_shoulder_r_x >= 1.01*self.range_df_shoulder_r_x[0]:
            self.df_shoulder_r_x += -self.resolution_df_shoulder_r_x
            self.bar_df_shoulder_r_x.set(self.df_shoulder_r_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_shoulder_r_x(self):
        if self.bar_df_shoulder_r_x.get() + self.resolution_df_shoulder_r_x <= 1.01*self.range_df_shoulder_r_x[1]:
            self.df_shoulder_r_x += self.resolution_df_shoulder_r_x
            self.bar_df_shoulder_r_x.set(self.df_shoulder_r_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_shoulder_r_z(self, event):
        self.df_shoulder_r_z = self.bar_df_shoulder_r_z.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_shoulder_r_z(self):
        if self.bar_df_shoulder_r_z.get() - self.resolution_df_shoulder_r_z >= 1.01*self.range_df_shoulder_r_z[0]:
            self.df_shoulder_r_z += -self.resolution_df_shoulder_r_z
            self.bar_df_shoulder_r_z.set(self.df_shoulder_r_z)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_shoulder_r_z(self):
        if self.bar_df_shoulder_r_z.get() + self.resolution_df_shoulder_r_z <= 1.01*self.range_df_shoulder_r_z[1]:
            self.df_shoulder_r_z += self.resolution_df_shoulder_r_z
            self.bar_df_shoulder_r_z.set(self.df_shoulder_r_z)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_ua_l_x(self, event):
        self.df_ua_l_x = self.bar_df_ua_l_x.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_ua_l_x(self):
        if self.bar_df_ua_l_x.get() - self.resolution_df_ua_l_x >= 1.01*self.range_df_ua_l_x[0]:
            self.df_ua_l_x += -self.resolution_df_ua_l_x
            self.bar_df_ua_l_x.set(self.df_ua_l_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_ua_l_x(self):
        if self.bar_df_ua_l_x.get() + self.resolution_df_ua_l_x <= 1.01*self.range_df_ua_l_x[1]:
            self.df_ua_l_x += self.resolution_df_ua_l_x
            self.bar_df_ua_l_x.set(self.df_ua_l_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_ua_l_y(self, event):
        self.df_ua_l_y = self.bar_df_ua_l_y.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_ua_l_y(self):
        if self.bar_df_ua_l_y.get() - self.resolution_df_ua_l_y >= 1.01*self.range_df_ua_l_y[0]:
            self.df_ua_l_y += -self.resolution_df_ua_l_y
            self.bar_df_ua_l_y.set(self.df_ua_l_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_ua_l_y(self):
        if self.bar_df_ua_l_y.get() + self.resolution_df_ua_l_y <= 1.01*self.range_df_ua_l_y[1]:
            self.df_ua_l_y += self.resolution_df_ua_l_y
            self.bar_df_ua_l_y.set(self.df_ua_l_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_elbow_l_y(self, event):
        self.df_elbow_l_y = self.bar_df_elbow_l_y.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_elbow_l_y(self):
        if self.bar_df_elbow_l_y.get() - self.resolution_df_elbow_l_y >= 1.01*self.range_df_elbow_l_y[0]:
            self.df_elbow_l_y += -self.resolution_df_elbow_l_y
            self.bar_df_elbow_l_y.set(self.df_elbow_l_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_elbow_l_y(self):
        if self.bar_df_elbow_l_y.get() + self.resolution_df_elbow_l_y <= 1.01*self.range_df_elbow_l_y[1]:
            self.df_elbow_l_y += self.resolution_df_elbow_l_y
            self.bar_df_elbow_l_y.set(self.df_elbow_l_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_elbow_l_z(self, event):
        self.df_elbow_l_z = self.bar_df_elbow_l_z.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_elbow_l_z(self):
        if self.bar_df_elbow_l_z.get() - self.resolution_df_elbow_l_z >= 1.01*self.range_df_elbow_l_z[0]:
            self.df_elbow_l_z += -self.resolution_df_elbow_l_z
            self.bar_df_elbow_l_z.set(self.df_elbow_l_z)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_elbow_l_z(self):
        if self.bar_df_elbow_l_z.get() + self.resolution_df_elbow_l_z <= 1.01*self.range_df_elbow_l_z[1]:
            self.df_elbow_l_z += self.resolution_df_elbow_l_z
            self.bar_df_elbow_l_z.set(self.df_elbow_l_z)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_wrist_l_x(self, event):
        self.df_wrist_l_x = self.bar_df_wrist_l_x.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_wrist_l_x(self):
        if self.bar_df_wrist_l_x.get() - self.resolution_df_wrist_l_x >= 1.01*self.range_df_wrist_l_x[0]:
            self.df_wrist_l_x += -self.resolution_df_wrist_l_x
            self.bar_df_wrist_l_x.set(self.df_wrist_l_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_wrist_l_x(self):
        if self.bar_df_wrist_l_x.get() + self.resolution_df_wrist_l_x <= 1.01*self.range_df_wrist_l_x[1]:
            self.df_wrist_l_x += self.resolution_df_wrist_l_x
            self.bar_df_wrist_l_x.set(self.df_wrist_l_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_wrist_l_y(self, event):
        self.df_wrist_l_y = self.bar_df_wrist_l_y.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_wrist_l_y(self):
        if self.bar_df_wrist_l_y.get() - self.resolution_df_wrist_l_y >= 1.01*self.range_df_wrist_l_y[0]:
            self.df_wrist_l_y += -self.resolution_df_wrist_l_y
            self.bar_df_wrist_l_y.set(self.df_wrist_l_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_wrist_l_y(self):
        if self.bar_df_wrist_l_y.get() + self.resolution_df_wrist_l_y <= 1.01*self.range_df_wrist_l_y[1]:
            self.df_wrist_l_y += self.resolution_df_wrist_l_y
            self.bar_df_wrist_l_y.set(self.df_wrist_l_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_ua_r_x(self, event):
        self.df_ua_r_x = self.bar_df_ua_r_x.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_ua_r_x(self):
        if self.bar_df_ua_r_x.get() - self.resolution_df_ua_r_x >= 1.01*self.range_df_ua_r_x[0]:
            self.df_ua_r_x += -self.resolution_df_ua_r_x
            self.bar_df_ua_r_x.set(self.df_ua_r_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_ua_r_x(self):
        if self.bar_df_ua_r_x.get() + self.resolution_df_ua_r_x <= 1.01*self.range_df_ua_r_x[1]:
            self.df_ua_r_x += self.resolution_df_ua_r_x
            self.bar_df_ua_r_x.set(self.df_ua_r_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_ua_r_y(self, event):
        self.df_ua_r_y = self.bar_df_ua_r_y.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_ua_r_y(self):
        if self.bar_df_ua_r_y.get() - self.resolution_df_ua_r_y >= 1.01*self.range_df_ua_r_y[0]:
            self.df_ua_r_y += -self.resolution_df_ua_r_y
            self.bar_df_ua_r_y.set(self.df_ua_r_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_ua_r_y(self):
        if self.bar_df_ua_r_y.get() + self.resolution_df_ua_r_y <= 1.01*self.range_df_ua_r_y[1]:
            self.df_ua_r_y += self.resolution_df_ua_r_y
            self.bar_df_ua_r_y.set(self.df_ua_r_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_elbow_r_y(self, event):
        self.df_elbow_r_y = self.bar_df_elbow_r_y.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_elbow_r_y(self):
        if self.bar_df_elbow_r_y.get() - self.resolution_df_elbow_r_y >= 1.01*self.range_df_elbow_r_y[0]:
            self.df_elbow_r_y += -self.resolution_df_elbow_r_y
            self.bar_df_elbow_r_y.set(self.df_elbow_r_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_elbow_r_y(self):
        if self.bar_df_elbow_r_y.get() + self.resolution_df_elbow_r_y <= 1.01*self.range_df_elbow_r_y[1]:
            self.df_elbow_r_y += self.resolution_df_elbow_r_y
            self.bar_df_elbow_r_y.set(self.df_elbow_r_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_elbow_r_z(self, event):
        self.df_elbow_r_z = self.bar_df_elbow_r_z.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_elbow_r_z(self):
        if self.bar_df_elbow_r_z.get() - self.resolution_df_elbow_r_z >= 1.01*self.range_df_elbow_r_z[0]:
            self.df_elbow_r_z += -self.resolution_df_elbow_r_z
            self.bar_df_elbow_r_z.set(self.df_elbow_r_z)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_elbow_r_z(self):
        if self.bar_df_elbow_r_z.get() + self.resolution_df_elbow_r_z <= 1.01*self.range_df_elbow_r_z[1]:
            self.df_elbow_r_z += self.resolution_df_elbow_r_z
            self.bar_df_elbow_r_z.set(self.df_elbow_r_z)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_wrist_r_x(self, event):
        self.df_wrist_r_x = self.bar_df_wrist_r_x.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_wrist_r_x(self):
        if self.bar_df_wrist_r_x.get() - self.resolution_df_wrist_r_x >= 1.01*self.range_df_wrist_r_x[0]:
            self.df_wrist_r_x += -self.resolution_df_wrist_r_x
            self.bar_df_wrist_r_x.set(self.df_wrist_r_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_wrist_r_x(self):
        if self.bar_df_wrist_r_x.get() + self.resolution_df_wrist_r_x <= 1.01*self.range_df_wrist_r_x[1]:
            self.df_wrist_r_x += self.resolution_df_wrist_r_x
            self.bar_df_wrist_r_x.set(self.df_wrist_r_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_wrist_r_y(self, event):
        self.df_wrist_r_y = self.bar_df_wrist_r_y.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_wrist_r_y(self):
        if self.bar_df_wrist_r_y.get() - self.resolution_df_wrist_r_y >= 1.01*self.range_df_wrist_r_y[0]:
            self.df_wrist_r_y += -self.resolution_df_wrist_r_y
            self.bar_df_wrist_r_y.set(self.df_wrist_r_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_wrist_r_y(self):
        if self.bar_df_wrist_r_y.get() + self.resolution_df_wrist_r_y <= 1.01*self.range_df_wrist_r_y[1]:
            self.df_wrist_r_y += self.resolution_df_wrist_r_y
            self.bar_df_wrist_r_y.set(self.df_wrist_r_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_hip_l_x(self, event):
        self.df_hip_l_x = self.bar_df_hip_l_x.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_hip_l_x(self):
        if self.bar_df_hip_l_x.get() - self.resolution_df_hip_l_x >= 1.01*self.range_df_hip_l_x[0]:
            self.df_hip_l_x += -self.resolution_df_hip_l_x
            self.bar_df_hip_l_x.set(self.df_hip_l_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_hip_l_x(self):
        if self.bar_df_hip_l_x.get() + self.resolution_df_hip_l_x <= 1.01*self.range_df_hip_l_x[1]:
            self.df_hip_l_x += self.resolution_df_hip_l_x
            self.bar_df_hip_l_x.set(self.df_hip_l_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_hip_l_y(self, event):
        self.df_hip_l_y = self.bar_df_hip_l_y.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_hip_l_y(self):
        if self.bar_df_hip_l_y.get() - self.resolution_df_hip_l_y >= 1.01*self.range_df_hip_l_y[0]:
            self.df_hip_l_y += -self.resolution_df_hip_l_y
            self.bar_df_hip_l_y.set(self.df_hip_l_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_hip_l_y(self):
        if self.bar_df_hip_l_y.get() + self.resolution_df_hip_l_y <= 1.01*self.range_df_hip_l_y[1]:
            self.df_hip_l_y += self.resolution_df_hip_l_y
            self.bar_df_hip_l_y.set(self.df_hip_l_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_hip_l_z(self, event):
        self.df_hip_l_z = self.bar_df_hip_l_z.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_hip_l_z(self):
        if self.bar_df_hip_l_z.get() - self.resolution_df_hip_l_z >= 1.01*self.range_df_hip_l_z[0]:
            self.df_hip_l_z += -self.resolution_df_hip_l_z
            self.bar_df_hip_l_z.set(self.df_hip_l_z)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_hip_l_z(self):
        if self.bar_df_hip_l_z.get() + self.resolution_df_hip_l_z <= 1.01*self.range_df_hip_l_z[1]:
            self.df_hip_l_z += self.resolution_df_hip_l_z
            self.bar_df_hip_l_z.set(self.df_hip_l_z)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_knee_l_y(self, event):
        self.df_knee_l_y = self.bar_df_knee_l_y.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_knee_l_y(self):
        if self.bar_df_knee_l_y.get() - self.resolution_df_knee_l_y >= 1.01*self.range_df_knee_l_y[0]:
            self.df_knee_l_y += -self.resolution_df_knee_l_y
            self.bar_df_knee_l_y.set(self.df_knee_l_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_knee_l_y(self):
        if self.bar_df_knee_l_y.get() + self.resolution_df_knee_l_y <= 1.01*self.range_df_knee_l_y[1]:
            self.df_knee_l_y += self.resolution_df_knee_l_y
            self.bar_df_knee_l_y.set(self.df_knee_l_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_ankle_l_x(self, event):
        self.df_ankle_l_x = self.bar_df_ankle_l_x.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_ankle_l_x(self):
        if self.bar_df_ankle_l_x.get() - self.resolution_df_ankle_l_x >= 1.01*self.range_df_ankle_l_x[0]:
            self.df_ankle_l_x += -self.resolution_df_ankle_l_x
            self.bar_df_ankle_l_x.set(self.df_ankle_l_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_ankle_l_x(self):
        if self.bar_df_ankle_l_x.get() + self.resolution_df_ankle_l_x <= 1.01*self.range_df_ankle_l_x[1]:
            self.df_ankle_l_x += self.resolution_df_ankle_l_x
            self.bar_df_ankle_l_x.set(self.df_ankle_l_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_ankle_l_y(self, event):
        self.df_ankle_l_y = self.bar_df_ankle_l_y.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_ankle_l_y(self):
        if self.bar_df_ankle_l_y.get() - self.resolution_df_ankle_l_y >= 1.01*self.range_df_ankle_l_y[0]:
            self.df_ankle_l_y += -self.resolution_df_ankle_l_y
            self.bar_df_ankle_l_y.set(self.df_ankle_l_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_ankle_l_y(self):
        if self.bar_df_ankle_l_y.get() + self.resolution_df_ankle_l_y <= 1.01*self.range_df_ankle_l_y[1]:
            self.df_ankle_l_y += self.resolution_df_ankle_l_y
            self.bar_df_ankle_l_y.set(self.df_ankle_l_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_hip_r_x(self, event):
        self.df_hip_r_x = self.bar_df_hip_r_x.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_hip_r_x(self):
        if self.bar_df_hip_r_x.get() - self.resolution_df_hip_r_x >= 1.01*self.range_df_hip_r_x[0]:
            self.df_hip_r_x += -self.resolution_df_hip_r_x
            self.bar_df_hip_r_x.set(self.df_hip_r_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_hip_r_x(self):
        if self.bar_df_hip_r_x.get() + self.resolution_df_hip_r_x <= 1.01*self.range_df_hip_r_x[1]:
            self.df_hip_r_x += self.resolution_df_hip_r_x
            self.bar_df_hip_r_x.set(self.df_hip_r_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_hip_r_y(self, event):
        self.df_hip_r_y = self.bar_df_hip_r_y.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_hip_r_y(self):
        if self.bar_df_hip_r_y.get() - self.resolution_df_hip_r_y >= 1.01*self.range_df_hip_r_y[0]:
            self.df_hip_r_y += -self.resolution_df_hip_r_y
            self.bar_df_hip_r_y.set(self.df_hip_r_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_hip_r_y(self):
        if self.bar_df_hip_r_y.get() + self.resolution_df_hip_r_y <= 1.01*self.range_df_hip_r_y[1]:
            self.df_hip_r_y += self.resolution_df_hip_r_y
            self.bar_df_hip_r_y.set(self.df_hip_r_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_hip_r_z(self, event):
        self.df_hip_r_z = self.bar_df_hip_r_z.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_hip_r_z(self):
        if self.bar_df_hip_r_z.get() - self.resolution_df_hip_r_z >= 1.01*self.range_df_hip_r_z[0]:
            self.df_hip_r_z += -self.resolution_df_hip_r_z
            self.bar_df_hip_r_z.set(self.df_hip_r_z)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_hip_r_z(self):
        if self.bar_df_hip_r_z.get() + self.resolution_df_hip_r_z <= 1.01*self.range_df_hip_r_z[1]:
            self.df_hip_r_z += self.resolution_df_hip_r_z
            self.bar_df_hip_r_z.set(self.df_hip_r_z)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_knee_r_y(self, event):
        self.df_knee_r_y = self.bar_df_knee_r_y.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_knee_r_y(self):
        if self.bar_df_knee_r_y.get() - self.resolution_df_knee_r_y >= 1.01*self.range_df_knee_r_y[0]:
            self.df_knee_r_y += -self.resolution_df_knee_r_y
            self.bar_df_knee_r_y.set(self.df_knee_r_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_knee_r_y(self):
        if self.bar_df_knee_r_y.get() + self.resolution_df_knee_r_y <= 1.01*self.range_df_knee_r_y[1]:
            self.df_knee_r_y += self.resolution_df_knee_r_y
            self.bar_df_knee_r_y.set(self.df_knee_r_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_ankle_r_x(self, event):
        self.df_ankle_r_x = self.bar_df_ankle_r_x.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_ankle_r_x(self):
        if self.bar_df_ankle_r_x.get() - self.resolution_df_ankle_r_x >= 1.01*self.range_df_ankle_r_x[0]:
            self.df_ankle_r_x += -self.resolution_df_ankle_r_x
            self.bar_df_ankle_r_x.set(self.df_ankle_r_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_ankle_r_x(self):
        if self.bar_df_ankle_r_x.get() + self.resolution_df_ankle_r_x <= 1.01*self.range_df_ankle_r_x[1]:
            self.df_ankle_r_x += self.resolution_df_ankle_r_x
            self.bar_df_ankle_r_x.set(self.df_ankle_r_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_ankle_r_y(self, event):
        self.df_ankle_r_y = self.bar_df_ankle_r_y.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_ankle_r_y(self):
        if self.bar_df_ankle_r_y.get() - self.resolution_df_ankle_r_y >= 1.01*self.range_df_ankle_r_y[0]:
            self.df_ankle_r_y += -self.resolution_df_ankle_r_y
            self.bar_df_ankle_r_y.set(self.df_ankle_r_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_ankle_r_y(self):
        if self.bar_df_ankle_r_y.get() + self.resolution_df_ankle_r_y <= 1.01*self.range_df_ankle_r_y[1]:
            self.df_ankle_r_y += self.resolution_df_ankle_r_y
            self.bar_df_ankle_r_y.set(self.df_ankle_r_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_hand_l_x(self, event):
        self.df_hand_l_x = self.bar_df_hand_l_x.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_hand_l_x(self):
        if self.bar_df_hand_l_x.get() - self.resolution_df_hand_l_x >= 1.01*self.range_df_hand_l_x[0]:
            self.df_hand_l_x += -self.resolution_df_hand_l_x
            self.bar_df_hand_l_x.set(self.df_hand_l_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_hand_l_x(self):
        if self.bar_df_hand_l_x.get() + self.resolution_df_hand_l_x <= 1.01*self.range_df_hand_l_x[1]:
            self.df_hand_l_x += self.resolution_df_hand_l_x
            self.bar_df_hand_l_x.set(self.df_hand_l_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_hand_r_x(self, event):
        self.df_hand_r_x = self.bar_df_hand_r_x.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_hand_r_x(self):
        if self.bar_df_hand_r_x.get() - self.resolution_df_hand_r_x >= 1.01*self.range_df_hand_r_x[0]:
            self.df_hand_r_x += -self.resolution_df_hand_r_x
            self.bar_df_hand_r_x.set(self.df_hand_r_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_hand_r_x(self):
        if self.bar_df_hand_r_x.get() + self.resolution_df_hand_r_x <= 1.01*self.range_df_hand_r_x[1]:
            self.df_hand_r_x += self.resolution_df_hand_r_x
            self.bar_df_hand_r_x.set(self.df_hand_r_x)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_foot_l_y(self, event):
        self.df_foot_l_y = self.bar_df_foot_l_y.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_foot_l_y(self):
        if self.bar_df_foot_l_y.get() - self.resolution_df_foot_l_y >= 1.01*self.range_df_foot_l_y[0]:
            self.df_foot_l_y += -self.resolution_df_foot_l_y
            self.bar_df_foot_l_y.set(self.df_foot_l_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_foot_l_y(self):
        if self.bar_df_foot_l_y.get() + self.resolution_df_foot_l_y <= 1.01*self.range_df_foot_l_y[1]:
            self.df_foot_l_y += self.resolution_df_foot_l_y
            self.bar_df_foot_l_y.set(self.df_foot_l_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_bar_df_foot_r_y(self, event):
        self.df_foot_r_y = self.bar_df_foot_r_y.get()
        self.calculate_positions()
        self.draw_shapes()

    def set_button_l_df_foot_r_y(self):
        if self.bar_df_foot_r_y.get() - self.resolution_df_foot_r_y >= 1.01*self.range_df_foot_r_y[0]:
            self.df_foot_r_y += -self.resolution_df_foot_r_y
            self.bar_df_foot_r_y.set(self.df_foot_r_y)
            self.calculate_positions()
            self.draw_shapes()

    def set_button_r_df_foot_r_y(self):
        if self.bar_df_foot_r_y.get() + self.resolution_df_foot_r_y <= 1.01*self.range_df_foot_r_y[1]:
            self.df_foot_r_y += self.resolution_df_foot_r_y
            self.bar_df_foot_r_y.set(self.df_foot_r_y)
            self.calculate_positions()
            self.draw_shapes()

    def calculate_positions(self):
        # Initial shape parameters
        self.x_start = 0
        self.y_start = self.wb + (self.w - self.wb)/2
        self.z_start = self.h/2

        self.pos_core = np.array([[self.x_start], [self.y_start], [self.z_start]])
        self.rot_core = np.array([[self.df_core_x], [self.df_core_y], [self.df_core_z]])
        self.correction_core = np.zeros((3, 3))
        self.correction_core[0, 0] = 1
        self.correction_core[1, 1] = 1
        self.correction_core[2, 2] = 1

        self.transform_lb = self.rot_mat(self.rot_core)
        self.pos_lb = self.pos_core + np.matmul(np.matmul(self.correction_core, self.transform_lb), self.v_lb)
        self.rot_lb = np.array([[0], [self.df_lb_y], [self.df_lb_z]])
        self.correction_lb = np.matmul(self.correction_core, self.transform_lb)

        self.transform_neck = self.rot_mat(self.rot_lb)
        self.pos_neck = self.pos_lb + np.matmul(np.matmul(self.correction_lb, self.transform_neck), self.v_ub)
        self.rot_neck = np.array([[self.df_neck_x], [self.df_neck_y], [self.df_neck_z]])
        self.correction_neck = np.matmul(self.correction_lb, self.transform_neck)

        self.transform_head = self.rot_mat(self.rot_neck)
        self.pos_head = self.pos_neck + np.matmul(np.matmul(self.correction_neck, self.transform_head), self.v_neck)
        self.rot_head = np.array([[0], [self.df_head_y], [0]])
        self.correction_head = np.matmul(self.correction_neck, self.transform_head)

        self.transform_shoulder_l = self.rot_mat(self.rot_lb)
        self.pos_shoulder_l = self.pos_lb + np.matmul(np.matmul(self.correction_lb, self.transform_shoulder_l), self.v_shoulder_l)
        self.rot_shoulder_l = np.array([[self.df_shoulder_l_x], [0], [self.df_shoulder_l_z]])
        self.correction_shoulder_l = np.matmul(self.correction_lb, self.transform_shoulder_l)

        self.transform_shoulder_r = self.rot_mat(self.rot_lb)
        self.pos_shoulder_r = self.pos_lb + np.matmul(np.matmul(self.correction_lb, self.transform_shoulder_r), self.v_shoulder_r)
        self.rot_shoulder_r = np.array([[self.df_shoulder_r_x], [0], [self.df_shoulder_r_z]])
        self.correction_shoulder_r = np.matmul(self.correction_lb, self.transform_shoulder_r)

        self.transform_ua_l = self.rot_mat(self.rot_shoulder_l)
        self.pos_ua_l = self.pos_shoulder_l + np.matmul(np.matmul(self.correction_shoulder_l, self.transform_ua_l), self.v_ua_l)
        self.rot_ua_l = np.array([[self.df_ua_l_x], [self.df_ua_l_y], [0]])
        self.correction_ua_l = np.matmul(self.correction_shoulder_l, self.transform_ua_l)

        self.transform_ua_r = self.rot_mat(self.rot_shoulder_r)
        self.pos_ua_r = self.pos_shoulder_r + np.matmul(np.matmul(self.correction_shoulder_r, self.transform_ua_r), self.v_ua_r)
        self.rot_ua_r = np.array([[self.df_ua_r_x], [self.df_ua_r_y], [0]])
        self.correction_ua_r = np.matmul(self.correction_shoulder_r, self.transform_ua_r)

        self.transform_elbow_l = self.rot_mat(self.rot_ua_l)
        self.pos_elbow_l = self.pos_ua_l + np.matmul(np.matmul(self.correction_ua_l, self.transform_elbow_l), self.v_elbow_l)
        self.rot_elbow_l = np.array([[0], [self.df_elbow_l_y], [self.df_elbow_l_z]])
        self.correction_elbow_l = np.matmul(self.correction_ua_l, self.transform_elbow_l)

        self.transform_elbow_r = self.rot_mat(self.rot_ua_r)
        self.pos_elbow_r = self.pos_ua_r + np.matmul(np.matmul(self.correction_ua_r, self.transform_elbow_r), self.v_elbow_r)
        self.rot_elbow_r = np.array([[0], [self.df_elbow_r_y], [self.df_elbow_r_z]])
        self.correction_elbow_r = np.matmul(self.correction_ua_r, self.transform_elbow_r)

        self.transform_wrist_l = self.rot_mat(self.rot_elbow_l)
        self.pos_wrist_l = self.pos_elbow_l + np.matmul(np.matmul(self.correction_elbow_l, self.transform_wrist_l), self.v_wrist_l)
        self.rot_wrist_l = np.array([[self.df_wrist_l_x], [self.df_wrist_l_y], [0]])
        self.correction_wrist_l = np.matmul(self.correction_elbow_l, self.transform_wrist_l)

        self.transform_wrist_r = self.rot_mat(self.rot_elbow_r)
        self.pos_wrist_r = self.pos_elbow_r + np.matmul(np.matmul(self.correction_elbow_r, self.transform_wrist_r), self.v_wrist_r)
        self.rot_wrist_r = np.array([[self.df_wrist_r_x], [self.df_wrist_r_y], [0]])
        self.correction_wrist_r = np.matmul(self.correction_elbow_r, self.transform_wrist_r)

        self.transform_hand_l = self.rot_mat(self.rot_wrist_l)
        self.pos_hand_l = self.pos_wrist_l + np.matmul(np.matmul(self.correction_wrist_l, self.transform_hand_l), self.v_hand_l)
        self.rot_hand_l = np.array([[self.df_hand_l_x], [0], [0]])
        self.correction_hand_l = np.matmul(self.correction_wrist_l, self.transform_hand_l)

        self.transform_hand_r = self.rot_mat(self.rot_wrist_r)
        self.pos_hand_r = self.pos_wrist_r + np.matmul(np.matmul(self.correction_wrist_r, self.transform_hand_r), self.v_hand_r)
        self.rot_hand_r = np.array([[self.df_hand_r_x], [0], [0]])
        self.correction_hand_r = np.matmul(self.correction_wrist_r, self.transform_hand_r)

        self.transform_fingers_l = self.rot_mat(self.rot_hand_l)
        self.pos_fingers_l = self.pos_hand_l + np.matmul(np.matmul(self.correction_hand_l, self.transform_fingers_l), self.v_fingers_l)

        self.transform_fingers_r = self.rot_mat(self.rot_hand_r)
        self.pos_fingers_r = self.pos_hand_r + np.matmul(np.matmul(self.correction_hand_r, self.transform_fingers_r), self.v_fingers_r)

        self.transform_hip_l = self.rot_mat(self.rot_core)
        self.pos_hip_l = self.pos_core + np.matmul(np.matmul(self.correction_core, self.transform_hip_l), self.v_hip_l)
        self.rot_hip_l = np.array([[self.df_hip_l_x], [self.df_hip_l_y], [self.df_hip_l_z]])
        self.correction_hip_l = np.matmul(self.correction_core, self.transform_hip_l)

        self.transform_hip_r = self.rot_mat(self.rot_core)
        self.pos_hip_r = self.pos_core + np.matmul(np.matmul(self.correction_core, self.transform_hip_r), self.v_hip_r)
        self.rot_hip_r = np.array([[self.df_hip_r_x], [self.df_hip_r_y], [self.df_hip_r_z]])
        self.correction_hip_r = np.matmul(self.correction_core, self.transform_hip_r)

        self.transform_knee_l = self.rot_mat(self.rot_hip_l)
        self.pos_knee_l = self.pos_hip_l + np.matmul(np.matmul(self.correction_hip_l, self.transform_knee_l), self.v_knee_l)
        self.rot_knee_l = np.array([[0], [self.df_knee_l_y], [0]])
        self.correction_knee_l = np.matmul(self.correction_hip_l, self.transform_knee_l)

        self.transform_knee_r = self.rot_mat(self.rot_hip_r)
        self.pos_knee_r = self.pos_hip_r + np.matmul(np.matmul(self.correction_hip_r, self.transform_knee_r), self.v_knee_r)
        self.rot_knee_r = np.array([[0], [self.df_knee_r_y], [0]])
        self.correction_knee_r = np.matmul(self.correction_hip_r, self.transform_knee_r)

        self.transform_ankle_l = self.rot_mat(self.rot_knee_l)
        self.pos_ankle_l = self.pos_knee_l + np.matmul(np.matmul(self.correction_knee_l, self.transform_ankle_l), self.v_ankle_l)
        self.rot_ankle_l = np.array([[self.df_ankle_l_x], [self.df_ankle_l_y], [0]])
        self.correction_ankle_l = np.matmul(self.correction_knee_l, self.transform_ankle_l)

        self.transform_ankle_r = self.rot_mat(self.rot_knee_r)
        self.pos_ankle_r = self.pos_knee_r + np.matmul(np.matmul(self.correction_knee_r, self.transform_ankle_r), self.v_ankle_r)
        self.rot_ankle_r = np.array([[self.df_ankle_r_x], [self.df_ankle_r_y], [0]])
        self.correction_ankle_r = np.matmul(self.correction_knee_r, self.transform_ankle_r)

        self.transform_foot_l = self.rot_mat(self.rot_ankle_l)
        self.pos_foot_l = self.pos_ankle_l + np.matmul(np.matmul(self.correction_ankle_l, self.transform_foot_l), self.v_foot_l)
        self.rot_foot_l = np.array([[0], [self.df_foot_l_y], [0]])
        self.correction_foot_l = np.matmul(self.correction_ankle_l, self.transform_foot_l)

        self.transform_foot_r = self.rot_mat(self.rot_ankle_r)
        self.pos_foot_r = self.pos_ankle_r + np.matmul(np.matmul(self.correction_ankle_r, self.transform_foot_r), self.v_foot_r)
        self.rot_foot_r = np.array([[0], [self.df_foot_r_y], [0]])
        self.correction_foot_r = np.matmul(self.correction_ankle_r, self.transform_foot_r)

        self.transform_toes_l = self.rot_mat(self.rot_foot_l)
        self.pos_toes_l = self.pos_foot_l + np.matmul(np.matmul(self.correction_foot_l, self.transform_toes_l), self.v_toes_l)

        self.transform_toes_r = self.rot_mat(self.rot_foot_r)
        self.pos_toes_r = self.pos_foot_r + np.matmul(np.matmul(self.correction_foot_r, self.transform_toes_r), self.v_toes_r)


    def rot_mat(self, v_angles):
        # Create the rotation matrix for rotation around x-axis, then y-axis, then z_axis
        transform_mat = np.zeros((3, 3))
        transform_mat[0, 0] = math.cos(v_angles[2])*math.cos(v_angles[1])
        transform_mat[0, 1] = math.sin(v_angles[2])*math.cos(v_angles[0]) + math.cos(v_angles[2])*math.sin(v_angles[1])*math.sin(v_angles[0])
        transform_mat[0, 2] = -math.sin(v_angles[2])*math.sin(v_angles[0]) + math.cos(v_angles[2])*math.sin(v_angles[1])*math.cos(v_angles[0])
        transform_mat[1, 0] = -math.sin(v_angles[2])*math.cos(v_angles[1])
        transform_mat[1, 1] = math.cos(v_angles[2])*math.cos(v_angles[0]) - math.sin(v_angles[2])*math.sin(v_angles[1])*math.sin(v_angles[0])
        transform_mat[1, 2] = -math.cos(v_angles[2])*math.sin(v_angles[0]) - math.sin(v_angles[2])*math.sin(v_angles[1])*math.cos(v_angles[0])
        transform_mat[2, 0] = -math.sin(v_angles[1])
        transform_mat[2, 1] = math.cos(v_angles[1])*math.sin(v_angles[0])
        transform_mat[2, 2] = math.cos(v_angles[1])*math.cos(v_angles[0])

        return transform_mat

    def draw_shapes(self):
        # Delete the old objects
        while len(self.all_shape_ids) > 0:
            self.canvas.delete(self.all_shape_ids.pop(0))

        # Set the colors
        color_l = 'blue'
        color_r = 'red'

        # Set the depth scale
        depth_scale = -0.1

        # Draw the new objects
        # Core circle
        draw_rad_core = self.rad_core*(1 + math.tanh(depth_scale*self.pos_core[0]/self.len_scale))
        circle_id = self.canvas.create_oval(int(self.pos_core[1] - draw_rad_core), int(self.pos_core[2] - draw_rad_core), int(self.pos_core[1] + draw_rad_core), int(self.pos_core[2] + draw_rad_core))
        self.all_shape_ids.append(circle_id)

        # Line from core to lower back
        line_id = self.canvas.create_line(int(self.pos_core[1]), int(self.pos_core[2]), int(self.pos_lb[1]), int(self.pos_lb[2]))
        self.all_shape_ids.append(line_id)

        # Lower back circle
        draw_rad_lb = self.rad_lb*(1 + math.tanh(depth_scale*self.pos_lb[0]/self.len_scale))
        circle_id = self.canvas.create_oval(int(self.pos_lb[1] - draw_rad_lb), int(self.pos_lb[2] - draw_rad_lb), int(self.pos_lb[1] + draw_rad_lb), int(self.pos_lb[2] + draw_rad_lb))
        self.all_shape_ids.append(circle_id)

        # Line from lower back to neck
        line_id = self.canvas.create_line(int(self.pos_lb[1]), int(self.pos_lb[2]), int(self.pos_neck[1]), int(self.pos_neck[2]))
        self.all_shape_ids.append(line_id)

        # Neck circle
        draw_rad_neck = self.rad_neck*(1 + math.tanh(depth_scale*self.pos_neck[0]/self.len_scale))
        circle_id = self.canvas.create_oval(int(self.pos_neck[1] - draw_rad_neck), int(self.pos_neck[2] - draw_rad_neck), int(self.pos_neck[1] + draw_rad_neck), int(self.pos_neck[2] + draw_rad_neck))
        self.all_shape_ids.append(circle_id)

        # Line from neck to head
        line_id = self.canvas.create_line(int(self.pos_neck[1]), int(self.pos_neck[2]), int(self.pos_head[1]), int(self.pos_head[2]))
        self.all_shape_ids.append(line_id)

        # Head circle
        draw_rad_head = self.rad_head*(1 + math.tanh(depth_scale*self.pos_head[0]/self.len_scale))
        circle_id = self.canvas.create_oval(int(self.pos_head[1] - draw_rad_head), int(self.pos_head[2] - draw_rad_head), int(self.pos_head[1] + draw_rad_head), int(self.pos_head[2] + draw_rad_head))
        self.all_shape_ids.append(circle_id)

        # Line from lower back to left shoulder
        line_id = self.canvas.create_line(int(self.pos_lb[1]), int(self.pos_lb[2]), int(self.pos_shoulder_l[1]), int(self.pos_shoulder_l[2]), fill = color_l)
        self.all_shape_ids.append(line_id)

        # Left shoulder circle
        draw_rad_shoulder_l = self.rad_shoulder*(1 + math.tanh(depth_scale*self.pos_shoulder_l[0]/self.len_scale))
        circle_id = self.canvas.create_oval(int(self.pos_shoulder_l[1] - draw_rad_shoulder_l), int(self.pos_shoulder_l[2] - draw_rad_shoulder_l), int(self.pos_shoulder_l[1] + draw_rad_shoulder_l), int(self.pos_shoulder_l[2] + draw_rad_shoulder_l), outline = color_l)
        self.all_shape_ids.append(circle_id)

        # Line from lower back to right shoulder
        line_id = self.canvas.create_line(int(self.pos_lb[1]), int(self.pos_lb[2]), int(self.pos_shoulder_r[1]), int(self.pos_shoulder_r[2]), fill = color_r)
        self.all_shape_ids.append(line_id)

        # Right shoulder circle
        draw_rad_shoulder_r = self.rad_shoulder*(1 + math.tanh(depth_scale*self.pos_shoulder_r[0]/self.len_scale))
        circle_id = self.canvas.create_oval(int(self.pos_shoulder_r[1] - draw_rad_shoulder_r), int(self.pos_shoulder_r[2] - draw_rad_shoulder_r), int(self.pos_shoulder_r[1] + draw_rad_shoulder_r), int(self.pos_shoulder_r[2] + draw_rad_shoulder_r), outline = color_r)
        self.all_shape_ids.append(circle_id)

        # Line from left shoulder to left upper arm
        line_id = self.canvas.create_line(int(self.pos_shoulder_l[1]), int(self.pos_shoulder_l[2]), int(self.pos_ua_l[1]), int(self.pos_ua_l[2]), fill = color_l)
        self.all_shape_ids.append(line_id)

        # Left upper arm circle
        draw_rad_ua_l = self.rad_ua*(1 + math.tanh(depth_scale*self.pos_ua_l[0]/self.len_scale))
        circle_id = self.canvas.create_oval(int(self.pos_ua_l[1] - draw_rad_ua_l), int(self.pos_ua_l[2] - draw_rad_ua_l), int(self.pos_ua_l[1] + draw_rad_ua_l), int(self.pos_ua_l[2] + draw_rad_ua_l), outline = color_l)
        self.all_shape_ids.append(circle_id)

        # Line from right shoulder to right upper arm
        line_id = self.canvas.create_line(int(self.pos_shoulder_r[1]), int(self.pos_shoulder_r[2]), int(self.pos_ua_r[1]), int(self.pos_ua_r[2]), fill = color_r)
        self.all_shape_ids.append(line_id)

        # Right upper arm circle
        draw_rad_ua_r = self.rad_ua*(1 + math.tanh(depth_scale*self.pos_ua_r[0]/self.len_scale))
        circle_id = self.canvas.create_oval(int(self.pos_ua_r[1] - draw_rad_ua_r), int(self.pos_ua_r[2] - draw_rad_ua_r), int(self.pos_ua_r[1] + draw_rad_ua_r), int(self.pos_ua_r[2] + draw_rad_ua_r), outline = color_r)
        self.all_shape_ids.append(circle_id)

        # Line from left upper arm to left elbow
        line_id = self.canvas.create_line(int(self.pos_ua_l[1]), int(self.pos_ua_l[2]), int(self.pos_elbow_l[1]), int(self.pos_elbow_l[2]), fill = color_l)
        self.all_shape_ids.append(line_id)

        # Left elbow circle
        draw_rad_elbow_l = self.rad_elbow*(1 + math.tanh(depth_scale*self.pos_elbow_l[0]/self.len_scale))
        circle_id = self.canvas.create_oval(int(self.pos_elbow_l[1] - draw_rad_elbow_l), int(self.pos_elbow_l[2] - draw_rad_elbow_l), int(self.pos_elbow_l[1] + draw_rad_elbow_l), int(self.pos_elbow_l[2] + draw_rad_elbow_l), outline = color_l)
        self.all_shape_ids.append(circle_id)

        # Line from right upper arm to right elbow
        line_id = self.canvas.create_line(int(self.pos_ua_r[1]), int(self.pos_ua_r[2]), int(self.pos_elbow_r[1]), int(self.pos_elbow_r[2]), fill = color_r)
        self.all_shape_ids.append(line_id)

        # Right elbow circle
        draw_rad_elbow_r = self.rad_elbow*(1 + math.tanh(depth_scale*self.pos_elbow_r[0]/self.len_scale))
        circle_id = self.canvas.create_oval(int(self.pos_elbow_r[1] - draw_rad_elbow_r), int(self.pos_elbow_r[2] - draw_rad_elbow_r), int(self.pos_elbow_r[1] + draw_rad_elbow_r), int(self.pos_elbow_r[2] + draw_rad_elbow_r), outline = color_r)
        self.all_shape_ids.append(circle_id)

        # Line from left elbow to left wrist
        line_id = self.canvas.create_line(int(self.pos_elbow_l[1]), int(self.pos_elbow_l[2]), int(self.pos_wrist_l[1]), int(self.pos_wrist_l[2]), fill = color_l)
        self.all_shape_ids.append(line_id)

        # Left wrist circle
        draw_rad_wrist_l = self.rad_wrist*(1 + math.tanh(depth_scale*self.pos_wrist_l[0]/self.len_scale))
        circle_id = self.canvas.create_oval(int(self.pos_wrist_l[1] - draw_rad_wrist_l), int(self.pos_wrist_l[2] - draw_rad_wrist_l), int(self.pos_wrist_l[1] + draw_rad_wrist_l), int(self.pos_wrist_l[2] + draw_rad_wrist_l), outline = color_l)
        self.all_shape_ids.append(circle_id)

        # Line from right elbow to right wrist
        line_id = self.canvas.create_line(int(self.pos_elbow_r[1]), int(self.pos_elbow_r[2]), int(self.pos_wrist_r[1]), int(self.pos_wrist_r[2]), fill = color_r)
        self.all_shape_ids.append(line_id)

        # Right wrist circle
        draw_rad_wrist_r = self.rad_wrist*(1 + math.tanh(depth_scale*self.pos_wrist_r[0]/self.len_scale))
        circle_id = self.canvas.create_oval(int(self.pos_wrist_r[1] - draw_rad_wrist_r), int(self.pos_wrist_r[2] - draw_rad_wrist_r), int(self.pos_wrist_r[1] + draw_rad_wrist_r), int(self.pos_wrist_r[2] + draw_rad_wrist_r), outline = color_r)
        self.all_shape_ids.append(circle_id)

        # Line from left wrist to left hand
        line_id = self.canvas.create_line(int(self.pos_wrist_l[1]), int(self.pos_wrist_l[2]), int(self.pos_hand_l[1]), int(self.pos_hand_l[2]), fill = color_l)
        self.all_shape_ids.append(line_id)

        # Left hand circle
        draw_rad_hand_l = self.rad_hand*(1 + math.tanh(depth_scale*self.pos_hand_l[0]/self.len_scale))
        circle_id = self.canvas.create_oval(int(self.pos_hand_l[1] - draw_rad_hand_l), int(self.pos_hand_l[2] - draw_rad_hand_l), int(self.pos_hand_l[1] + draw_rad_hand_l), int(self.pos_hand_l[2] + draw_rad_hand_l), outline = color_l)
        self.all_shape_ids.append(circle_id)

        # Line from right wrist to right hand
        line_id = self.canvas.create_line(int(self.pos_wrist_r[1]), int(self.pos_wrist_r[2]), int(self.pos_hand_r[1]), int(self.pos_hand_r[2]), fill = color_r)
        self.all_shape_ids.append(line_id)

        # Right hand circle
        draw_rad_hand_r = self.rad_hand*(1 + math.tanh(depth_scale*self.pos_hand_r[0]/self.len_scale))
        circle_id = self.canvas.create_oval(int(self.pos_hand_r[1] - draw_rad_hand_r), int(self.pos_hand_r[2] - draw_rad_hand_r), int(self.pos_hand_r[1] + draw_rad_hand_r), int(self.pos_hand_r[2] + draw_rad_hand_r), outline = color_r)
        self.all_shape_ids.append(circle_id)

        # Left finger line
        line_id = self.canvas.create_line(int(self.pos_hand_l[1]), int(self.pos_hand_l[2]), int(self.pos_fingers_l[1]), int(self.pos_fingers_l[2]), fill = color_l)
        self.all_shape_ids.append(line_id)

        # Right finger line
        line_id = self.canvas.create_line(int(self.pos_hand_r[1]), int(self.pos_hand_r[2]), int(self.pos_fingers_r[1]), int(self.pos_fingers_r[2]), fill = color_r)
        self.all_shape_ids.append(line_id)

        # Line from core to left hip
        line_id = self.canvas.create_line(int(self.pos_core[1]), int(self.pos_core[2]), int(self.pos_hip_l[1]), int(self.pos_hip_l[2]), fill = color_l)
        self.all_shape_ids.append(line_id)

        # Left hip circle
        draw_rad_hip_l = self.rad_hip*(1 + math.tanh(depth_scale*self.pos_hip_l[0]/self.len_scale))
        circle_id = self.canvas.create_oval(int(self.pos_hip_l[1] - draw_rad_hip_l), int(self.pos_hip_l[2] - draw_rad_hip_l), int(self.pos_hip_l[1] + draw_rad_hip_l), int(self.pos_hip_l[2] + draw_rad_hip_l), outline = color_l)
        self.all_shape_ids.append(circle_id)

        # Line from core to right hip
        line_id = self.canvas.create_line(int(self.pos_core[1]), int(self.pos_core[2]), int(self.pos_hip_r[1]), int(self.pos_hip_r[2]), fill = color_r)
        self.all_shape_ids.append(line_id)

        # Right hip circle
        draw_rad_hip_r = self.rad_hip*(1 + math.tanh(depth_scale*self.pos_hip_r[0]/self.len_scale))
        circle_id = self.canvas.create_oval(int(self.pos_hip_r[1] - draw_rad_hip_r), int(self.pos_hip_r[2] - draw_rad_hip_r), int(self.pos_hip_r[1] + draw_rad_hip_r), int(self.pos_hip_r[2] + draw_rad_hip_r), outline = color_r)
        self.all_shape_ids.append(circle_id)

        # Line from left hip to left knee
        line_id = self.canvas.create_line(int(self.pos_hip_l[1]), int(self.pos_hip_l[2]), int(self.pos_knee_l[1]), int(self.pos_knee_l[2]), fill = color_l)
        self.all_shape_ids.append(line_id)

        # Left knee circle
        draw_rad_knee_l = self.rad_knee*(1 + math.tanh(depth_scale*self.pos_knee_l[0]/self.len_scale))
        circle_id = self.canvas.create_oval(int(self.pos_knee_l[1] - draw_rad_knee_l), int(self.pos_knee_l[2] - draw_rad_knee_l), int(self.pos_knee_l[1] + draw_rad_knee_l), int(self.pos_knee_l[2] + draw_rad_knee_l), outline = color_l)
        self.all_shape_ids.append(circle_id)

        # Line from right hip to right knee
        line_id = self.canvas.create_line(int(self.pos_hip_r[1]), int(self.pos_hip_r[2]), int(self.pos_knee_r[1]), int(self.pos_knee_r[2]), fill = color_r)
        self.all_shape_ids.append(line_id)

        # Right knee circle
        draw_rad_knee_r = self.rad_knee*(1 + math.tanh(depth_scale*self.pos_knee_r[0]/self.len_scale))
        circle_id = self.canvas.create_oval(int(self.pos_knee_r[1] - draw_rad_knee_r), int(self.pos_knee_r[2] - draw_rad_knee_r), int(self.pos_knee_r[1] + draw_rad_knee_r), int(self.pos_knee_r[2] + draw_rad_knee_r), outline = color_r)
        self.all_shape_ids.append(circle_id)

        # Line from left knee to left ankle
        line_id = self.canvas.create_line(int(self.pos_knee_l[1]), int(self.pos_knee_l[2]), int(self.pos_ankle_l[1]), int(self.pos_ankle_l[2]), fill = color_l)
        self.all_shape_ids.append(line_id)

        # Left ankle circle
        draw_rad_ankle_l = self.rad_ankle*(1 + math.tanh(depth_scale*self.pos_ankle_l[0]/self.len_scale))
        circle_id = self.canvas.create_oval(int(self.pos_ankle_l[1] - draw_rad_ankle_l), int(self.pos_ankle_l[2] - draw_rad_ankle_l), int(self.pos_ankle_l[1] + draw_rad_ankle_l), int(self.pos_ankle_l[2] + draw_rad_ankle_l), outline = color_l)
        self.all_shape_ids.append(circle_id)

        # Line from right knee to right ankle
        line_id = self.canvas.create_line(int(self.pos_knee_r[1]), int(self.pos_knee_r[2]), int(self.pos_ankle_r[1]), int(self.pos_ankle_r[2]), fill = color_r)
        self.all_shape_ids.append(line_id)

        # Right ankle circle
        draw_rad_ankle_r = self.rad_ankle*(1 + math.tanh(depth_scale*self.pos_ankle_r[0]/self.len_scale))
        circle_id = self.canvas.create_oval(int(self.pos_ankle_r[1] - draw_rad_ankle_r), int(self.pos_ankle_r[2] - draw_rad_ankle_r), int(self.pos_ankle_r[1] + draw_rad_ankle_r), int(self.pos_ankle_r[2] + draw_rad_ankle_r), outline = color_r)
        self.all_shape_ids.append(circle_id)

        # Line from left ankle to left foot
        line_id = self.canvas.create_line(int(self.pos_ankle_l[1]), int(self.pos_ankle_l[2]), int(self.pos_foot_l[1]), int(self.pos_foot_l[2]), fill = color_l)
        self.all_shape_ids.append(line_id)

        # Left foot circle
        draw_rad_foot_l = self.rad_foot*(1 + math.tanh(depth_scale*self.pos_foot_l[0]/self.len_scale))
        circle_id = self.canvas.create_oval(int(self.pos_foot_l[1] - draw_rad_foot_l), int(self.pos_foot_l[2] - draw_rad_foot_l), int(self.pos_foot_l[1] + draw_rad_foot_l), int(self.pos_foot_l[2] + draw_rad_foot_l), outline = color_l)
        self.all_shape_ids.append(circle_id)

        # Line from right ankle to right foot
        line_id = self.canvas.create_line(int(self.pos_ankle_r[1]), int(self.pos_ankle_r[2]), int(self.pos_foot_r[1]), int(self.pos_foot_r[2]), fill = color_r)
        self.all_shape_ids.append(line_id)

        # Right foot circle
        draw_rad_foot_r = self.rad_foot*(1 + math.tanh(depth_scale*self.pos_foot_r[0]/self.len_scale))
        circle_id = self.canvas.create_oval(int(self.pos_foot_r[1] - draw_rad_foot_r), int(self.pos_foot_r[2] - draw_rad_foot_r), int(self.pos_foot_r[1] + draw_rad_foot_r), int(self.pos_foot_r[2] + draw_rad_foot_r), outline = color_r)
        self.all_shape_ids.append(circle_id)

        # Left toe line
        line_id = self.canvas.create_line(int(self.pos_foot_l[1]), int(self.pos_foot_l[2]), int(self.pos_toes_l[1]), int(self.pos_toes_l[2]), fill = color_l)
        self.all_shape_ids.append(line_id)

        # Right toe line
        line_id = self.canvas.create_line(int(self.pos_foot_r[1]), int(self.pos_foot_r[2]), int(self.pos_toes_r[1]), int(self.pos_toes_r[2]), fill = color_r)
        self.all_shape_ids.append(line_id)



        

        

if __name__ == "__main__":
    board = DrawingRig()