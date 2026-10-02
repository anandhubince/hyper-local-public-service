/*
SQLyog Community v13.1.6 (64 bit)
MySQL - 5.7.9 : Database - python_public_service
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`python_public_service` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `python_public_service`;

/*Table structure for table `agent` */

DROP TABLE IF EXISTS `agent`;

CREATE TABLE `agent` (
  `agent_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `fname` varchar(100) DEFAULT NULL,
  `lname` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`agent_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `agent` */

insert  into `agent`(`agent_id`,`login_id`,`fname`,`lname`,`place`,`phone`,`email`) values 
(3,6,'Madrubhoomi','qwerty','kerala','2345678907','student@gmail.com'),
(4,8,'manorama','antony','thrissur','4567892345','lijo@gmail.com');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `usertype` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`usertype`) values 
(5,'hai','hai','user'),
(6,'agent','agent','agent'),
(7,'uu','uu','user'),
(8,'u','u','agent');

/*Table structure for table `news` */

DROP TABLE IF EXISTS `news`;

CREATE TABLE `news` (
  `news_id` int(11) NOT NULL AUTO_INCREMENT,
  `agent_id` int(11) DEFAULT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `details` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `date` varchar(100) DEFAULT NULL,
  `category` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'General',
  PRIMARY KEY (`news_id`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

/*Data for the table `news` */

insert  into `news`(`news_id`,`agent_id`,`title`,`details`,`date`,`category`) values 
(2,3,'Toxic gas putting millions at risk in Middle East, BBC finds','fcri','2023-11-23','General'),
(3,3,'Tunnel rescue: ‘Rat-hole’ miners begin operation to reach 41','fff','2023-11-23','General'),
(10,4,'Rohit Sharma: The Indian captain who lost cricket World Cup but won hearts','wdw','2023-11-28','General'),
(11,3,'എല്ലാ തിങ്കളാഴ്ചയും ഹാജരാകണം; ബലാത്സംഗ കേസിൽ രാഹുൽ മാങ്കൂട്ടത്തിലിന് ഉപാധികളോടെ മുൻകൂർ ജാമ്യം','തിരുവനന്തപുരം: സ്ത്രീപീഡനക്കേസില്‍ പാലക്കാട് എംഎല്‍എ രാഹുല്‍ മാങ്കൂട്ടത്തിലിന് മുന്‍കൂര്‍ ജാമ്യം. ലൈംഗിക പീഡന ആരോപണത്തില്‍ രണ്ടാമത് രജിസ്റ്റര്‍ ','2025-12-10','General'),
(12,3,'Parliament Winter Session 2025: Live Updates Day 8 – Electoral Reforms Debate Resumes in Lok Sabha','Day 8 of the Winter Session of Parliament 2025 is underway, with the Lok Sabha continuing its debate on Electoral Reforms, and the discussion on \'Vande Mataram\' is ongoing in Rajya Sabha.','2025-12-10','General'),
(14,3,'ജമാഅത്തെ ഇസ്‌ലാമി സ്ഥാനാർഥികളെ പ്രഖ്യാപിക്കുന്നത് പാണക്കാട്ട്; സംഘിക്കുപ്പായം സിപിഎമ്മിനു വേണ്ട: മുഖ','യുഡിഎഫിന്റെ കൂടെയുള്ളവർ വൻ തോതിൽ കൊഴിഞ്ഞുപോകുകയാണെന്നു പിണറായി വിജയൻ പറഞ്ഞു. പുതിയ ഏതെങ്കിലും ശക്തിയ','2025-12-10','Politics'),
(15,3,'FIFA President Gianni Infantino accused of ethics breach: Report','A worldwide advocacy group has filed a complaint with FIFA’s Ethics Committee, citing a lack of impartiality from organisation President Gianni Infantino, as well as the political nature of last week’s 2026 World Cup draw, The Athletic reported on Tuesday (December 9, 2025).\r\n\r\n','2025-12-10','Sports');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `fname` varchar(100) DEFAULT NULL,
  `lname` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`user_id`,`login_id`,`fname`,`lname`,`place`,`phone`,`email`) values 
(3,5,'user','qwerty','kerala','2345678907','student@gmail.com'),
(4,7,'liya','antony','thrissur','3456789023','liya@gmail.coom');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
