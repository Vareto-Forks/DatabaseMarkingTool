__author__ = 'Amin'

import cv2

from os import listdir
from os.path import isfile, join, exists

import pickle

from ObjectInformation import ObjectInformation
from MouseButton import MouseButton

# GLOBALS - required for OpenCV mouse callback
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

    # IMPORTANT - PARAMETERS
    # there is a problem with images that are bigger than screen resolution
    # they are resized by this parameters
    # change to 1.0 if not resizing is needed
    scale_x = 1.0#0.8
    scale_y = 1.0#0.8

    # choose the part of the image that should be used
    # put (0, 0) and (width, height) if you want whole image
    roi_top_left_x = 698
    roi_top_left_y = 650
    roi_bottom_right_x = 1375 * scale_x
    roi_bottom_right_y = 1150 * scale_y

    # set the directories (relative or not) where the dataset is and where the descriptions should be placed
    # all of this directories have to exist
    dataset_name = "dataset_7"
    path_to_description = "description/" + dataset_name + "/"
    path_to_images = "datasets/" + dataset_name + "/"

    # END OF PARAMETERS LIST

    # CONSTANTS
    font = cv2.FONT_HERSHEY_SIMPLEX
    window_name = "image"

    # INITIALIZATION
    image_counter = 950#0
    flag_auto_load = False

    files = [f for f in listdir(path_to_images) if isfile(join(path_to_images, f))]

    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, mouse_callback)

    #img = cv2.imread("Desert.jpg", cv2.IMREAD_COLOR)
    #img_original = np.zeros((512, 512, 3), np.uint8)
    img_original = cv2.imread(path_to_images + files[image_counter], cv2.IMREAD_COLOR)
    img_original_resized = cv2.resize(img_original, (0, 0), None, fx=scale_x, fy=scale_y, interpolation=cv2.INTER_NEAREST)
    img_original_resized_roi = img_original_resized[roi_top_left_y:roi_bottom_right_y, roi_top_left_x:roi_bottom_right_x]

    key = 0
    while key != 27:

        if current_object is not None:
            # move selected object
            if key == ord('w'):
                current_object.move(0, -1)
            elif key == ord('s'):
                current_object.move(0, 1)
            elif key == ord('a'):
                current_object.move(-1, 0)
            elif key == ord('d'):
                current_object.move(1, 0)
            # resize selected object
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

            # choose object below
            elif key == ord('1'):
                current_object = select_object_below(objects_to_draw)

            # delete selected object
            elif key == ord('2'):
                objects_to_draw.remove(current_object)

            # change type to person
            elif key == ord('3'):
                current_object.change_type_to_person()

            # change type to car
            elif key == ord('4'):
                current_object.change_type_to_car()

            # change type to hidden
            elif key == ord('5'):
                current_object.change_type_to_hidden()

        # next image
        if key == ord('m'):
            image_counter += 1
            print "Image number: " + str(image_counter)
            img_original = cv2.imread(path_to_images + files[image_counter], cv2.IMREAD_COLOR)
            img_original_resized = cv2.resize(img_original, (0, 0), None, fx=scale_x, fy=scale_y, interpolation=cv2.INTER_NEAREST)
            img_original_resized_roi = img_original_resized[roi_top_left_y:roi_bottom_right_y, roi_top_left_x:roi_bottom_right_x]
            if flag_auto_load:
                file_to_open = path_to_description + str(image_counter) + "_" + files[image_counter] + ".pickle"
                if exists(file_to_open):
                    with open(file_to_open, "rb") as f:
                        objects_to_draw = pickle.load(f)

        # previous image
        elif key == ord('n'):
            image_counter -= 1
            print "Image number: " + str(image_counter)
            img_original = cv2.imread(path_to_images + files[image_counter], cv2.IMREAD_COLOR)
            img_original_resized = cv2.resize(img_original, (0, 0), None, fx=scale_x, fy=scale_y, interpolation=cv2.INTER_NEAREST)
            img_original_resized_roi = img_original_resized[roi_top_left_y:roi_bottom_right_y, roi_top_left_x:roi_bottom_right_x]
            if flag_auto_load:
                file_to_open = path_to_description + str(image_counter) + "_" + files[image_counter] + ".pickle"
                if exists(file_to_open):
                    with open(file_to_open, "rb") as f:
                        objects_to_draw = pickle.load(f)

        # save the descriptioon
        elif key == ord('p'):
            file_to_save = path_to_description + str(image_counter) + "_" + files[image_counter] + ".pickle"
            print file_to_save
            with open(file_to_save, "wb") as f:
                pickle.dump(objects_to_draw, f)

        # load the description
        elif key == ord('o'):
            file_to_open = path_to_description + str(image_counter) + "_" + files[image_counter] + ".pickle"
            if exists(file_to_open):
                with open(file_to_open, "rb") as f:
                    objects_to_draw = pickle.load(f)

        # toggle auto load of description (invoked when choosing next image)
        elif key == ord('l'):
            flag_auto_load = not flag_auto_load
            print "Auto load state: " + str(flag_auto_load)

        # remove all created objects
        elif key == ord('k'):
            objects_to_draw = []

        img_working = img_original_resized_roi.copy()
        # draw all stored objects
        for object_to_draw in objects_to_draw:
            object_to_draw.draw(img_working, font)

        cv2.imshow(window_name, img_working)
        key = cv2.waitKey(20)

    cv2.destroyAllWindows()
