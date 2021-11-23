from unittest import TestCase

from src.Swell import Swell
from src.SwellDAO import SwellDAO


class TestSwellDAO(TestCase):

    def test_insert_csv_into_database(self):

        swellDAO = SwellDAO()
        swellDAO.select_all_swell_staging()

        test_data_path ='testdata/testWaveData.csv'
        swell1 = Swell(test_data_path)

        try:
            swellDAO.insert_csv_into_database(swell1)
        except:
            self.fail()

        swellDAO.select_all_swell_staging()

