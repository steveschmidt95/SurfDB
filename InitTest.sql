DROP SCHEMA IF EXISTS `surfdb`;
CREATE SCHEMA IF NOT EXISTS `surfdb`;
USE `surfdb`;

DROP TABLE IF EXISTS `surfdb`.`ReportDataPoint`;

CREATE TABLE ReportDataPoint (
    PersonID int,
    LastName varchar(255),
    FirstName varchar(255),
    Address varchar(255),
    City varchar(255)
);

