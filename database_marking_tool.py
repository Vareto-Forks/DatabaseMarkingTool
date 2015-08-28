__author__ = 'Amin'

import cv2
import numpy as np

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

#previous_x = 0
#previous_y = 0


# mouse callback function
# left key is used for moving objects
# right key is used for creating new objects
def mouse_callback(event, x, y, flags, param):
    global current_object, new_object, objects_to_draw, right_button, left_button
    #global state, previous_x, previous_y

    # right mouse button
    if event == cv2.EVENT_RBUTTONDOWN:
        right_button.callback_pressed(x, y)
        new_object = ObjectInformation()
        new_object.init(x, y, x+1, y+1)
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

    # if state == STATE.idle:
    #
    #     if event == cv2.EVENT_LBUTTONDOWN:
    #
    #         is_clicked_inside = False
    #         for object_to_draw in objects_to_draw:
    #             if object_to_draw.check_if_inside(x, y):
    #                 is_clicked_inside = True
    #                 break
    #
    #         if is_clicked_inside:
    #             current_object = object_to_draw
    #             current_object.selected = True
    #             previous_x = x
    #             previous_y = y
    #             state = STATE.left_clicked_inside
    #         else:
    #             current_object = ObjectInformation()
    #             current_object.init(x, y, x+1, y+1)
    #             objects_to_draw.append(current_object)
    #             state = STATE.left_clicked_outside
    #
    # elif state == STATE.left_clicked_outside:
    #
    #     if event == cv2.EVENT_LBUTTONUP:
    #         current_object.finish(x, y)
    #         state = STATE.idle
    #
    #     elif event == cv2.EVENT_MOUSEMOVE:
    #         current_object.resize(x, y)
    #
    # elif state == STATE.left_clicked_inside:
    #     if event == cv2.EVENT_LBUTTONUP:
    #         current_object.selected = False
    #         state = STATE.idle
    #
    #     elif event == cv2.EVENT_MOUSEMOVE:
    #         dx = (x-previous_x)
    #         dy = (y-previous_y)
    #         current_object.move(dx, dy)
    #         previous_x = x
    #         previous_y = y
    #
    # else:
    #     pass

if __name__ == "__main__":

    window_name = "image"

    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, mouse_callback)

    #img = cv2.imread("Desert.jpg", cv2.IMREAD_COLOR)
    img_original = np.zeros((512, 512, 3), np.uint8)

    font = cv2.FONT_HERSHEY_SIMPLEX

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


        img_working = img_original.copy()
        # draw all stored objects
        for object_to_draw in objects_to_draw:
            object_to_draw.draw(img_working, font)

        cv2.imshow(window_name, img_working)
        key = cv2.waitKey(20)

    cv2.destroyAllWindows()
