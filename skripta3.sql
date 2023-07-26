-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema videoteka
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema videoteka
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `videoteka` DEFAULT CHARACTER SET utf8 ;
USE `videoteka` ;

-- -----------------------------------------------------
-- Table `videoteka`.`Movie`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `videoteka`.`Movie` (
  `IdMovie` INT NOT NULL AUTO_INCREMENT,
  `MovieName` VARCHAR(100) NOT NULL,
  `year` VARCHAR(10) NOT NULL,
  `image` VARCHAR(1000) NOT NULL,
  `language` VARCHAR(1000) NOT NULL,
  `imdb` DECIMAL(4,2) NOT NULL,
  `category` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`IdMovie`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `videoteka`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `videoteka`.`User` (
  `IdUser` INT NOT NULL AUTO_INCREMENT,
  `firstname` VARCHAR(45) NOT NULL,
  `lastname` VARCHAR(45) NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(500) NOT NULL,
  `gender` VARCHAR(11) NOT NULL,
  `active` TINYINT(1) NULL,
  PRIMARY KEY (`IdUser`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `videoteka`.`Reviews`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `videoteka`.`Reviews` (
  `IdReview` INT NOT NULL AUTO_INCREMENT,
  `TimeReview` VARCHAR(45) NOT NULL,
  `ContentReview` VARCHAR(150) NULL,
  `User_IdUser` INT NOT NULL,
  `Movie_IdMovie` INT NOT NULL,
  PRIMARY KEY (`IdReview`, `User_IdUser`, `Movie_IdMovie`),
  INDEX `fk_Reviews_User1_idx` (`User_IdUser` ASC) VISIBLE,
  INDEX `fk_Reviews_Movie1_idx` (`Movie_IdMovie` ASC) VISIBLE,
  CONSTRAINT `fk_Reviews_User1`
    FOREIGN KEY (`User_IdUser`)
    REFERENCES `videoteka`.`User` (`IdUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Reviews_Movie1`
    FOREIGN KEY (`Movie_IdMovie`)
    REFERENCES `videoteka`.`Movie` (`IdMovie`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `videoteka`.`Rates`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `videoteka`.`Rates` (
  `IdRate` INT NOT NULL AUTO_INCREMENT,
  `Rate` DECIMAL NULL,
  `User_IdUser` INT NOT NULL,
  `Movie_IdMovie` INT NOT NULL,
  PRIMARY KEY (`IdRate`, `User_IdUser`, `Movie_IdMovie`),
  INDEX `fk_Rates_User_idx` (`User_IdUser` ASC) VISIBLE,
  INDEX `fk_Rates_Movie1_idx` (`Movie_IdMovie` ASC) VISIBLE,
  CONSTRAINT `fk_Rates_User`
    FOREIGN KEY (`User_IdUser`)
    REFERENCES `videoteka`.`User` (`IdUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Rates_Movie1`
    FOREIGN KEY (`Movie_IdMovie`)
    REFERENCES `videoteka`.`Movie` (`IdMovie`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `videoteka`.`MovieCategory`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `videoteka`.`MovieCategory` (
  `IdCategoryMovie` INT NOT NULL AUTO_INCREMENT,
  `CategoryMovie` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`IdCategoryMovie`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `videoteka`.`Movie_has_MovieCategory`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `videoteka`.`Movie_has_MovieCategory` (
  `Movie_IdMovie` INT NOT NULL,
  `MovieCategory_IdCategoryMovie` INT NOT NULL,
  PRIMARY KEY (`Movie_IdMovie`, `MovieCategory_IdCategoryMovie`),
  INDEX `fk_Movie_has_MovieCategory_MovieCategory1_idx` (`MovieCategory_IdCategoryMovie` ASC) VISIBLE,
  INDEX `fk_Movie_has_MovieCategory_Movie1_idx` (`Movie_IdMovie` ASC) VISIBLE,
  CONSTRAINT `fk_Movie_has_MovieCategory_Movie1`
    FOREIGN KEY (`Movie_IdMovie`)
    REFERENCES `videoteka`.`Movie` (`IdMovie`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Movie_has_MovieCategory_MovieCategory1`
    FOREIGN KEY (`MovieCategory_IdCategoryMovie`)
    REFERENCES `videoteka`.`MovieCategory` (`IdCategoryMovie`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
