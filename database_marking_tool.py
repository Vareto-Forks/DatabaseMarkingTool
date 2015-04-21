__author__ = 'Amin'

import cv2
import numpy as np

import math

def enum(**enums):
    return type('Enum', (), enums)

STATE = enum(idle=0, left_clicked_outside=1, left_clicked_inside=2)


class ObjectInformation:
    def __init__(self):
        self.centre = (0, 0)
        self.width = 0
        self.height = 0

        self.point_1 = (0, 0)
        self.point_2 = (0, 0)
        self._update_based_on_points()

        self.type = "type"
        #self.description = "object"

    def init(self, x1, y1, x2, y2):
        self.point_1 = (x1, y1)
        self.point_2 = (x2, y2)
        self.type = "temporary"
        self._update_based_on_points()

    def resize(self, x2, y2):
        self.point_2 = (x2, y2)
        self._update_based_on_points()

    def finish(self, x2, y2):
        self.point_2 = (x2, y2)
        self.type = "permanent"
        self._update_based_on_points()

    def move(self, dx, dy):
        x_centre = self.centre[0] + dx
        y_centre = self.centre[1] + dy
        self.centre = (x_centre, y_centre)
        self._update_base_on_centre()

    def _update_based_on_points(self):
        x1 = self.point_1[0]
        x2 = self.point_2[0]
        y1 = self.point_1[1]
        y2 = self.point_2[1]

        self.centre = ((x1 + x2)/2.0, (y1 + y2)/2.0)
        self.width = abs(x1-x2)
        self.height = abs(y1-y2)

    def _update_base_on_centre(self):
        x_centre = self.centre[0]
        y_centre = self.centre[1]
        x1 = int(x_centre - math.floor(self.width/2))
        x2 = int(x_centre + math.floor(self.width/2))
        y1 = int(y_centre - math.floor(self.height/2))
        y2 = int(y_centre + math.floor(self.height/2))

        self.point_1 = (x1, y1)
        self.point_2 = (x2, y2)

    def check_if_inside(self, x, y):
        x1 = self.point_1[0]
        x2 = self.point_2[0]
        y1 = self.point_1[1]
        y2 = self.point_2[1]

        result_x = False

        if x1 > x2:
            if x2 <= x <= x1:
                result_x = True
        else:
            if x1 <= x <= x2:
                result_x = True

        result_y = False

        if y1 > y2:
            if y2 <= y <= y1:
                result_y = True
        else:
            if y1 <= y <= y2:
                result_y = True

        result = False
        if result_x and result_y:
            result = True

        return result

objects_to_draw = []

current_object = None

state = STATE.idle

point_upper_left = (0, 0)
point_bottom_right = (0, 0)

previous_x = 0
previous_y = 0

# mouse callback function
def mouse_callback(event, x, y, flags, param):
    global state, current_object, objects_to_draw, previous_x, previous_y

    if state == STATE.idle:

        if event == cv2.EVENT_LBUTTONDOWN:

            is_clicked_inside = False
            for object_to_draw in objects_to_draw:
                if object_to_draw.check_if_inside(x, y):
                    is_clicked_inside = True
                    break

            if is_clicked_inside:
                current_object = object_to_draw
                previous_x = x
                previous_y = y
                state = STATE.left_clicked_inside
            else:
                current_object = ObjectInformation()
                current_object.init(x, y, x+1, y+1)
                objects_to_draw.append(current_object)
                state = STATE.left_clicked_outside

    elif state == STATE.left_clicked_outside:

        if event == cv2.EVENT_LBUTTONUP:
            current_object.finish(x, y)
            state = STATE.idle

        elif event == cv2.EVENT_MOUSEMOVE:
            current_object.resize(x, y)

    elif state == STATE.left_clicked_inside:
        if event == cv2.EVENT_LBUTTONUP:
            state = STATE.idle

        elif event == cv2.EVENT_MOUSEMOVE:
            dx = (x-previous_x)
            dy = (y-previous_y)
            current_object.move(dx, dy)
            previous_x = x
            previous_y = y

    else:
        pass


if __name__ == "__main__":

    window_name = "image"

    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, mouse_callback)

    #img = cv2.imread("Desert.jpg", cv2.IMREAD_COLOR)
    img_original = np.zeros((512, 512, 3), np.uint8)

    cv2.rectangle(img_original, (10, 10), (100, 100), (255, 0, 0), 10)

    key = 0
    while key != 27:
        img_working = img_original.copy()
        # draw all stored objects
        for object_to_draw in objects_to_draw:
            if object_to_draw.type == "temporary":
                cv2.rectangle(img_working, object_to_draw.point_1, object_to_draw.point_2, (0, 100, 255), 1)
            else:
                cv2.rectangle(img_working, object_to_draw.point_1, object_to_draw.point_2, (0, 0, 255), 3)
        cv2.imshow(window_name, img_working)
        key = cv2.waitKey(20)

    cv2.destroyAllWindows()
