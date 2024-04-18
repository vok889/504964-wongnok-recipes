CREATE DATABASE IF NOT EXISTS `Wongrok` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `Wongrok`;

CREATE TABLE IF NOT EXISTS `accounts` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`username` varchar(50) NOT NULL,
`password` varchar(255) NOT NULL,
`email` varchar(100) NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `recipe` (
`recipe_id` int(11) NOT NULL AUTO_INCREMENT,
`id` int(11) NOT NULL,
`recipe_name` varchar(255) NOT NULL,
`recipe_category` int(2) NOT NULL,
`recipe_picture` varchar(50) NOT NULL,
`recipe_serving` int(4) NOT NULL,
`recipe_time` int(2) NOT NULL,
`recipe_level` int(2) NOT NULL,
`recipe_ingredient` varchar(1200) NOT NULL,
`recipe_step` varchar(1200) NOT NULL,
PRIMARY KEY (`recipe_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `ingredients` (
`ingredient_id` int(11) NOT NULL AUTO_INCREMENT,
`recipe_id` int(11) NOT NULL,
`ingredient_detail` varchar(255) NOT NULL,
PRIMARY KEY (`ingredient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `procedures` (
`procedure_id` int(11) NOT NULL AUTO_INCREMENT,
`recipe_id` int(11) NOT NULL,
`step` varchar(255) NOT NULL,
PRIMARY KEY (`procedure_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `review` (
`review_id` int(11) NOT NULL AUTO_INCREMENT,
`recipe_id` int(11) NOT NULL,
`id` int(11) NOT NULL,
`score` int(2) NOT NULL,
`comments` varchar(255) NOT NULL,
PRIMARY KEY (`review_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `recipe` (
`recipe_id` int(11) NOT NULL AUTO_INCREMENT,
`id` int(11) NOT NULL,
`recipe_name` varchar(255) NOT NULL,
`recipe_category` int(2) NOT NULL,
`recipe_picture` varchar(50) NOT NULL,
`recipe_serving` int(4) NOT NULL,
`recipe_time` int(2) NOT NULL,
`recipe_level` int(2) NOT NULL,
`recipe_ingredient` varchar(1200) NOT NULL,
`recipe_step` varchar(1200) NOT NULL,
PRIMARY KEY (`recipe_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;





