#DROP SCHEMA IF EXISTS `surfdb`;
CREATE SCHEMA IF NOT EXISTS `surfdb`;
USE `surfdb`;
SHOW VARIABLES LIKE "secure_file_priv";

DROP TABLE IF EXISTS `surfdb`.`ReportDataPoint`;
DROP TABLE IF EXISTS `surfdb`.`ReportWeather`;
DROP TABLE IF EXISTS `surfdb`.`ReportImages`;
DROP TABLE IF EXISTS `surfdb`,`SwellStaging`;

CREATE TABLE IF NOT EXISTS `surfdb`.`ReportWeather` (
    `ReportWeatherKey` BIGINT NOT NULL AUTO_INCREMENT,
    `ReportGenerationDate` DATE,
    `TimeBlockHourStart` INT,
	`ReportForecastDate` DATE,
    PRIMARY KEY (`ReportWeatherKey`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `surfdb`.`ReportImages` (
    `ReportImagesKey` BIGINT NOT NULL AUTO_INCREMENT,
	`ReportForecastDate` DATE,
    `TimeBlockHourStart` INT,
    `TimeBlockDirectory` TEXT(200),
    PRIMARY KEY (`ReportImagesKey`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `surfdb`.`ReportDataPoint` (
    `ReportDataPointKey` BIGINT NOT NULL AUTO_INCREMENT,
    `ReportGenerationDate` DATE,
    `TimeBlockHourStart` INT, 
	`ReportForecastDate` DATE,
    `ReportImagesFK` BIGINT NULL,
	`ReportWeatherFK` BIGINT NULL,
    PRIMARY KEY (`ReportDataPointKey`),
    INDEX `fk_report_images_idx` (`ReportImagesFK` ASC) VISIBLE,
	INDEX `fk_report_weather_idx` (`ReportWeatherFK` ASC) VISIBLE,
	CONSTRAINT `fk_report_images_idx`
	  FOREIGN KEY (`ReportImagesFK`)
      REFERENCES `surfdb`.`ReportImages` (`ReportImagesKey`)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
	CONSTRAINT `fk_report_weather_idx`
	  FOREIGN KEY (`ReportWeatherFK`)
	  REFERENCES `surfdb`.`ReportWeather` (`ReportWeatherKey`)
	  ON DELETE NO ACTION
	  ON UPDATE NO ACTION)
ENGINE = InnoDB;

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


-- -----------------------------------------------------
-- Load data into `surfdb`.`SwellStaging`
-- -----------------------------------------------------
#LOAD DATA INFILE 'testWaveDataShort.csv' INTO TABLE `surfdb`.`SwellStaging` 
#	FIELDS TERMINATED BY ',' 
#	OPTIONALLY ENCLOSED BY '"' 
#	LINES TERMINATED BY '\r\n' 
#	IGNORE 1 LINES;
    

    

INSERT INTO `surfdb`.`ReportImages`
(`ReportImagesKey`, `TimeBlockHourStart`, `TimeBlockDirectory`)
VALUES (5, 5, "/Users/stephenschmidt/Desktop/Steve/SurfDB/testdata/05031995/00-03");

SHOW COLUMNS FROM `surfdb`.`SwellStaging`;

INSERT INTO `surfdb`.`SwellStaging`(`GenerationHour`) VALUES(3);
SELECT * FROM `surfdb`.`SwellStaging`

#INSERT INTO `surfdb`.`SwellStaging`(`GenerationHour`) VALUES(3);


