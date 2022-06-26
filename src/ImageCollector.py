from DataCollector import DataCollector
import os
from datetime import datetime, date
import time
from grabFrame import hidden_video_url_extractor, get_video_frame
import errno, stat, shutil

class ImageCollector(DataCollector):

    def __init__(self, end_collection_date, initial_daylight_start_hour, initial_daylight_end_hour,
                 experiment_data_folder, video_url):
        super().__init__(end_collection_date, initial_daylight_start_hour, initial_daylight_end_hour,
                         experiment_data_folder)
        self.video_url = hidden_video_url_extractor(video_url)
        self.image_experiment_folder = os.path.join(self.local_path, 'images')
        print(self.image_experiment_folder)
        
    def collect_images_for_hour(self, num_images_per_hour, current_day_image_path):
        images_collected_current_hour = 0
        image_collection_time_frame = 3600 / num_images_per_hour

        while images_collected_current_hour < num_images_per_hour:

            next_image_acquisition_time_in_seconds = (images_collected_current_hour * image_collection_time_frame)

            current_hour = datetime.now().hour
            current_minute = datetime.now().minute
            current_seconds_in_hour = datetime.now().second + current_minute * 60
            print('Current Seconds: ', current_seconds_in_hour)
            print('Next Collection Time: ', next_image_acquisition_time_in_seconds)
            while current_seconds_in_hour < next_image_acquisition_time_in_seconds:
                time.sleep(.5)
                current_hour = datetime.now().hour
                current_seconds_in_hour = datetime.now().second + datetime.now().minute * 60

            # Wait over, grab frame, reset times
            im_filename = os.path.join(current_day_image_path, str(current_hour) + '_'
                                       + str(images_collected_current_hour) + '.png')     
            get_video_frame(self.video_url, current_day_image_path, im_filename)

            current_hour = datetime.now().hour
            images_collected_current_hour += 1

            print('Hour: ', current_hour, '||', 'Images Collected: ', images_collected_current_hour)
            
    def handleRemoveReadonly(func, path, exc):
        excvalue = exc[1]
        if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
          os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
          func(path)
        else:
          raise
          
    def collect_images_for_day(self, num_images_per_hour):
        current_day = date.today()
        current_day_image_path = os.path.join(self.image_experiment_folder, str(current_day))

        # Erase a previous folder if it was created
        if os.path.exists(current_day_image_path):
            shutil.rmtree(current_day_image_path, ignore_errors=False, onerror=self.handleRemoveReadonly)
            # os.remove(current_day_image_path)
        os.makedirs(current_day_image_path)
        os.chmod(current_day_image_path,0o777)

        current_hour = datetime.now().hour

        # Collects daylight specified hours only, 24 hour time
        while self.initial_day_end_hour >= current_hour >= self.initial_day_start_hour:  # less or equal to?
            self.video_url = hidden_video_url_extractor(video_url)
            self.collect_images_for_hour(num_images_per_hour, current_day_image_path)
            last_hour = current_hour
            current_hour = datetime.now().hour

            while last_hour == current_hour:
                time.sleep(1)
                current_hour = datetime.now().hour

    def collect_set_number_images_per_hour(self, num_images_per_hour=30):
        assert 3600 % num_images_per_hour == 0  # Keep it divisible by number of seconds in an hour for now until that can be fixed

        current_day = date.today()

        # Outer loop, collects until the specified date
        while current_day < self.end_collection_date:
            self.collect_images_for_day(num_images_per_hour)
            current_day = date.today()
            current_day_image_path = os.path.join(self.image_experiment_folder, str(current_day))
            os.makedirs(current_day_image_path, exist_ok=True)
            os.chmod(current_day_image_path,0o777)

end_date = date(2022, 4, 20)
daylight_start_hour = 5
daylight_end_hour = 8 + 12  # 24 hour time, this would be 7 PM
experiment_data_folder = 'init_data_test'
video_url = 'https://www.youtube.com/watch?v=NqhAaA2mGcA'

im_collect = ImageCollector(end_date, daylight_start_hour, daylight_end_hour, experiment_data_folder, video_url)

images_per_hour = 30

im_collect.collect_set_number_images_per_hour(images_per_hour)
