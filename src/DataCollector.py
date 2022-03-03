from definitions import ROOT_DIR
import os


class DataCollector:

    def __init__(self, end_collection_date, initial_daylight_start_hour, initial_daylight_end_hour, experiment_data_folder):
        self.end_collection_date = end_collection_date
        self.initial_day_start_hour = initial_daylight_start_hour
        self.initial_day_end_hour = initial_daylight_end_hour
        self.experiment_data_path = os.path.join(ROOT_DIR, 'data', experiment_data_folder)

        os.makedirs(self.experiment_data_path, exist_ok=True)


