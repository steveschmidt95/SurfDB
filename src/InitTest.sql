DROP SCHEMA IF EXISTS `surfdb`;
CREATE SCHEMA IF NOT EXISTS `surfdb`;
USE `surfdb`;

DROP TABLE IF EXISTS `surfdb`.`ReportDataPoint`;
DROP TABLE IF EXISTS `surfdb`.`ReportWeather`;
DROP TABLE IF EXISTS `surfdb`.`ReportImages`;

CREATE TABLE IF NOT EXISTS `surfdb`.`ReportWeather` (
    `ReportWeatherKey` BIGINT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (`ReportWeatherKey`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `surfdb`.`ReportImages` (
    `ReportImagesKey` BIGINT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (`ReportImagesKey`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `surfdb`.`ReportDataPoint` (
    `ReportDataPointKey` BIGINT NOT NULL AUTO_INCREMENT,
    `ReportDate` DATE NOT NULL,
    `ReportImagesFK` BIGINT NULL,
	`ReportWeatherFK` BIGINT NULL,
    PRIMARY KEY (`ReportDataPointKey`),
    INDEX `fk_report_images_idx` (`ReportImagesFK` ASC) VISIBLE,
	INDEX `fk_report_weather_idx` (`ReportWeatherFK` ASC) VISIBLE,
	CONSTRAINT `fk_report_images_idx`
	  FOREIGN KEY (`ReportImagesFK`)
      REFERENCES `mydb`.`ReportImages` (`ReportImagesKey`)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
	CONSTRAINT `fk_report_weather_idx`
	  FOREIGN KEY (`ReportWeatherFK`)
	  REFERENCES `mydb`.`ReportWeather` (`ReportWeatherKey`)
	  ON DELETE NO ACTION
	  ON UPDATE NO ACTION)
ENGINE = InnoDB;

