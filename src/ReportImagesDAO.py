from src.Connection import Connection
from src.ReportImages import ReportImages
from src.DAO import DAO


class ReportImagesDAO(DAO):

    def __init__(self):
        DAO.__init__(self)

    def create(self, report_images: ReportImages):
        cursor = self.connection.cursor()
        # For inserting new images into table
        create_report_images = """
        INSERT INTO `surfdb`.`ReportImages`
        (`ReportImagesKey`, `TimeBlockHourStart`, `TimeBlockDirectory`)
        VALUES (%s, %s, %s)
        """

        values = [(report_images.report_images_key,
                  report_images.time_block_hour_start,
                  report_images.report_images_directory)]

        print(create_report_images)
        cursor.executemany(create_report_images, values)
        return report_images

    def get_image_report_by_key(self, key):
        pass

    def select_all(self):
        select_statement = "SELECT * FROM `surfdb`.`ReportImages`"
        all_rows = self.execute_read_query(select_statement)

        for row in all_rows:
            print(row)