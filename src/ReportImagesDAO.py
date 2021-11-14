import Connection
import ReportImages


class ReportImagesDAO(DAO):

    def __init__(self):
        DAO.__init__(self)

    def create(self, report_images: ReportImages):
        # For inserting new images into table
        create_report_images = """
        INSERT INTO
        ReportImages(ReportImagesKey, TimeBlockHourStart, TimeBlockDirectory)
        VALUES(%d, %d, %s)
        """ % (report_images.report_images_key,
               report_images.time_block_hour_start,
               report_images.report_images_directory)

        execute_query(self, create_report_images)
        return report_images

    def get_image_report_by_key(self, key):
        pass
