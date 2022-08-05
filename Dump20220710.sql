-- MySQL dump 10.13  Distrib 8.0.29, for macos12 (x86_64)
--
-- Host: localhost    Database: analyst_connections
-- ------------------------------------------------------
-- Server version	8.0.29

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
-- Table structure for table `Analysts`
--

DROP TABLE IF EXISTS `Analysts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Analysts` (
  `ANALYST_ID` int NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) NOT NULL,
  `FUND` int DEFAULT NULL,
  `LN_ID` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ANALYST_ID`),
  KEY `FUNDS_FK1_idx` (`FUND`),
  CONSTRAINT `FUNDS_FK1` FOREIGN KEY (`FUND`) REFERENCES `Funds` (`FUND_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Analysts`
--

LOCK TABLES `Analysts` WRITE;
/*!40000 ALTER TABLE `Analysts` DISABLE KEYS */;
INSERT INTO `Analysts` VALUES (6,'Adil Abdul Halim',7,'%5B%22ACoAAB_BeDMBLu2J3i3ETrZ00k4-SPoD5ILBg7w%22%5D&network=%5B%22F%22%2C%22S%22%5D'),(7,'Badai Tanmizi',9,'%5B\"ACoAABzLFbkBXmi0BGHeFjokuCSCoClr21hw1SE\"%5D'),(8,'Adriel Yong',10,'%5B\"ACoAAB5jmpYBtZ2I6myyxfj-Q2UCcPArUjaqEY0\"%5D&');
/*!40000 ALTER TABLE `Analysts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CONNECTEES`
--

DROP TABLE IF EXISTS `CONNECTEES`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CONNECTEES` (
  `CONNECTEE_ID` int NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) NOT NULL,
  `COMPANY` varchar(100) NOT NULL,
  `COUNTRY` varchar(100) NOT NULL,
  `CONNECTED_DATE` date NOT NULL,
  `CONNECTED_TO` int DEFAULT NULL,
  PRIMARY KEY (`CONNECTEE_ID`),
  KEY `CONNECTED_TO_FK1_idx` (`CONNECTED_TO`),
  CONSTRAINT `CONNECTED_TO_FK1` FOREIGN KEY (`CONNECTED_TO`) REFERENCES `Analysts` (`ANALYST_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CONNECTEES`
--

LOCK TABLES `CONNECTEES` WRITE;
/*!40000 ALTER TABLE `CONNECTEES` DISABLE KEYS */;
INSERT INTO `CONNECTEES` VALUES (10,'Roger','Telamundo','Singapore','2021-12-12',6),(11,'Christopher','Vikings','Singapore','2021-12-12',6),(12,'Phyllis Chua','TikTok','Singapore','2021-12-12',6);
/*!40000 ALTER TABLE `CONNECTEES` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Funds`
--

DROP TABLE IF EXISTS `Funds`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Funds` (
  `FUND_ID` int NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`FUND_ID`),
  UNIQUE KEY `NAME_UNIQUE` (`NAME`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Funds`
--

LOCK TABLES `Funds` WRITE;
/*!40000 ALTER TABLE `Funds` DISABLE KEYS */;
INSERT INTO `Funds` VALUES (10,'Orvel Ventures'),(9,'Qualgro Partners'),(7,'Tanglin Venture Partners');
/*!40000 ALTER TABLE `Funds` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-07-10 17:24:04
