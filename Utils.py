__author__ = 'Amin'

from os import listdir
from os.path import isfile, join, exists

import cv2
import pickle

from lxml import etree


class Utils:
    def __init__(self):
        # IMPORTANT - PARAMETERS
        # there is a problem with images that are bigger than screen resolution
        # they are resized by this parameters
        # change to 1.0 if not resizing is needed
        # self.scale_x = 1.0
        # self.scale_y = 1.0

        self.scale_x = 0.8
        self.scale_y = 0.8

        # choose the part of the image that should be used
        # put (0, 0) and (width, height) if you want whole image
        # self.roi_top_left_x = 698
        # self.roi_top_left_y = 650
        # self.roi_bottom_right_x = 1375 * self.scale_x
        # self.roi_bottom_right_y = 1150 * self.scale_y

        self.roi_top_left_x = 0
        self.roi_top_left_y = 0
        self.roi_bottom_right_x = 1600 * self.scale_x
        self.roi_bottom_right_y = 1200 * self.scale_y

        # set the directories (relative or not) where the dataset is and where the descriptions should be placed
        # all of this directories have to exist
        #self.dataset_name = "dataset_7"
        self.dataset_name = "processed_6"
        self.path_to_description = "description/" + self.dataset_name + "/"
        self.path_to_images = "datasets/" + self.dataset_name + "/"

        self.image_counter_start = 900
        self.image_counter_stop = self.image_counter_start + 630#360#630

        # END OF PARAMETERS LIST

        # CONSTANTS
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def load_and_resize_image(self, filename):
        img_original = cv2.imread(self.path_to_images + filename, cv2.IMREAD_COLOR)
        img_original_resized = cv2.resize(img_original, (0, 0), None,
                                          fx=self.scale_x, fy=self.scale_y,
                                          interpolation=cv2.INTER_NEAREST
        )
        img_original_resized_roi = img_original_resized[
                                   self.roi_top_left_y:self.roi_bottom_right_y,
                                   self.roi_top_left_x:self.roi_bottom_right_x
        ]
        return img_original_resized_roi

    def create_video(self):
        # INITIALIZATION
        window_name = "image"
        cv2.namedWindow(window_name)
        files = [f for f in listdir(self.path_to_images) if isfile(join(self.path_to_images, f))]

        img = self.load_and_resize_image(files[self.image_counter_start])
        height, width, layers = img.shape
        video = cv2.VideoWriter("video\\" + self.dataset_name + ".avi", -1, 10, (width, height))

        for image_counter in range(self.image_counter_start, self.image_counter_stop, 1):

            img = self.load_and_resize_image(files[image_counter])

            file_to_open = self.path_to_description + str(image_counter) + "_" + files[image_counter] + ".pickle"
            print file_to_open
            if exists(file_to_open):
                with open(file_to_open, "rb") as f:
                    objects_to_draw = pickle.load(f)
                    for object_to_draw in objects_to_draw:
                        object_to_draw.draw(img, self.font)
            cv2.imshow(window_name, img)
            cv2.waitKey(20)
            video.write(img)

        cv2.destroyAllWindows()
        video.release()

    def prepare_roi(self):
        path_to_roi_images = "datasets/" + self.dataset_name + "_roi/"

        files = [f for f in listdir(self.path_to_images) if isfile(join(self.path_to_images, f))]

        for image_counter in range(self.image_counter_start, self.image_counter_stop, 1):

            img = self.load_and_resize_image(files[image_counter])

            cv2.imwrite(path_to_roi_images + files[image_counter] + ".png", img)

    def prepare_xml(self):

        files = [f for f in listdir(self.path_to_description) if isfile(join(self.path_to_description, f))]

        xml_name = "PUT_Surveillance_database_sequence_3"

        # Create the root element
        page = etree.Element(xml_name)

        # Make a new document tree
        doc = etree.ElementTree(page)

        # For multiple multiple attributes, use as shown above
        for filename in files:
            # Add the subelements
            pageElement = etree.SubElement(page, 'Image',
                                           name=filename)
            with open(self.path_to_description + filename, "rb") as f:
                    objects_to_draw = pickle.load(f)
                    for object_to_draw in objects_to_draw:

                        top_left_x = int(round(object_to_draw.point_top_left.x * 1/self.scale_x, 0))
                        top_left_y = int(round(object_to_draw.point_top_left.y * 1/self.scale_y, 0))

                        bottom_right_x = int(round(object_to_draw.point_bottom_right.x * 1/self.scale_x, 0))
                        bottom_right_y = int(round(object_to_draw.point_bottom_right.y * 1/self.scale_y, 0))


                        if object_to_draw.type != "hidden":
                            etree.SubElement(pageElement, 'Object',
                                             type=object_to_draw.type,
                                             #center_of_gravity_x=str(object_to_draw.centre.x),
                                             #center_of_gravity_y=str(object_to_draw.centre.y),
                                             minimal_bounding_box_top_left_x=str(top_left_x),
                                             minimal_bounding_box_top_left_y=str(top_left_y),
                                             minimal_bounding_box_bottom_right_x=str(bottom_right_x),
                                             minimal_bounding_box_bottom_right_y=str(bottom_right_y)
                            )

        # Save to XML file
        outFile = open("xml/" + xml_name + '.xml', 'w')
        doc.write(outFile, pretty_print=True, xml_declaration=True, encoding='utf-8')

if __name__ == "__main__":
    u = Utils()
    #u.create_video()
    u.prepare_xml()
    #u.prepare_roi()
