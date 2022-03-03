from src.DataCollector import DataCollector
import os
from datetime import datetime, date
import time
from grabFrame import hidden_video_url_extractor, get_video_frame


class ImageCollector(DataCollector):

    def __init__(self, end_collection_date, initial_daylight_start_hour, initial_daylight_end_hour,
                 experiment_data_folder, video_url):
        super().__init__(end_collection_date, initial_daylight_start_hour, initial_daylight_end_hour,
                         experiment_data_folder)
        self.video_url = hidden_video_url_extractor(video_url)
        self.image_experiment_folder = os.path.join(self.experiment_data_path, 'images')

    def collect_set_number_images_per_hour(self, num_images_per_hour=30):

        assert 3600 % num_images_per_hour == 0 # Keep it divisible by number of seconds in an hour for now until that can be fixed

        current_day = date.today()
        current_day_image_path = os.path.join(self.image_experiment_folder, str(current_day))
        os.makedirs(current_day_image_path , exist_ok=True)
        image_collection_time_frame = 3600 / num_images_per_hour

        # Outer loop, collects until the specified date
        while current_day < self.end_collection_date:

            current_hour = datetime.now().hour
            current_day = date.today()
            images_collected_current_hour = 0

            # Collects daylight specified hours only, 24 hour time
            while self.initial_day_end_hour > current_hour > self.initial_day_start_hour:

                next_image_acquisition_time_in_seconds = (images_collected_current_hour * image_collection_time_frame)

                current_hour = datetime.now().hour
                current_minute = datetime.now().minute
                current_seconds_in_hour = datetime.now().second + current_minute * 60
                while current_seconds_in_hour < next_image_acquisition_time_in_seconds:
                    time.sleep(.5)
                    current_seconds_in_hour = datetime.now().second + current_minute * 60

                # Wait over, grab frame, reset times
                im_filename = os.path.join(current_day_image_path, str(current_hour) + '_'
                                           + str(images_collected_current_hour) + '.png')
                get_video_frame(self.video_url, current_day_image_path, im_filename)
                current_hour = datetime.now().hour
                images_collected_current_hour += 1


end_date = date(2022, 3, 5)
daylight_start_hour = 5
daylight_end_hour = 7+12 # 24 hour time, this would be 7 PM
experiment_data_folder = 'init_data_test'
video_url = 'https://www.youtube.com/watch?v=NqhAaA2mGcA'
im_collect = ImageCollector(end_date, daylight_start_hour, daylight_end_hour, experiment_data_folder, video_url)

im_collect.collect_set_number_images_per_hour()
