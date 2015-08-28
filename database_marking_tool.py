__author__ = 'Amin'

import cv2
import numpy as np

import pickle

from ObjectInformation import ObjectInformation
from MouseButton import MouseButton


def enum(**enums):
    return type('Enum', (), enums)

STATE = enum(idle=0, left_clicked_outside=1, left_clicked_inside=2)

right_button = MouseButton()
left_button = MouseButton()

new_object = None
current_object = None
objects_to_draw = []

state = STATE.idle

id_counter = 0


# mouse callback function
# left key is used for moving objects
# right key is used for creating new objects
def mouse_callback(event, x, y, flags, param):
    global current_object, new_object, objects_to_draw, right_button, left_button, id_counter
    #global state, previous_x, previous_y

    # right mouse button
    if event == cv2.EVENT_RBUTTONDOWN:
        right_button.callback_pressed(x, y)
        new_object = ObjectInformation()
        new_object.init(x, y, x+1, y+1, id_counter)
        id_counter += 1
        objects_to_draw.append(new_object)
    elif event == cv2.EVENT_RBUTTONUP:
        right_button.callback_released(x, y)
        new_object.finish(x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if right_button.is_pressed:
            right_button.callback_moved(x, y)
            new_object.resize(x, y)
        if left_button.is_pressed:
            if current_object is not None and current_object.selected:
                dx = (x-left_button.get_previous_location_x())
                dy = (y-left_button.get_previous_location_y())
                current_object.move(dx, dy)

            left_button.callback_moved(x, y)

    elif event == cv2.EVENT_LBUTTONDOWN:
        left_button.callback_pressed(x, y)

        for object_to_draw in objects_to_draw:
            object_to_draw.unselect()

        for object_to_draw in objects_to_draw:
            if object_to_draw.check_if_inside(x, y):
                current_object = object_to_draw
                current_object.select(x, y)
                break

    elif event == cv2.EVENT_LBUTTONUP:
        left_button.callback_released(x, y)


from os import listdir
from os.path import isfile, join


if __name__ == "__main__":

    path_to_decription = "description/processed_1/"

    path_to_images = "datasets/processed_1/"
    files = [f for f in listdir(path_to_images) if isfile(join(path_to_images, f))]
    image_counter = 0

    font = cv2.FONT_HERSHEY_SIMPLEX

    window_name = "image"

    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, mouse_callback)

    #img = cv2.imread("Desert.jpg", cv2.IMREAD_COLOR)
    #img_original = np.zeros((512, 512, 3), np.uint8)
    img_original = cv2.imread(path_to_images + files[image_counter], cv2.IMREAD_COLOR)

    key = 0
    while key != 27:

        if current_object is not None:
            if key == ord('w'):
                current_object.move(0, -1)
            elif key == ord('s'):
                current_object.move(0, 1)
            elif key == ord('a'):
                current_object.move(-1, 0)
            elif key == ord('d'):
                current_object.move(1, 0)
            elif key == ord('q'):
                current_object.increase_size(top=-1)
            elif key == ord('z'):
                current_object.increase_size(top=1)
            elif key == ord('Q'):
                current_object.increase_size(down=1)
            elif key == ord('Z'):
                current_object.increase_size(down=-1)
            elif key == ord('e'):
                current_object.increase_size(left=-1)
            elif key == ord('c'):
                current_object.increase_size(left=1)
            elif key == ord('E'):
                current_object.increase_size(right=1)
            elif key == ord('C'):
                current_object.increase_size(right=-1)

            elif key == ord('1'):
                flag_start_checking = False
                selected_object = None
                for object_to_draw in objects_to_draw:
                    if flag_start_checking:
                        if object_to_draw.check_if_inside(
                                selected_object.point_of_selection.x,
                                selected_object.point_of_selection.y
                        ):
                            selected_object.unselect()
                            current_object = object_to_draw
                            current_object.select(selected_object.point_of_selection.x, selected_object.point_of_selection.y)
                            break
                    if object_to_draw.selected:
                        flag_start_checking = True
                        selected_object = object_to_draw

            elif key == ord('2'):
                objects_to_draw.remove(current_object)

            elif key == ord('3'):
                current_object.change_type_to_person()

            elif key == ord('4'):
                current_object.change_type_to_car()

            elif key == ord('5'):
                current_object.change_type_to_hidden()

        if key == ord('m'):
            image_counter += 1
            img_original = cv2.imread(path_to_images + files[image_counter], cv2.IMREAD_COLOR)

        if key == ord('n'):
            image_counter -= 1
            img_original = cv2.imread(path_to_images + files[image_counter], cv2.IMREAD_COLOR)

        if key == ord('p'):
            file_to_save = path_to_decription + str(image_counter) + "_" + files[image_counter] + ".pickle"
            print file_to_save
            with open(file_to_save, "wb") as f:
                pickle.dump(objects_to_draw, f)

        if key == ord('o'):
            file_to_open = path_to_decription + str(image_counter) + "_" + files[image_counter] + ".pickle"
            with open(file_to_open, "rb") as f:
                objects_to_draw = pickle.load(f)



        img_working = img_original.copy()
        # draw all stored objects
        for object_to_draw in objects_to_draw:
            object_to_draw.draw(img_working, font)

        cv2.imshow(window_name, img_working)
        key = cv2.waitKey(20)

    cv2.destroyAllWindows()
