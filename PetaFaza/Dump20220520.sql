-- MySQL dump 10.13  Distrib 8.0.27, for Win64 (x86_64)
--
-- Host: localhost    Database: vic_hub
-- ------------------------------------------------------
-- Server version	8.0.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (3,'admin'),(1,'basic'),(2,'moderator');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add category',6,'add_category'),(22,'Can change category',6,'change_category'),(23,'Can delete category',6,'delete_category'),(24,'Can view category',6,'view_category'),(25,'Can add user',7,'add_user'),(26,'Can change user',7,'change_user'),(27,'Can delete user',7,'delete_user'),(28,'Can view user',7,'view_user'),(29,'Can add request',8,'add_request'),(30,'Can change request',8,'change_request'),(31,'Can delete request',8,'delete_request'),(32,'Can view request',8,'view_request'),(33,'Can add joke',9,'add_joke'),(34,'Can change joke',9,'change_joke'),(35,'Can delete joke',9,'delete_joke'),(36,'Can view joke',9,'view_joke'),(37,'Can add grade',10,'add_grade'),(38,'Can change grade',10,'change_grade'),(39,'Can delete grade',10,'delete_grade'),(40,'Can view grade',10,'view_grade'),(41,'Can add comment',11,'add_comment'),(42,'Can change comment',11,'change_comment'),(43,'Can delete comment',11,'delete_comment'),(44,'Can view comment',11,'view_comment'),(45,'Can add belongs to',12,'add_belongsto'),(46,'Can change belongs to',12,'change_belongsto'),(47,'Can delete belongs to',12,'delete_belongsto'),(48,'Can view belongs to',12,'view_belongsto');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `belongs_to`
--

DROP TABLE IF EXISTS `belongs_to`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `belongs_to` (
  `id_joke` int NOT NULL,
  `id_category` int NOT NULL,
  PRIMARY KEY (`id_joke`),
  UNIQUE KEY `belongs_to_id_joke_id_category_631e8c5f_uniq` (`id_joke`,`id_category`),
  KEY `belongs_to_id_category_8da15163_fk_category_id_category` (`id_category`),
  CONSTRAINT `belongs_to_id_category_8da15163_fk_category_id_category` FOREIGN KEY (`id_category`) REFERENCES `category` (`id_category`),
  CONSTRAINT `belongs_to_id_joke_c04c6992_fk_joke_id_joke` FOREIGN KEY (`id_joke`) REFERENCES `joke` (`id_joke`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `belongs_to`
--

LOCK TABLES `belongs_to` WRITE;
/*!40000 ALTER TABLE `belongs_to` DISABLE KEYS */;
/*!40000 ALTER TABLE `belongs_to` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `id_category` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`id_category`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `id_comment` int NOT NULL AUTO_INCREMENT,
  `ordinal_number` int NOT NULL,
  `content` longtext NOT NULL,
  `status` varchar(1) NOT NULL,
  `date_posted` datetime(6) DEFAULT NULL,
  `id_joke` int NOT NULL,
  `id_user` int NOT NULL,
  PRIMARY KEY (`id_comment`),
  KEY `comment_id_joke_d14c08b5_fk_joke_id_joke` (`id_joke`),
  KEY `comment_id_user_8f8b46ac_fk_user_id_user` (`id_user`),
  CONSTRAINT `comment_id_joke_d14c08b5_fk_joke_id_joke` FOREIGN KEY (`id_joke`) REFERENCES `joke` (`id_joke`),
  CONSTRAINT `comment_id_user_8f8b46ac_fk_user_id_user` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_user_id_user` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_user_id_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id_user`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2022-05-20 18:18:55.105804','1','basic',1,'[{\"added\": {}}]',3,1),(2,'2022-05-20 18:19:03.820406','2','moderator',1,'[{\"added\": {}}]',3,1),(3,'2022-05-20 18:19:09.472918','3','admin',1,'[{\"added\": {}}]',3,1),(4,'2022-05-20 18:25:17.497954','1','admin',2,'[{\"changed\": {\"fields\": [\"Groups\", \"Subscribed\", \"Status\", \"Type\"]}}]',7,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(5,'sessions','session'),(12,'VicHubApp','belongsto'),(6,'VicHubApp','category'),(11,'VicHubApp','comment'),(10,'VicHubApp','grade'),(9,'VicHubApp','joke'),(8,'VicHubApp','request'),(7,'VicHubApp','user');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2022-05-20 18:02:57.625994'),(2,'contenttypes','0002_remove_content_type_name','2022-05-20 18:02:58.142878'),(3,'auth','0001_initial','2022-05-20 18:02:59.072419'),(4,'auth','0002_alter_permission_name_max_length','2022-05-20 18:02:59.368622'),(5,'auth','0003_alter_user_email_max_length','2022-05-20 18:02:59.387113'),(6,'auth','0004_alter_user_username_opts','2022-05-20 18:02:59.407595'),(7,'auth','0005_alter_user_last_login_null','2022-05-20 18:02:59.426599'),(8,'auth','0006_require_contenttypes_0002','2022-05-20 18:02:59.437512'),(9,'auth','0007_alter_validators_add_error_messages','2022-05-20 18:02:59.455528'),(10,'auth','0008_alter_user_username_max_length','2022-05-20 18:02:59.475551'),(11,'auth','0009_alter_user_last_name_max_length','2022-05-20 18:02:59.495112'),(12,'auth','0010_alter_group_name_max_length','2022-05-20 18:02:59.537670'),(13,'auth','0011_update_proxy_permissions','2022-05-20 18:02:59.556680'),(14,'auth','0012_alter_user_first_name_max_length','2022-05-20 18:02:59.575631'),(15,'VicHubApp','0001_initial','2022-05-20 18:03:03.814793'),(16,'admin','0001_initial','2022-05-20 18:03:04.497654'),(17,'admin','0002_logentry_remove_auto_add','2022-05-20 18:03:04.561918'),(18,'admin','0003_logentry_add_action_flag_choices','2022-05-20 18:03:04.617647'),(19,'sessions','0001_initial','2022-05-20 18:03:04.724402'),(20,'VicHubApp','0002_alter_user_date_of_birth_and_more','2022-05-20 18:12:50.174584'),(21,'VicHubApp','0003_alter_user_date_of_birth_and_more','2022-05-20 18:27:41.962588'),(22,'VicHubApp','0004_alter_user_date_of_birth_and_more','2022-05-20 18:27:58.877208');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('heew36o0jdcjm984ubjqmdl9irylr0pf','.eJxVjEEOwiAQRe_C2pBSphRcuu8ZyAwzStVAUtqV8e7apAvd_vfef6mI25rj1mSJM6uzMur0uxGmh5Qd8B3LrepUy7rMpHdFH7TpqbI8L4f7d5Cx5W-dht4LJO_ZjOLBJmfAGgIKg1AIlh30ZNkCE4rxjHhNRCSdsY5G36n3B-S1OFk:1ns78F:pOBh_CQApRtFnnBe_LW9cS1TsHrodVVdDo0Fb5zPQ1g','2022-06-03 18:13:47.527825');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grade`
--

DROP TABLE IF EXISTS `grade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grade` (
  `id_grade` int NOT NULL AUTO_INCREMENT,
  `grade` int NOT NULL,
  `id_joke` int NOT NULL,
  `id_user` int NOT NULL,
  PRIMARY KEY (`id_grade`),
  KEY `grade_id_joke_a47357b7_fk_joke_id_joke` (`id_joke`),
  KEY `grade_id_user_74ee880f_fk_user_id_user` (`id_user`),
  CONSTRAINT `grade_id_joke_a47357b7_fk_joke_id_joke` FOREIGN KEY (`id_joke`) REFERENCES `joke` (`id_joke`),
  CONSTRAINT `grade_id_user_74ee880f_fk_user_id_user` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grade`
--

LOCK TABLES `grade` WRITE;
/*!40000 ALTER TABLE `grade` DISABLE KEYS */;
/*!40000 ALTER TABLE `grade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `joke`
--

DROP TABLE IF EXISTS `joke`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `joke` (
  `id_joke` int NOT NULL AUTO_INCREMENT,
  `title` varchar(45) NOT NULL,
  `content` longtext NOT NULL,
  `status` varchar(1) NOT NULL,
  `date_posted` datetime(6) DEFAULT NULL,
  `id_user_created` int NOT NULL,
  `id_user_reviewed` int DEFAULT NULL,
  PRIMARY KEY (`id_joke`),
  KEY `joke_id_user_created_08e669c6_fk_user_id_user` (`id_user_created`),
  KEY `joke_id_user_reviewed_4395f2f4_fk_user_id_user` (`id_user_reviewed`),
  CONSTRAINT `joke_id_user_created_08e669c6_fk_user_id_user` FOREIGN KEY (`id_user_created`) REFERENCES `user` (`id_user`),
  CONSTRAINT `joke_id_user_reviewed_4395f2f4_fk_user_id_user` FOREIGN KEY (`id_user_reviewed`) REFERENCES `user` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `joke`
--

LOCK TABLES `joke` WRITE;
/*!40000 ALTER TABLE `joke` DISABLE KEYS */;
/*!40000 ALTER TABLE `joke` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `request`
--

DROP TABLE IF EXISTS `request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `request` (
  `id_request` int NOT NULL AUTO_INCREMENT,
  `status` varchar(1) NOT NULL,
  `id_user` int NOT NULL,
  `id_user_reviewed` int DEFAULT NULL,
  PRIMARY KEY (`id_request`),
  KEY `request_id_user_28b90120_fk_user_id_user` (`id_user`),
  KEY `request_id_user_reviewed_8b8729ee_fk_user_id_user` (`id_user_reviewed`),
  CONSTRAINT `request_id_user_28b90120_fk_user_id_user` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`),
  CONSTRAINT `request_id_user_reviewed_8b8729ee_fk_user_id_user` FOREIGN KEY (`id_user_reviewed`) REFERENCES `user` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `request`
--

LOCK TABLES `request` WRITE;
/*!40000 ALTER TABLE `request` DISABLE KEYS */;
/*!40000 ALTER TABLE `request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `id_user` int NOT NULL AUTO_INCREMENT,
  `date_of_birth` date NOT NULL,
  `subscribed` varchar(1) NOT NULL,
  `status` varchar(1) NOT NULL,
  `type` varchar(1) NOT NULL,
  `date_of_promotion` datetime(6) NOT NULL,
  PRIMARY KEY (`id_user`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('pbkdf2_sha256$320000$39HOCsLur89grIJb7tiC3L$js09m3zojWdTamjUOaYzuGFqiGEL99FxR6c5eadTR0M=','2022-05-20 18:13:47.000000',1,'admin','','','',1,1,'2022-05-20 18:13:11.000000',1,'2022-05-20','N','A','A','2022-05-20 20:12:54.000000');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_groups`
--

DROP TABLE IF EXISTS `user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_groups_user_id_group_id_40beef00_uniq` (`user_id`,`group_id`),
  KEY `user_groups_group_id_b76f8aba_fk_auth_group_id` (`group_id`),
  CONSTRAINT `user_groups_group_id_b76f8aba_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_groups_user_id_abaea130_fk_user_id_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id_user`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_groups`
--

LOCK TABLES `user_groups` WRITE;
/*!40000 ALTER TABLE `user_groups` DISABLE KEYS */;
INSERT INTO `user_groups` VALUES (1,1,3);
/*!40000 ALTER TABLE `user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_user_permissions`
--

DROP TABLE IF EXISTS `user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_user_permissions_user_id_permission_id_7dc6e2e0_uniq` (`user_id`,`permission_id`),
  KEY `user_user_permission_permission_id_9deb68a3_fk_auth_perm` (`permission_id`),
  CONSTRAINT `user_user_permission_permission_id_9deb68a3_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_user_permissions_user_id_ed4a47ea_fk_user_id_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_user_permissions`
--

LOCK TABLES `user_user_permissions` WRITE;
/*!40000 ALTER TABLE `user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-05-20 20:30:59
