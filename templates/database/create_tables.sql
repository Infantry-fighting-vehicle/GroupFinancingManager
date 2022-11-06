-- Active: 1666011951204@@127.0.0.1@3306@groupfinancingmanager

CREATE DATABASE GroupFinancingManager DEFAULT CHARACTER SET = 'utf8mb4';
USE `GroupFinancingManager` ;
CREATE TABLE IF NOT EXISTS `GroupFinancingManager`.`users` (
  `user_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `card_number` VARCHAR(45) NOT NULL,
  `phone` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `GroupFinancingManager`.`groups_` (
  `group_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `owner_id` INT UNSIGNED NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`group_id`),
  INDEX `fk_groups__users_idx` (`owner_id` ASC) VISIBLE,
  CONSTRAINT `fk_groups__users`
    FOREIGN KEY (`owner_id`)
    REFERENCES `GroupFinancingManager`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `GroupFinancingManager`.`memberships` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` INT UNSIGNED NOT NULL,
  `group_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_memberships_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_memberships_groups_1_idx` (`group_id` ASC) VISIBLE,
  CONSTRAINT `fk_memberships_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `GroupFinancingManager`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_memberships_groups_1`
    FOREIGN KEY (`group_id`)
    REFERENCES `GroupFinancingManager`.`groups_` (`group_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `GroupFinancingManager`.`purchases` (
  `purchase_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `group_id` INT UNSIGNED NOT NULL,
  `owner_id` INT UNSIGNED NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `cost` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`purchase_id`),
  INDEX `fk_purchases_groups_1_idx` (`group_id` ASC) VISIBLE,
  INDEX `fk_purchases_users1_idx` (`owner_id` ASC) VISIBLE,
  CONSTRAINT `fk_purchases_groups_1`
    FOREIGN KEY (`group_id`)
    REFERENCES `GroupFinancingManager`.`groups_` (`group_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_purchases_users1`
    FOREIGN KEY (`owner_id`)
    REFERENCES `GroupFinancingManager`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `GroupFinancingManager`.`typesOfTransfer` (
  `type_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`type_id`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `GroupFinancingManager`.`transfers` (
  `transfer_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `amount` FLOAT NOT NULL,
  `user_id` INT UNSIGNED NOT NULL,
  `type_id` INT UNSIGNED NOT NULL,
  `purchase_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`transfer_id`),
  INDEX `fk_transfers_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_transfers_purchases1_idx` (`purchase_id` ASC) VISIBLE,
  INDEX `fk_transfers_typesOfTransfer1_idx` (`type_id` ASC) VISIBLE,
  CONSTRAINT `fk_transfers_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `GroupFinancingManager`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_transfers_purchases1`
    FOREIGN KEY (`purchase_id`)
    REFERENCES `GroupFinancingManager`.`purchases` (`purchase_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_transfers_typesOfTransfer1`
    FOREIGN KEY (`type_id`)
    REFERENCES `GroupFinancingManager`.`typesOfTransfer` (`type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;