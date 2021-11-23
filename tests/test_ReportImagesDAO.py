import os
from unittest import TestCase
from src.ReportImages import ReportImages
from src.ReportImagesDAO import ReportImagesDAO
import definitions


class TestReportImagesDAO(TestCase):

    def test_create(self):

        reportDAO = ReportImagesDAO()
        reportDAO.select_all()
        test_data = os.path.join(definitions.ROOT_DIR, 'testdata/05031995/00-03')
        report1 = ReportImages(1, 0, test_data)

        try:
            report1 = reportDAO.create(report1)
        except:
            self.fail()

        reportDAO.select_all()

    # def test_get_image_report_by_key(self):
    # self.fail()
