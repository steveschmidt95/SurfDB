import os


from definitions import ROOT_DIR
from datetime import datetime, date
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from random import randint

plt.interactive(False)


class DayData:

    def __init__(self, experiment_name, date):
        self.date_path = os.path.join(ROOT_DIR, 'data', experiment_name, 'images', str(date))

    def get_hour_data_filenames(self, hour):
        day_images = os.listdir(self.date_path)
        hour_images = [image for image in day_images if image.startswith(str(hour)) and image.endswith('.png')]
        hour_images.sort()
        return hour_images

    def get_image_dims(self, hour):
        image_list = self.get_hour_data_filenames(hour)
        im1 = os.path.join(self.date_path, image_list[0])
        image = Image.open(im1)
        return image.size

    def get_hour_data_images(self, hour):
        image_list = self.get_hour_data_filenames(hour)
        num_images = len(image_list)
        image_size = self.get_image_dims(hour)

        image_array = np.zeros((num_images, image_size[1], image_size[0], 3), dtype=np.uint8)  # 3 for color
        for idx, image in enumerate(image_list):
            image_array[idx, :, :, :] = np.asarray(Image.open(os.path.join(self.date_path, image)))
        return image_array
