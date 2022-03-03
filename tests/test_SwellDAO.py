from unittest import TestCase

import definitions
from src.Swell import Swell
from src.SwellDAO import SwellDAO
import pandas as pd
import os


class TestSwellDAO(TestCase):

    def test_create_table(self):
        swellDAO = SwellDAO()

        swellDAO.create_table()
        tables = swellDAO.show_tables()
        tables_list = [elem[0] for elem in tables]

        if ('SwellStaging') not in tables_list:
            self.fail()

    def test_empty_swell_staging(self):
        swellDAO = SwellDAO()

        swellDAO.create_table()

        swellDAO.drop_table_if_exists()
        tables = swellDAO.show_tables()
        tables_list = [elem[0] for elem in tables]

        if ('SwellStaging') in tables_list:
            self.fail()

    def test_insert_csv_into_database(self):

        swellDAO = SwellDAO()
        swellDAO.drop_table_if_exists()
        swellDAO.create_table()
        test_data_path = os.path.join(definitions.ROOT_DIR, 'testdata/testWaveDataWithHeaders.csv')
        swell1 = Swell(test_data_path)

        data = pd.read_csv(test_data_path, encoding='unicode_escape')
        df = pd.DataFrame(data)

        try:
            swellDAO.insert_csv_into_database(swell1)
        except:
            self.fail()

        rows_inserted = swellDAO.select_all_swell_staging()
        if len(rows_inserted) != df.shape[0]:
            self.fail()
