-- MySQL dump 10.13  Distrib 8.0.20, for macos10.15 (x86_64)
--
-- Host: localhost    Database: chatbot_test
-- ------------------------------------------------------
-- Server version	8.0.20

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
-- Table structure for table `answers`
--

DROP TABLE IF EXISTS `answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `answers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `answer` varchar(60) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `answer_category_id` int NOT NULL,
  `grade` int DEFAULT NULL,
  `emoji` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  PRIMARY KEY (`id`),
  KEY `category_id_idx` (`answer_category_id`),
  CONSTRAINT `answer_category_id` FOREIGN KEY (`answer_category_id`) REFERENCES `categories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answers`
--

LOCK TABLES `answers` WRITE;
/*!40000 ALTER TABLE `answers` DISABLE KEYS */;
INSERT INTO `answers` VALUES (1,'тревоги нет',1,0,'?'),(2,'легкая тревога',1,1,'?'),(3,'умеренная тревога',1,2,'?'),(4,'интенсивная тревога',1,3,'?'),(5,'никогда (0%)',2,0,'?'),(6,'иногда (1 - 33%)',2,1,'?'),(7,'часто (34 - 67%)',2,2,'?'),(8,'постоянно (68 - 100%)',2,3,'?'),(30,'всё отлично (0)',3,0,'?'),(31,'в порядке (1)',3,1,'?'),(32,'нормально (2)',3,2,'?'),(33,'бывало и лучше (3)',3,3,'?'),(34,'бывало и хуже (4)',3,4,'☁️'),(35,'плохо (5)',3,5,'  ?'),(36,'всё плохо (6)',3,6,'⛈'),(37,'Совсем не беспокоит',4,0,'?'),(38,'Слегка. Не слишком меня беспокоит',4,1,'?'),(39,'Умеренно. Это было неприятно, но я могу это перенести',4,2,'☹️'),(40,'Очень сильно. Я с трудом могу это переносить',4,3,'?');
/*!40000 ALTER TABLE `answers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-07  8:53:36
