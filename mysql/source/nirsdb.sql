/*
SQLyog Community v13.1.6 (64 bit)
MySQL - 5.7.31 : Database - nirsdb
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
/*Table structure for table `alembic_version` */

DROP TABLE IF EXISTS `alembic_version`;

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `alembic_version` */

LOCK TABLES `alembic_version` WRITE;

insert  into `alembic_version`(`version_num`) values 
('3f36554f5829');

UNLOCK TABLES;

/*Table structure for table `system_role` */

DROP TABLE IF EXISTS `system_role`;

CREATE TABLE `system_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `desc` varchar(200) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `permissions` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `system_role` */

LOCK TABLES `system_role` WRITE;

UNLOCK TABLES;

/*Table structure for table `system_role_user` */

DROP TABLE IF EXISTS `system_role_user`;

CREATE TABLE `system_role_user` (
  `system_role_id` int(11) NOT NULL,
  `system_user_id` int(11) NOT NULL,
  PRIMARY KEY (`system_role_id`,`system_user_id`),
  KEY `system_user_id` (`system_user_id`),
  CONSTRAINT `system_role_user_ibfk_1` FOREIGN KEY (`system_role_id`) REFERENCES `system_role` (`id`),
  CONSTRAINT `system_role_user_ibfk_2` FOREIGN KEY (`system_user_id`) REFERENCES `system_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `system_role_user` */

LOCK TABLES `system_role_user` WRITE;

UNLOCK TABLES;

/*Table structure for table `system_user` */

DROP TABLE IF EXISTS `system_user`;

CREATE TABLE `system_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `_password` varchar(256) DEFAULT NULL,
  `email` varchar(50) NOT NULL,
  `join_time` datetime DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `last_login_time` datetime DEFAULT NULL,
  `realname` varchar(20) DEFAULT NULL,
  `gender` int(11) DEFAULT NULL,
  `contact` varchar(15) DEFAULT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `signature` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Data for the table `system_user` */

LOCK TABLES `system_user` WRITE;

insert  into `system_user`(`id`,`username`,`_password`,`email`,`join_time`,`is_active`,`last_login_time`,`realname`,`gender`,`contact`,`avatar`,`signature`) values 
(1,'midi','pbkdf2:sha256:260000$Rzt0nZ2QD3uCffZI$7dc3581d4b943a50242d3e9a7c60a46dec4705d303aea093698f4922b358f4a4','admin@qq.com','2021-10-04 15:17:36',1,'2021-10-04 15:22:02',NULL,4,NULL,NULL,NULL);

UNLOCK TABLES;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
