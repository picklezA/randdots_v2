# version: 0.0.3
# author: picklez

import cv2
import numpy
import random
import math
import imageio
import os
from datetime import datetime

cwd = os.getcwd()
filename = "testing"+str(datetime.now())+".gif"

height = 900
width = 1600
dots_defined = 1000

def draw_black(array):
    for col in range(len(array)):
        for row in range(len(array[-1])):
            array[col][row][0] = 0
            array[col][row][1] = 0
            array[col][row][2] = 0
    return array

def create_random_dots(array):
    amt_of_dots = dots_defined
    dot_array = []
    while amt_of_dots != 0:
        new_dot = []
        new_dot.append(random.randrange(1,height-1))
        new_dot.append(random.randrange(1,width-1))
        dot_array.append(new_dot)
        amt_of_dots -= 1
    return sorted(dot_array)

def find_distance(dot1, dot2):
    d_x = abs(dot2[0]) - abs(dot1[0])
    d_y = abs(dot2[1]) - abs(dot1[1])
    distance = math.sqrt((d_x*d_x)+(d_y*d_y))
    return round(distance, 2)
    
def nearest(dot_array): # returns the 10 nearest dot to a given dot
    nearest = {}
    for dot in dot_array:
        sub_nearest = {}
        distance_array = []
        sub_dot_array = dot_array.copy()
        sub_dot_array.remove(dot)
        for dot2 in sub_dot_array:
            distance = find_distance(dot, dot2)
            sub_nearest[str(distance)] = dot2
            distance_array.append(distance)
        distance_array=sorted(distance_array)
        to_add = []
        for i in range(10):
            to_add.append(sub_nearest[str(distance_array[i])])
        nearest[str(dot)] = to_add
    return nearest

def line(point1, point2):
    point1 = point1.replace("[","").replace("]","").split(", ")
    for i in range(len(point1)):
        point1[i] = int(point1[i])
    all_points_between = []
    # y = mx + b
    dtop = point2[0] - point1[0]
    dbot = point2[1] - point1[1]
    m = (dtop + 0.001) / (dbot + 0.001)
    b = point1[0] - (m * point1[1])
    if point1[1] < point2[1]:
        for i in range(point1[1],point2[1]):
            hy = (m*i)+b
            hy = math.trunc(hy)
            hold = [int(hy), int(i)]
            all_points_between.append(hold)
    if point1[1] > point2[1]:
        for i in range(point2[1],point1[1]):
            hy = (m*i)+b
            hy = math.trunc(hy)
            hold = [int(hy), int(i)]
            all_points_between.append(hold)
    return all_points_between

def draw_lines(new_image, nearest):
    for key in nearest:
        for point in nearest[key]:
            line_array = line(key, point)
            r_or_b = random.randrange(0,2)
            for point2 in line_array:
                if point2[0] != 0 and point2[0] <= height and point2[1] != 0 and point2[1] <= width:
                    if r_or_b == 0:
                        new_image[point2[0]][point2[1]][0] = 255
                        new_image[point2[0]][point2[1]][1] = 0
                        new_image[point2[0]][point2[1]][2] = 0
                    if r_or_b == 1:
                        new_image[point2[0]][point2[1]][0] = 0
                        new_image[point2[0]][point2[1]][1] = 0
                        new_image[point2[0]][point2[1]][2] = 255
    return new_image

def apply_dots(new_image, dot_array):
    for dot in dot_array:
        # center of dot
        if dot[0] != 0 and dot[0] <= height-1 and dot[1] != 0 and dot[1] <= width-1:
            new_image[dot[0]][dot[1]][0] = 255
            new_image[dot[0]][dot[1]][1] = 255
            new_image[dot[0]][dot[1]][2] = 255
    return new_image

def get_random_dot_movement_dict(dot_array):
    direction_dict = {}
    for i in range(len(dot_array)):
        direction_dict[i] = random.randrange(0,8)
    return direction_dict

def next_step(direction_value):
    if direction_value == 0:
        return -1, -1
    if direction_value == 1:
        return -1, 0
    if direction_value == 2:
        return -1, 1
    if direction_value == 3:
        return 0, -1
    if direction_value == 4:
        return 0, 1
    if direction_value == 5:
        return 1, -1
    if direction_value == 6:
        return 1, 0
    if direction_value == 7:
        return 1, 1

def next_step_new_array(dot_array, direction_dict):
    for i in range(len(dot_array)):
        direction = direction_dict[i]
        current_dot = dot_array[i]
        next_move = next_step(direction)
        if current_dot[0]+1 != 0 and current_dot[0]+1 != height and current_dot[1]+1 != 0 and current_dot[1]+1 != width:
            current_dot[0] = current_dot[0] + next_move[0]
            current_dot[1] = current_dot[1] + next_move[1]
        dot_array[i] = current_dot
    return dot_array

def create_image(ni):
    da = create_random_dots(ni)
    ni = apply_dots(ni, da)
    ndm = nearest(da)
    ni = draw_lines(ni, ndm)
    dd = get_random_dot_movement_dict(da)
    dans = next_step_new_array(da, dd)
    return ni, dd, dans

def move_image(bi, da, dd):
    bi = apply_dots(bi, da)
    ndm = nearest(da)
    bi = draw_lines(bi, ndm)
    dans = next_step_new_array(da, dd)
    return bi, dd, dans
    
# define our image array
new_image = numpy.empty((height,width,3))
new_image = draw_black(new_image)
blank_image = new_image.copy()

new_image, direction_dict, dot_array_next_step = create_image(new_image)
cv2.imwrite(cwd+"\\bin\\test0.png", new_image.copy())

for i in range(1,1000):
    new_image_2, direction_dict, dot_array_next_step = move_image(blank_image.copy(), dot_array_next_step, direction_dict)
    cv2.imwrite(cwd+"\\bin\\test"+str(i)+".png", new_image_2.copy())

import video_maker