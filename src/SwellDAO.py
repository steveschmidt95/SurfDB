import definitions
from src.Swell import Swell
from src.DAO import DAO
import pandas as pd
import os
from datetime import datetime


class SwellDAO(DAO):

    def __init__(self):
        DAO.__init__(self)

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS `surfdb`.`SwellStaging`(
                        `SwellStagingKey` BIGINT NOT NULL AUTO_INCREMENT,
                        `ReportGenerationDate` DATE,
                        `GenerationHour` INT, 
                        `ReportForecastDate` DATE,
                        `ForecastHour` INT,
                        `TideHeight` DOUBLE,
                        `SurfMin` DOUBLE,
                        `SurfMax` DOUBLE,
                        `SurfOptimalScore` DOUBLE,
                        `WindDirection` DOUBLE,
                        `WindSpeed` DOUBLE,
                        `WindGust` DOUBLE,
                        `Temperature` MEDIUMINT,
                        `Swell1Height` DOUBLE,
                        `Swell1Direction` DOUBLE,
                        `Swell1SwellMinDirection` DOUBLE,
                        `Swell1Period` DOUBLE,
                        `Swell1OptimalScore` DOUBLE,
                        `Swell2Height` DOUBLE,
                        `Swell2Direction` DOUBLE,
                        `Swell2SwellMinDirection` DOUBLE,
                        `Swell2Period` DOUBLE,
                        `Swell2OptimalScore` DOUBLE,
                        `Swell3Height` DOUBLE,
                        `Swell3Direction` DOUBLE,
                        `Swell3SwellMinDirection` DOUBLE,
                        `Swell3Period` DOUBLE,
                        `Swell3OptimalScore` DOUBLE,
                        `Swell4Height` DOUBLE,
                        `Swell4Direction` DOUBLE,
                        `Swell4SwellMinDirection` DOUBLE,
                        `Swell4Period` DOUBLE,
                        `Swell4OptimalScore` DOUBLE,
                        `Swell5Height` DOUBLE,
                        `Swell5Direction` DOUBLE,
                        `Swell5SwellMinDirection` DOUBLE,
                        `Swell5Period` DOUBLE,
                        `Swell5OptimalScore` DOUBLE,
                        `Swell6Height` DOUBLE,
                        `Swell6Direction` DOUBLE,
                        `Swell6SwellMinDirection` DOUBLE,
                        `Swell6Period` DOUBLE,
                        `Swell6OptimalScore` DOUBLE,
                        PRIMARY KEY (`SwellStagingKey`)) 
                        ENGINE = InnoDB;        
        """)

    def show_tables(self):
        cursor = self.connection.cursor()
        cursor.execute("SHOW Tables")
        return cursor.fetchall()

    def drop_table_if_exists(self):
        cursor = self.connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS `surfdb`.`SwellStaging`")
        self.connection.commit()

    def insert_csv_into_database(self, swell: Swell):
        data_path = os.path.join(definitions.ROOT_DIR, swell.swell_csv_dir)

        data = pd.read_csv(data_path, encoding='unicode_escape')
        df = pd.DataFrame(data)

        cursor = self.connection.cursor()

        for row in df.itertuples():
            gen_date = datetime.strptime(row.generation_date, '%m-%d-%Y').date()
            for_date = datetime.strptime(row.forecast_date, '%m-%d-%Y').date()

            ins_statement = """
                        INSERT INTO surfdb.SwellStaging 
                        (`ReportGenerationDate`, `GenerationHour`, `ReportForecastDate`, `ForecastHour`, `TideHeight`,
                        `SurfMin`, `SurfMax`, `SurfOptimalScore`, `WindDirection`, `WindSpeed`, `WindGust`, `Temperature`, 
                        `Swell1Height`, `Swell1Direction`, `Swell1SwellMinDirection`, `Swell1Period`, `Swell1OptimalScore`,
                        `Swell2Height`, `Swell2Direction`, `Swell2SwellMinDirection`, `Swell2Period`, `Swell2OptimalScore`, 
                        `Swell3Height`, `Swell3Direction`, `Swell3SwellMinDirection`, `Swell3period`, `Swell3OptimalScore`, 
                        `Swell4Height`, `Swell4Direction`, `Swell4SwellMinDirection`, `Swell4Period`, `Swell4OptimalScore`, 
                        `Swell5Height`, `Swell5Direction`, `Swell5SwellMinDirection`, `Swell5Period`, `Swell5OptimalScore`,
                        `Swell6Height`, `Swell6Direction`, `Swell6SwellMinDirection`, `Swell6Period`, `Swell6OptimalScore`) 
                        
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,  %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,  %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,  %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,  %s,%s)
                        """
            values = (
                gen_date,
                row.generation_hour,
                for_date,
                row.forecast_hour,
                row.tide_height,
                row.surf_min,
                row.surf_max,
                row.surf_optimal_score,
                row.wind_direction,
                row.wind_speed,
                row.wind_gust,
                row.temperature,

                row.swell_1_height,
                row.swell_1_direction,
                row.swell_1_swell_min_direction,
                row.swell_1_period,
                row.swell_1_optimal_score,

                row.swell_2_height,
                row.swell_2_direction,
                row.swell_2_swell_min_direction,
                row.swell_2_period,
                row.swell_2_optimal_score,

                row.swell_3_height,
                row.swell_3_direction,
                row.swell_3_swell_min_direction,
                row.swell_3_period,
                row.swell_3_optimal_score,

                row.swell_4_height,
                row.swell_4_direction,
                row.swell_4_swell_min_direction,
                row.swell_4_period,
                row.swell_4_optimal_score,

                row.swell_5_height,
                row.swell_5_direction,
                row.swell_5_swell_min_direction,
                row.swell_5_period,
                row.swell_5_optimal_score,

                row.swell_6_height,
                row.swell_6_direction,
                row.swell_6_swell_min_direction,
                row.swell_6_period,
                row.swell_6_optimal_score
            )

            cursor.execute(ins_statement, values)
        self.connection.commit()
        print(df)

    def select_all_swell_staging(self) -> list:
        select_statement = "SELECT * FROM `surfdb`.`SwellStaging`"
        all_rows = self.execute_read_query(select_statement)
        return all_rows
