import definitions
from src.Swell import Swell
from src.DAO import DAO
import pandas as pd
import os


class SwellDAO(DAO):

    def __init__(self):
        DAO.__init__(self)

    def insert_csv_into_database(self, swell: Swell):
        print(os.getcwd())
        data_path = os.path.join(definitions.ROOT_DIR, swell.swell_csv_dir)

        data = pd.read_csv(data_path, encoding= 'unicode_escape')
        df = pd.DataFrame(data)

        cursor = self.connection.cursor()

        for row in df.itertuples():
            cursor.execute('''
                        INSERT INTO `surfdb`.`SwellStaging` 
                        (`ReportGenerationDate`, `GenerationHour`, `ReportForecastDate`, `ForecastHour`, `TideHeight`,
                        `SurfMin`, `SurfMax`, `SurfOptimalScore`, `WindDirection`, `WindSpeed`, `WindGust`, `Temperature`, 
                        `Swell1Height`, `Swell1Direction`, `Swell1SwellMinDirection`, `Swell1Period`, `Swell1OptimalScore`,
                        `Swell2Height`, `Swell2Direction`, `Swell2SwellMinDirection`,, `Swell2Period`, `Swell2OptimalScore`, 
                        `Swell3Height`, `Swell3Direction`, `Swell3SwellMinDirection`,, `Swell3period`, `Swell3OptimalScore`, 
                        `Swell4Height`, `Swell4Direction`, `Swell4SwellMinDirection`,, `Swell4Period`, `Swell4OptimalScore`, 
                        `Swell5Height`, `Swell5Direction`, `Swell5SwellMinDirection`,, `Swell5Period`, `Swell5OptimalScore`,
                        `Swell6Height`, `Swell6Direction`, `Swell6SwellMinDirection`,, `Swell6Period`, `Swell6OptimalScore`)
                        VALUES (?,?,?,?,?,?,?,?,?,?,  ?,?,?,?,?,?,?,?,?,?,  ?,?,?,?,?,?,?,?,?,?,  ?,?,?,?,?,?,?,?,?,?,  ?,?)
                        ''',
                           row.generation_date,
                           row.generation_hour,
                           row.forecast_date,
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
                           row.swell_6_optimal_score,

                           )
        self.connection.commit()

        print(df)





    def select_all_swell_staging(self):
        select_statement = "SELECT * FROM `surfdb`.`SwellStaging`"
        all_rows = self.execute_read_query(select_statement)

        for row in all_rows:
            print(row)
