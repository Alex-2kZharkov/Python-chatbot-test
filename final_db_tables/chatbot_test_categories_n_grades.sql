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
-- Table structure for table `categories_n_grades`
--

DROP TABLE IF EXISTS `categories_n_grades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories_n_grades` (
  `id` int NOT NULL AUTO_INCREMENT,
  `categories_grades_id` int NOT NULL,
  `grades_id` int NOT NULL,
  `recomendation_text` varchar(450) DEFAULT NULL,
  `gif` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `categories_grades_id_idx` (`categories_grades_id`),
  KEY `grades_id_idx` (`grades_id`),
  CONSTRAINT `categories_grades_id` FOREIGN KEY (`categories_grades_id`) REFERENCES `categories` (`id`),
  CONSTRAINT `grades_id` FOREIGN KEY (`grades_id`) REFERENCES `grades_scope` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories_n_grades`
--

LOCK TABLES `categories_n_grades` WRITE;
/*!40000 ALTER TABLE `categories_n_grades` DISABLE KEYS */;
INSERT INTO `categories_n_grades` VALUES (1,1,1,'отсутствует социофобия. Поздравлем!','https://media.tumblr.com/tumblr_loxahbLJ3k1qk8rvb.gif'),(2,1,2,'присутсвует cлабовыраженная социофобия. Учитесь искусству спокойно дышать, которое ему следует применять при наступлении тревоги, что, несомненно, поможет вам сохранять спокойствие. Если этот метод практикуется регулярно, он способен творить чудеса.','https://blog.zenduty.com/assets/images/meditate.gif'),(3,1,3,'достаточно выраженная социофобия.  Учитесь искусству спокойно дышать, которое ему следует применять при наступлении тревоги, что, несомненно, поможет вам сохранять спокойствие. Если этот метод практикуется регулярно, он способен творить чудеса. И по возможности обратитесь к специалисту.','https://media3.giphy.com/media/F7kdOcOdh07Ru/giphy.gif'),(4,1,4,'сильная социофобия. Игнорировать и/или заниматься самолечением в таком случае невыход. Это может сильно отразиться на вашей жизни. Обратитесь к специалисту.','https://media1.tenor.com/images/81e17777ad8145d41f5c8f38ddbeb59d/tenor.gif?itemid=12028473'),(5,1,5,'очень сильная социофобия.  Немедленно обратитесь к специалисту.','https://media2.giphy.com/media/A9MftKr3J3lra/giphy.gif'),(6,3,6,'нет депрессии. Поздравляем!','https://media0.giphy.com/media/YnBntKOgnUSBkV7bQH/giphy.gif'),(7,3,7,'малый депрессивный эпизод. В целом ничего критичного, но стоит больше заниматься спортом, творчеством и не держать эмоции в себе. ','https://i.pinimg.com/originals/24/ec/dc/24ecdc5a536b9c7af956deb33a31764d.gif'),(8,3,8,'умеренный депрессивный эпизод. Тут без помощи врача не обойтись. Как только появится время, сразу найдите хорошего специалиста в вашем городе и запишитесь на приём','https://media3.giphy.com/media/htkLDMetC4PGxkKUpg/giphy-downsized.gif'),(9,3,9,'большой депрессивный эпизод. Немедленно обратитесь к врачу.','https://i.pinimg.com/originals/eb/9d/54/eb9d542c9e70e79bf5c45353b79eb434.gif'),(10,2,1,'отсутствует социофобия. Поздравлем!','https://thumbs.gfycat.com/UnevenAbsoluteIaerismetalmark-max-1mb.gif'),(11,2,2,'присутсвует cлабовыраженная социофобия. Учитесь искусству спокойно дышать, которое ему следует применять при наступлении тревоги, что, несомненно, поможет вам сохранять спокойствие. Если этот метод практикуется регулярно, он способен творить чудеса.','https://biteable.com/content/uploads/2017/09/videogif4.gif'),(12,2,3,'достаточно выраженная социофобия.  Учитесь искусству спокойно дышать, которое ему следует применять при наступлении тревоги, что, несомненно, поможет вам сохранять спокойствие. Если этот метод практикуется регулярно, он способен творить чудеса. И по возможности обратитесь к специалисту.','https://i.pinimg.com/originals/ad/13/55/ad1355924d00911106e56c1c2688f7b1.gif'),(13,2,4,'сильная социофобия. Игнорировать и/или заниматься самолечением в таком случае невыход. Это может сильно отразиться на вашей жизни. Обратитесь к специалисту.','https://media4.giphy.com/media/yR09GN4EqSnC0/200.gif'),(14,2,5,'очень сильная социофобия.  Немедленно обратитесь к специалисту.','https://media2.giphy.com/media/A9MftKr3J3lra/giphy.gifэ'),(15,4,10,'низкая тревожность. Отличная вещь! (если вы были реалистичны в своей оценке) В тоже время, слишком низкая тревога может указывать на то, что вы оторваны от себя, других или своего окружения.','https://media3.giphy.com/media/26xBv1FLG6b3BznRS/giphy.gif'),(16,4,11,'средняя выраженность тревоги. Возможно, ваше тело пытается вам что-то сказать. Ищите паттерны — когда и почему вы испытываете симптомы, описанные выше. Например, если это происходит перед публичным выступлением (и ваша работа часто этого требует) вы можете найти способы успокоиться перед тем, как выступить. (или иногда позволять делать это другим)','https://giffiles.alphacoders.com/369/3692.gif'),(17,4,12,'очень высокая тревога.Это потенциальная причина для беспокойства.Стоит задуматься — в каких обстоятельствах, как и когда проявляются эти симптомы. Однако такой высокий уровень тревоги требует не только вашего внимания, такое состояние стоит проактивно лечить.(Иначе это может иметь значительные последствия для вас, и  умственно и физически.) Если накал чувств сохраняется, стоит обратиться к врачу или психологу.','https://thumbs.gfycat.com/ConcreteAccurateAustralianfurseal-size_restricted.gif');
/*!40000 ALTER TABLE `categories_n_grades` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-07  8:53:34
