__author__ = 'Amin'


class MouseButton:
    def __init__(self):
        self.previous_x = 0
        self.previous_y = 0
        self.is_pressed = False

    def update_previous_location(self, x, y):
        self.previous_x = x
        self.previous_y = y

    def get_previous_location_x(self):
        return self.previous_x

    def get_previous_location_y(self):
        return self.previous_y

    def callback_pressed(self, x, y):
        self.update_previous_location(x, y)
        self.is_pressed = True

    def callback_released(self, x, y):
        self.is_pressed = False

    def callback_moved(self, x, y):
        if self.is_pressed:
            self.update_previous_location(x, y)