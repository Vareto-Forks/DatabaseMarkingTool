__author__ = 'Amin'

import cv2

from os import listdir
from os.path import isfile, join, exists

import pickle

from ObjectInformation import ObjectInformation
from MouseButton import MouseButton

right_button = MouseButton()
left_button = MouseButton()

new_object = None
current_object = None
objects_to_draw = []


# mouse callback function
# left key is used for moving objects
# right key is used for creating new objects
def mouse_callback(event, x, y, flags, param):
    global current_object, new_object, objects_to_draw, right_button, left_button

    # right mouse button
    if event == cv2.EVENT_RBUTTONDOWN:
        right_button.callback_pressed(x, y)
        new_object = ObjectInformation()
        new_object.init(x, y, x+1, y+1, len(objects_to_draw))
        objects_to_draw.append(new_object)
    elif event == cv2.EVENT_RBUTTONUP:
        right_button.callback_released(x, y)
        new_object.finish(x, y)

    # mouse movement
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

    # left mouse button
    elif event == cv2.EVENT_LBUTTONDOWN:
        print x, y
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


def select_object_below(objects):
    object_below = None
    flag_start_checking = False
    selected_object = None
    for o in objects:
        if flag_start_checking:
            if o.check_if_inside(
                    selected_object.point_of_selection.x,
                    selected_object.point_of_selection.y
            ):
                selected_object.unselect()
                object_below = o
                object_below.select(selected_object.point_of_selection.x, selected_object.point_of_selection.y)
                break
        if o.selected:
            flag_start_checking = True
            selected_object = o

    return object_below


if __name__ == "__main__":

    dataset_name = "processed_6"
    path_to_description = "description/" + dataset_name + "/"
    path_to_images = "datasets/" + dataset_name + "/"

    files = [f for f in listdir(path_to_images) if isfile(join(path_to_images, f))]

    image_counter = 0
    flag_auto_load = False

    font = cv2.FONT_HERSHEY_SIMPLEX

    window_name = "image"

    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, mouse_callback)

    scale_x = 0.8
    scale_y = 0.8

    #img = cv2.imread("Desert.jpg", cv2.IMREAD_COLOR)
    #img_original = np.zeros((512, 512, 3), np.uint8)
    img_original = cv2.imread(path_to_images + files[image_counter], cv2.IMREAD_COLOR)
    img_original_resized = cv2.resize(img_original, (0, 0), None, fx=scale_x, fy=scale_y, interpolation=cv2.INTER_NEAREST)

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
                current_object = select_object_below(objects_to_draw)

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
            print "Image number: " + str(image_counter)
            img_original = cv2.imread(path_to_images + files[image_counter], cv2.IMREAD_COLOR)
            img_original_resized = cv2.resize(img_original, (0, 0), None, fx=scale_x, fy=scale_y, interpolation=cv2.INTER_NEAREST)
            if flag_auto_load:
                file_to_open = path_to_description + str(image_counter) + "_" + files[image_counter] + ".pickle"
                if exists(file_to_open):
                    with open(file_to_open, "rb") as f:
                        objects_to_draw = pickle.load(f)

        elif key == ord('n'):
            image_counter -= 1
            print "Image number: " + str(image_counter)
            img_original = cv2.imread(path_to_images + files[image_counter], cv2.IMREAD_COLOR)
            img_original_resized = cv2.resize(img_original, (0, 0), None, fx=scale_x, fy=scale_y, interpolation=cv2.INTER_NEAREST)
            if flag_auto_load:
                file_to_open = path_to_description + str(image_counter) + "_" + files[image_counter] + ".pickle"
                if exists(file_to_open):
                    with open(file_to_open, "rb") as f:
                        objects_to_draw = pickle.load(f)

        elif key == ord('p'):
            file_to_save = path_to_description + str(image_counter) + "_" + files[image_counter] + ".pickle"
            print file_to_save
            with open(file_to_save, "wb") as f:
                pickle.dump(objects_to_draw, f)

        elif key == ord('o'):
            file_to_open = path_to_description + str(image_counter) + "_" + files[image_counter] + ".pickle"
            if exists(file_to_open):
                with open(file_to_open, "rb") as f:
                    objects_to_draw = pickle.load(f)

        elif key == ord('l'):
            flag_auto_load = not flag_auto_load
            print "Auto load state: " + str(flag_auto_load)

        # remove all created objects
        elif key == ord('k'):
            objects_to_draw = []

        img_working = img_original_resized.copy()
        # draw all stored objects
        for object_to_draw in objects_to_draw:
            object_to_draw.draw(img_working, font)

        cv2.imshow(window_name, img_working)
        key = cv2.waitKey(20)

    cv2.destroyAllWindows()
