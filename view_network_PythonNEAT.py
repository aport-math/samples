'''
Create a figure for the network output from PythonNEAT.
'''

def curve_coordinates(x0, y0, x1, y1, curve_amount, num_points_on_curve):
    '''
    Returns the x and y coordinates for a circle of curvature 2*curve_amount/((x1 - x0)**2 + (y1 - y0)**2)**0.5.,
    or just a circle of radius 0.15 if the two endpoints are the same.
    Defines the curve using 101 points.
        Inputs:
            x0: x-coordinate of starting point
            y0: y-coordinate of starting point
            x1: x-coordinate of ending point
            y1: y-coordinate of ending point
            curve_amount: amount of curvature on path, float value between -1 and 1 inclusive
            num_points_on_curve: number of points on the curve
        Outputs:
            x: x-coordinates of the curve
            y: y-coordinates of the curve
    '''
    import math
    loop_radius = 0.15
    
    if curve_amount == 0:
        x = []
        y = []
        for i in range(num_points_on_curve + 1):
            x.append(x0*(num_points_on_curve - i)/num_points_on_curve + x1*i/num_points_on_curve)
            y.append(y0*(num_points_on_curve - i)/num_points_on_curve + y1*i/num_points_on_curve)
    elif curve_amount >= -1 and curve_amount <= 1:
        a = (x0 + x1)/2 - (y1 - y0)/(2*curve_amount)*(1 - curve_amount**2)**0.5
        b = (y0 + y1)/2 + (x1 - x0)/(2*curve_amount)*(1 - curve_amount**2)**0.5
        d = ((x1 - x0)**2 + (y1 - y0)**2)**0.5
        if d == 0:
            x = []
            y = []
            for i in range(num_points_on_curve + 1):
                x.append(x0 - loop_radius*math.sin(i*2*math.pi/num_points_on_curve))
                y.append(y0 - loop_radius + loop_radius*math.cos(i*2*math.pi/num_points_on_curve))
        else:
            r = d/(2*abs(curve_amount))
            theta0 = math.atan2(y0 - b, x0 - a)
            theta1 = math.atan2(y1 - b, x1 - a)
            if theta1 < theta0 and curve_amount > 0:
                theta1 += 2*math.pi
            elif theta1 > theta0 and curve_amount < 0:
                theta1 -= 2*math.pi
            x = []
            y = []
            for i in range(num_points_on_curve + 1):
                x.append(a + r*math.cos(theta0 + i/num_points_on_curve*(theta1 - theta0)))
                y.append(b + r*math.sin(theta0 + i/num_points_on_curve*(theta1 - theta0)))
    else:
        print('Error: Invalid value provided for amount of curvature.')
    return x, y

def dist_pt_2_curve(x_p, y_p, x_c, y_c):
    '''
    Compute the distance from the curve to a point.
        Inputs:
            x_p: x-coordinate of point
            y_p: y-coordinate of point
            x_c: x-coordinates of the curve
            x_c: y-coordinates of the curve
        Outputs:
            min_dist: minimum distance from point to the curve
            min_index: index of the point on the curve closest to the point
    '''
    min_dist = float('inf')
    min_index = float('inf')
    for i in range(len(x_c)):
        dist_i = ((x_c[i] - x_p)**2 + (y_c[i] - y_p)**2)**0.5
        if dist_i < min_dist:
            min_dist = dist_i
            min_index = i
    return min_dist, min_index

# Model parameters
wait_time = 2                   # time to wait when error occurs
margin_thresh = 0.5             # maximum margin to look for in spacing curves away from nodes
divide_num_per_side = 10        # number of subdivisions between 0 to 1 to look for better curve amounts
tri_scale = 0.06                # size of triangle markers on edges
minimize_curvature_flag = 0     # determine whether or not to minimize curvature of edges
num_points_on_curve = 40        # number of points on each curve

### Import and verify all dependencies for running code ###
import time

### Version thresholds for Python and required modules
python_version_threshold = '3.5.3'
tkinter_version_threshold = '8.6'
numpy_version_threshold = '1.14.5'
matplotlib_version_threshold = '3.0.2'

### Make sure the current version of Python is 3.7.0 or later
from sys import version_info
python_version = '%d.%d.%d'%(version_info.major, version_info.minor, version_info.micro)
if python_version < python_version_threshold:
    print('Error: Installed Python vesion is ' + python_version + \
        '. Please install version ' + python_version_threshold + \
        ' of Python or later.')
    time.sleep(wait_time)
    quit()

### Import required modules, check their versions 
# Math
import math
# TkInter
try:
    import tkinter as tk
    if str(tk.TkVersion) < tkinter_version_threshold:
        raise Exception('Error: Installed TkInter module vesion is ' + str(tk.TkVersion) + \
            '. Please install version ' + tkinter_version_threshold + \
            ' of TkInter or later.')
except ImportError:
    print('Error: TkInter module not found. Please install version ' + \
        str(tkinter_version_threshold) + ' of TkInter or later.')
    time.sleep(wait_time)
    quit()
except Exception as error:
    print(error)
    time.sleep(wait_time)
    quit()
except:
    print('Error: Unspecified error in loading TkInter. Please install version ' + \
        str(tkinter_version_threshold) + ' of TkInter or later.')
    time.sleep(wait_time)
    quit()
# NumPy
try:
    import numpy as np
    if np.version.version < numpy_version_threshold:
        raise Exception('Error: Installed NumPy module vesion is ' + np.version.version + \
            '. Please install version ' + numpy_version_threshold + \
            ' of NumPy or later.')
except ImportError:
    print('Error: NumPy module not found. Please install version ' + \
        numpy_version_threshold + ' of NumPy or later.')
    time.sleep(wait_time)
    quit()
except Exception as error:
    print(error)
    time.sleep(wait_time)
    quit()
except:    
    print('Error: Unspecified error in loading NumPy. Please install version ' + \
        numpy_version_threshold + ' of NumPy or later.')
    time.sleep(wait_time)
    quit()
# MatPlotLib
try:
    import matplotlib as mpl
    if mpl.__version__ < matplotlib_version_threshold:
        raise Exception('Error: Installed MatPlotLib module vesion is ' + mpl.__version__ + \
            '. Please install version ' + matplotlib_version_threshold + \
            ' of MatPlotLib or later.')
except ImportError:
    print('Error: MatPlotLib module not found. Please install version ' + \
        matplotlib_version_threshold + ' of MatPlotLib or later.')
    time.sleep(wait_time)
    quit()
except Exception as error:
    print(error)
    time.sleep(wait_time)
    quit()
except:    
    print('Error: Unspecified error in loading MatPlotLib. Please install version ' + \
        matplotlib_version_threshold + ' of MatPlotLib or later.')
    time.sleep(wait_time)
    quit()
    
### Import the data ###
try:
    root = tk.Tk()
    from tkinter import filedialog
    root.filename = filedialog.askopenfilename(title = 'Select PythonNEAT file', \
                                               filetypes = (('txt files', '*.txt'),('all files','*.*')))
    # Handle if cancel was pressed
    if not root.filename:
        raise SystemExit
    # Otherwise import the data
    raw_data = np.loadtxt(root.filename)
    root.destroy()
except SystemExit:
    quit()
except:    
    print('Error: Unspecified error in loading provided data file.')
    time.sleep(wait_time)
    quit()
    
### Extract the dimensions and subsets of the data ###
n_total = raw_data.shape[1]

weight_array = raw_data[:n_total, :]
input_array = raw_data[n_total, :]
output_array = raw_data[n_total + 1, :]

n_input = int(np.sum(input_array) - 1)    # subtract 1 for the bias
n_output = int(np.sum(output_array))
n_edge = int(np.sum(weight_array != 0))

### Create node label and type information ###
labels = []
sources = []
sinks = []
bias_index = 0
for i in range(n_total):
    labels.append(str(i + 1))
    if input_array[i] == 1:
        sources.append(str(i + 1))
        bias_index = i + 1    # last input node assumed to be the bias
    if output_array[i] == 1:
        sinks.append(str(i + 1))

### Find the minimum and maximum non-zero absolute values of entries in weight_array ###
max_value = 0
min_value = math.inf
for i in range (n_total):
    for j in range(n_total):
        if weight_array[i, j] != 0:
            if abs(weight_array[i, j]) > max_value:
                max_value = abs(weight_array[i, j])
            if abs(weight_array[i, j]) < min_value:
                min_value = abs(weight_array[i, j])

### Create create and width information for the diagram ###
adj_array = np.zeros([n_total, n_total])
color_info = np.zeros([n_edge, 4])
edge_count = 1
for i in range(n_total):
    for j in range(n_total):
        if weight_array[i, j] != 0:
            color_num = 1
            if weight_array[i, j] < 0:
                color_num = -1
            width = 5.5*(abs(weight_array[i, j]) - min_value)/(max_value - min_value) + 0.5
            color_info[edge_count - 1, :] = [i + 1, j + 1, color_num, width];
            adj_array[i, j] = 1;
            edge_count = edge_count + 1

### Draw the network ###
### Compute the depth of each node
# Initialize
depth_array = np.zeros(n_total)
for i in range(n_total):
    if input_array[i] == 0:
        depth_array[i] = math.inf
# Compute the longest non-repeating path to each non-input node
stable = 0
current_depth = 1
visited_array = np.zeros([n_total, n_total])
while stable == 0:
    stable = 1
    changed = 0
    for i in range(n_total):
        for j in range(n_total):
            if i != j and adj_array[j, i] == 1 and depth_array[j] == current_depth - 1 and visited_array[j, i] == 0:
                depth_array[i] = current_depth
                visited_array[j, i] = 1
                changed = 1
    current_depth += 1
    if changed == 1:
        stable = 0
# Check that graph is connected
old_max_depth = np.max(depth_array)
if old_max_depth == math.inf:
    print('Error: Provided data file does not represent a connected network.')
# Correct so that output nodes are in the last layer
for i in range(n_total):
    if output_array[i] == 1:
        depth_array[i] = old_max_depth + 1
# Shift to fill in any holes left by moving the output node depths and count the number of nodes at each depth
all_old_depth_values = []
for i in range(n_total):
    if np.sum(all_old_depth_values == depth_array[i]) == 0:     # not found in list
        all_old_depth_values.append(depth_array[i])
sorted_all_old_depth_values = np.sort(all_old_depth_values)
num_layers = len(sorted_all_old_depth_values)
depth_node_counts = np.zeros(num_layers)
for i in range(n_total):
    for j in range(num_layers):
        if depth_array[i] == sorted_all_old_depth_values[j]:
            depth_array[i] = j
            depth_node_counts[j] += 1
# Construct initial coordinates for nodes
x_coord = np.zeros(n_total)
y_coord = depth_array
layer_counters = np.zeros(num_layers)
for i in range(n_total):
    layer = int(depth_array[i])
    x_coord[i] = layer_counters[layer] - 0.5*depth_node_counts[layer] + 0.5
    layer_counters[layer] += 1
# Shuffle the x-values around to make connected node closer
scale = 0.02*(np.max(x_coord) - np.min(x_coord))
for i in range(int(1 + 1000*scale)):
    x_coord_new = np.copy(x_coord)
    for j in range(int(n_total - n_input - 1)):
        weight = 0
        for k in range(n_total):
            if adj_array[int(j + n_input + 1), k] == 1 or adj_array[k, int(j + n_input + 1)] == 1:
                diff = x_coord[k] - x_coord[int(j + n_input + 1)]
                if diff > 0:
                    weight += abs(diff)
                if diff < 0:
                    weight -= abs(diff)
        if weight > 0:
            x_coord_new[int(j + n_input + 1)] += scale*abs(weight)**0.5
        if weight < 0:
            x_coord_new[int(j + n_input + 1)] -= scale*abs(weight)**0.5
    new_center = np.mean(x_coord_new[n_input + 1:])
    for j in range(int(n_total - n_input - 1)):
        x_coord_new[int(j + n_input + 1)] -= new_center
    x_coord = np.copy(x_coord_new)
# Adjust the x-values for better spacing
x_coord_new = np.copy(x_coord)
max_depth = np.max(depth_array)
current_depth = 1
while current_depth <= max_depth:
    nodes_at_depth = []
    x_coord_at_depth = []
    for i in range(int(n_total - n_input - 1)):
        if depth_array[int(i + n_input + 1)] == current_depth:
            nodes_at_depth.append(int(i + n_input + 1))
            x_coord_at_depth.append(x_coord[int(i + n_input + 1)])
    x_coord_at_depth.sort()
    for i in range(len(nodes_at_depth)):
        for j in nodes_at_depth:
            if x_coord[j] == x_coord_at_depth[i]:
                x_coord_new[j] = i - 0.5*len(nodes_at_depth) + 0.5
    current_depth += 1
for i in range(n_total - n_input - 1):  # make the non-input node more spaced apart
    x_coord[i + n_input + 1] = 2.25*x_coord[i + n_input + 1] + 0.75*x_coord_new[i + n_input + 1]
# Draw the network according to the above
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
for i in range(n_edge):
    # Coordinates of the start and end nodes
    x0 = x_coord[int(color_info[i, 0] - 1)]
    y0 = y_coord[int(color_info[i, 0] - 1)]
    x1 = x_coord[int(color_info[i, 1] - 1)]
    y1 = y_coord[int(color_info[i, 1] - 1)]
    # Create the curve conencting the two nodes
    protected_placement = 0
    if adj_array[int(color_info[i, 0] - 1), int(color_info[i, 1] - 1)] == 1 \
       and adj_array[int(color_info[i, 1] - 1), int(color_info[i, 0] - 1)] == 1:   # if edges going in both directions between two nodes, split them up
        curve_amount = 0.4
    else:
        layer0 = depth_array[int(color_info[i, 0] - 1)]
        layer1 = depth_array[int(color_info[i, 1] - 1)]
        if np.max(depth_array) == 1:
            curve_amount = 0
            protected_placement = 1
        else:
            # Curve them more if separated by more layers
            if (x0 < x1 and y0 < y1) or (x0 > x1 and y0 > y1):
                curve_amount = -0.8*(abs(abs(layer1 - layer0) - 1)/(np.max(depth_array) - 1))**0.5
            elif (x0 > x1 and y0 < y1) or (x0 < x1 and y0 > y1):
                curve_amount = 0.8*(abs(abs(layer1 - layer0) - 1)/(np.max(depth_array) - 1))**0.5
            else:
                curve_amount = 0
    x, y = curve_coordinates(x0, y0, x1, y1, curve_amount, num_points_on_curve)
    # Get better spacing for the curves    
    if protected_placement == 0:
        # Increase curvature if passing too close to another point
        all_min_dist = float('inf')
        all_min_index = float('inf')
        for j in range(n_total):
            if j != int(color_info[i, 0] - 1) and j != int(color_info[i, 1] - 1):
                min_dist, min_index = dist_pt_2_curve(x_coord[j], y_coord[j], x, y)
                if min_dist < all_min_dist:
                    all_min_dist = min_dist
                    all_min_index = min_index
        if all_min_dist < margin_thresh*all_min_index*(100 - all_min_index)/2500:
            if curve_amount >= 0:
                new_curve_amount = (curve_amount + 1)/2
            else:
                new_curve_amount = (curve_amount - 1)/2
            x, y = curve_coordinates(x0, y0, x1, y1, new_curve_amount, num_points_on_curve)
            # If still too close, search for best curvature
            all_min_dist = float('inf')
            all_min_index = float('inf')
            for j in range(n_total):
                if j != int(color_info[i, 0] - 1) and j != int(color_info[i, 1] - 1):
                    min_dist, min_index = dist_pt_2_curve(x_coord[j], y_coord[j], x, y)
                    if min_dist < all_min_dist:
                        all_min_dist = min_dist
                        all_min_index = min_index
            if all_min_dist < margin_thresh*all_min_index*(100 - all_min_index)/2500:
                # Two types of margin searches, minimum acceptable and largest
                smallest_valid_min_margin = -float('inf')
                smallest_valid_min_curve_amount = float('inf')
                largest_min_margin = -float('inf')
                largest_min_curve_amount = float('inf')
                for j in range(2*divide_num_per_side + 1):
                    current_curve_amount = j/divide_num_per_side - 1
                    x_current, y_current = curve_coordinates(x0, y0, x1, y1, current_curve_amount, int(num_points_on_curve/2))  # check at lower density to speed up code
                    current_min_margin = float('inf')
                    for k in range(n_total):
                        if k != int(color_info[i, 0] - 1) and k != int(color_info[i, 1] - 1):
                            min_dist, min_index = dist_pt_2_curve(x_coord[k], y_coord[k], x_current, y_current)
                            if margin_thresh*min_index*(100 - min_index)/2500 > 0:
                                margin = min_dist/(margin_thresh*min_index*(100 - min_index)/2500)
                            else:
                                margin = float('inf')
                            if margin < current_min_margin:
                                current_min_margin = margin
                    # Choose smallest amount of curve that fits a margin greater than or equal to 1
                    if current_min_margin >= 1 and abs(current_curve_amount) <= abs(smallest_valid_min_curve_amount):
                        smallest_valid_min_margin = current_min_margin
                        smallest_valid_min_curve_amount = current_curve_amount
                    # As backup, just store the one with the largest margin
                    if current_min_margin > largest_min_margin:
                        largest_min_margin = current_min_margin
                        largest_min_curve_amount = current_curve_amount
                if smallest_valid_min_curve_amount != float('inf') and minimize_curvature_flag == 1:
                    best_curve_amount = smallest_valid_min_curve_amount
                else:
                    best_curve_amount = largest_min_curve_amount
                x, y = curve_coordinates(x0, y0, x1, y1, best_curve_amount, num_points_on_curve)   
    # Extract color information
    if color_info[i, 2] == 1:
        c = 'b'
    if color_info[i, 2] == -1:
        c = 'r'
    plt.plot(x, y, c, zorder = 0, linewidth = color_info[i, 3])
    # Create a triangle in the middle of the curve to indicate direction
    center_index = int(num_points_on_curve/2)
    x_center = x[center_index]
    y_center = y[center_index]
    dir_x = (x[center_index + 1] - x[center_index - 1])/((x[center_index + 1] - x[center_index - 1])**2 + (y[center_index + 1] - y[center_index - 1])**2)**0.5
    dir_y = (y[center_index + 1] - y[center_index - 1])/((x[center_index + 1] - x[center_index - 1])**2 + (y[center_index + 1] - y[center_index - 1])**2)**0.5
    x_head = x_center + tri_scale*dir_x
    y_head = y_center + tri_scale*dir_y
    x_left = x_center - tri_scale*dir_x - tri_scale*dir_y
    y_left = y_center - tri_scale*dir_y + tri_scale*dir_x
    x_right = x_center - tri_scale*dir_x + tri_scale*dir_y
    y_right = y_center - tri_scale*dir_y - tri_scale*dir_x
    edge_tri = plt.Polygon(np.array([[x_head, y_head], [x_left, y_left], [x_right, y_right]]), color = c)
    plt.gca().add_patch(edge_tri)
node_size = 200
ax.scatter(x_coord[:n_input], y_coord[:n_input], color = 'k', zorder = 1, s = node_size)
ax.scatter(x_coord[n_input], y_coord[n_input], color = (0.5, 0.8, 0.5), zorder = 1, s = node_size)
ax.scatter(x_coord[n_input + 1:n_input + n_output + 1], y_coord[n_input + 1:n_input + n_output + 1], color = 'k', zorder = 1, s = node_size)
ax.scatter(x_coord[n_input + n_output + 1:], y_coord[n_input + n_output + 1:], color = '0.5', zorder = 1, s = node_size)
ax.set_aspect('equal')
plt.axis('off')
plt.show()
