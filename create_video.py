__author__ = 'Amin'

import cv2
import pickle

from os import listdir
from os.path import isfile, join, exists

from ObjectInformation import ObjectInformation

if __name__ == "__main__":

    dataset_name = "processed_5"
    path_to_description = "description/" + dataset_name + "/"
    path_to_images = "datasets/" + dataset_name + "/"

    font = cv2.FONT_HERSHEY_SIMPLEX

    files = [f for f in listdir(path_to_images) if isfile(join(path_to_images, f))]

    img_original = cv2.imread(path_to_images + files[0], cv2.IMREAD_COLOR)
    scale_x = 0.8
    scale_y = 0.8
    img_original_resized = cv2.resize(img_original, (0, 0), None, fx=scale_x, fy=scale_y, interpolation=cv2.INTER_NEAREST)

    height, width, layers = img_original_resized.shape
    video = cv2.VideoWriter('video.avi', -1, 10, (width, height))

    for i, filename in enumerate(files):
        img_original = cv2.imread(path_to_images + filename, cv2.IMREAD_COLOR)
        img_original_resized = cv2.resize(img_original, (0, 0), None, fx=scale_x, fy=scale_y, interpolation=cv2.INTER_NEAREST)
        file_to_open = path_to_description + str(i) + "_" + filename + ".pickle"
        print file_to_open
        if exists(file_to_open):
            with open(file_to_open, "rb") as f:
                objects_to_draw = pickle.load(f)
                for object_to_draw in objects_to_draw:
                    object_to_draw.draw(img_original_resized, font)
        video.write(img_original_resized)

        #if i == 10:
            #break

    cv2.destroyAllWindows()
    video.release()
