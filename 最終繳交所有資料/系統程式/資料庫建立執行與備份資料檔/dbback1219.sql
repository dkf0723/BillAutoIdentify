CREATE DATABASE  IF NOT EXISTS `112-112405` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `112-112405`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 140.131.114.242    Database: 112-112405
-- ------------------------------------------------------
-- Server version	8.0.35-0ubuntu0.22.04.1

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
-- Table structure for table `Manufacturer_Information`
--

DROP TABLE IF EXISTS `Manufacturer_Information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Manufacturer_Information` (
  `廠商編號` char(18) NOT NULL,
  `廠商名` char(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `負責或對接人` char(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `市話` char(12) DEFAULT NULL,
  `電話` char(10) DEFAULT NULL,
  `付款方式` char(2) NOT NULL,
  `行庫名` char(30) DEFAULT NULL,
  `行庫代號` char(3) DEFAULT NULL,
  `匯款帳號` char(14) DEFAULT NULL,
  `建立時間` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`廠商編號`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Manufacturer_Information`
--

LOCK TABLES `Manufacturer_Information` WRITE;
/*!40000 ALTER TABLE `Manufacturer_Information` DISABLE KEYS */;
INSERT INTO `Manufacturer_Information` VALUES ('manufacturer000001','燙金生鮮蔬果批發2群','燙金客服小幫手','(無)略過','略過','匯款','彰化商業銀行','009','05487860090078','2023-09-27 09:33:00'),('manufacturer000002','71go批發2館','尤琦瑋','略過','略過','匯款','中華郵政股份有限公司','700','00417960182048','2023-09-27 20:02:44'),('manufacturer000003','豪格嚴選(尊爵經銷)二館','豪格嚴選數位行銷','(無)略過','略過','匯款','玉山商業銀行','808','01285940119644','2023-09-27 20:04:33'),('manufacturer000004','冰品批發','鄭羿承','(無)略過','略過','匯款','中華郵政股份有限公司','700','02912070405674','2023-09-28 12:46:08'),('manufacturer000006','真好商號','林真好','(02)25678908','0978017567','現金','略過','略過','略過','2023-12-14 07:29:59'),('manufacturer000007','高罄食品','高罄','(02)24890128','略過','現金','略過','略過','略過','2023-12-14 22:58:50'),('manufacturer000008','吳慷時品','吳慷','(02)24890780','0978157000','現金','略過','略過','略過','2023-12-14 22:59:45'),('testMan000001','測試廠商','高培芮','(02)20901923','0909339101','匯款','略過','略過','略過','2023-09-27 09:28:44'),('testMan000002','阿蓉食品','阿蓉','(02)25670198','0967000124','現金',NULL,NULL,NULL,'2023-09-27 09:28:44'),('testMan000005','五號廠商','小五',NULL,'0909555555','現金',NULL,NULL,NULL,'2023-10-05 14:20:13');
/*!40000 ALTER TABLE `Manufacturer_Information` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Order_information`
--

DROP TABLE IF EXISTS `Order_information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Order_information` (
  `訂單編號` char(18) NOT NULL,
  `會員_LINE_ID` char(33) NOT NULL,
  `電話` char(10) NOT NULL,
  `訂單成立時間` datetime NOT NULL,
  `取貨完成時間` datetime DEFAULT NULL,
  `訂單狀態未取已取` char(5) NOT NULL,
  `評分數` float DEFAULT NULL,
  `評語內容` char(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `評分時間` datetime DEFAULT NULL,
  `商品圖片_顧客上傳` text,
  `總額` int DEFAULT NULL,
  `可取消訂單時間` datetime DEFAULT NULL,
  PRIMARY KEY (`訂單編號`),
  KEY `會員_LINE_ID` (`會員_LINE_ID`),
  CONSTRAINT `Order_information_ibfk_1` FOREIGN KEY (`會員_LINE_ID`) REFERENCES `member_profile` (`會員_LINE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Order_information`
--

LOCK TABLES `Order_information` WRITE;
/*!40000 ALTER TABLE `Order_information` DISABLE KEYS */;
INSERT INTO `Order_information` VALUES ('cart20230724000001','U829bc8925a60ec2cf8b25aa7d167b0cc','1add','2023-07-24 13:25:13','2023-11-25 23:05:44','預購已取',NULL,NULL,NULL,NULL,NULL,NULL),('cart20230724000002','Uc52aef2ae05ee1c9356ba20ea470947b','2add','2023-07-24 15:20:23',NULL,'預購未取',NULL,NULL,NULL,NULL,NULL,NULL),('cart20230727000001','U2ec5ee75f06ce4b8efde7604655b194e','3add','2023-07-27 14:06:04',NULL,'預購未取',NULL,NULL,NULL,NULL,NULL,NULL),('cart20230801000001','Uc889c85fdfd36d82a427672383a73572','4add','2023-08-01 14:22:09',NULL,'預購未取',NULL,NULL,NULL,NULL,NULL,NULL),('cart20230802000001','U3d7c25d64f92dbd3e413f9d238055bbb','5add','2023-08-02 09:19:32',NULL,'預購未取',NULL,NULL,NULL,NULL,NULL,NULL),('cart20230930000001','Uef6bbcc0906316aea2debe5d43020602','6add','2023-09-30 09:41:52',NULL,'預購未取',NULL,NULL,NULL,NULL,NULL,NULL),('cart20231119000001','Ucbff1a4f64c00c0a1d7a1611c1bf739a','add','2023-11-19 14:43:20',NULL,'add',NULL,NULL,NULL,NULL,NULL,NULL),('cart20231125000001','Ud816833e08a750c6f70900f0c0bb0790','add','2023-11-25 20:13:12',NULL,'add',NULL,NULL,NULL,NULL,NULL,NULL),('order2023072500001','U829bc8925a60ec2cf8b25aa7d167b0cc','7add','2023-07-25 13:19:00',NULL,'預購未取',NULL,NULL,NULL,NULL,275,NULL),('order2023072500002','U829bc8925a60ec2cf8b25aa7d167b0cc','8add','2023-07-25 13:50:00',NULL,'預購未取',NULL,NULL,NULL,NULL,275,NULL),('order2023072500003','U829bc8925a60ec2cf8b25aa7d167b0cc','9add','2023-07-25 13:50:00',NULL,'預購未取',NULL,NULL,NULL,NULL,405,NULL),('order2023072600001','U829bc8925a60ec2cf8b25aa7d167b0cc','10add','2023-07-26 12:32:00',NULL,'預購未取',NULL,NULL,NULL,NULL,785,NULL),('order2023072600002','U829bc8925a60ec2cf8b25aa7d167b0cc','11add','2023-07-26 13:20:00',NULL,'預購未取',NULL,NULL,NULL,NULL,625,NULL),('order2023072600003','U829bc8925a60ec2cf8b25aa7d167b0cc','0956235645','2023-07-26 13:23:00',NULL,'預購未取',NULL,NULL,NULL,NULL,625,NULL),('order2023072600004','U829bc8925a60ec2cf8b25aa7d167b0cc','0956235645','2023-07-26 13:26:00',NULL,'預購未取',NULL,NULL,NULL,NULL,625,NULL),('order2023072600005','U829bc8925a60ec2cf8b25aa7d167b0cc','0956789000','2023-07-26 13:29:17','2023-07-26 14:29:17','取消',NULL,NULL,NULL,NULL,20,NULL),('order2023072600006','U829bc8925a60ec2cf8b25aa7d167b0cc','0952000000','2023-07-26 14:32:05',NULL,'預購未取',NULL,NULL,NULL,NULL,440,NULL),('order2023072600007','U829bc8925a60ec2cf8b25aa7d167b0cc','0952000000','2023-07-26 14:34:07',NULL,'預購未取',NULL,NULL,NULL,NULL,110,NULL),('order2023072700001','U829bc8925a60ec2cf8b25aa7d167b0cc','0956235465','2023-07-27 13:32:24',NULL,'預購未取',NULL,NULL,NULL,NULL,440,NULL),('order2023072700002','Uc52aef2ae05ee1c9356ba20ea470947b','0978215471','2023-07-27 13:34:51','2023-11-26 22:09:44','預購已取',NULL,NULL,NULL,NULL,600,NULL),('order2023072700003','Uc52aef2ae05ee1c9356ba20ea470947b','0978215471','2023-07-27 13:36:55','2023-11-13 21:25:13','預購已取',NULL,NULL,NULL,NULL,800,NULL),('order2023072800001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029187','2023-07-28 14:14:54',NULL,'預購未取',NULL,NULL,NULL,NULL,440,NULL),('order2023072800002','U829bc8925a60ec2cf8b25aa7d167b0cc','0956789456','2023-07-28 14:32:02',NULL,'預購未取',NULL,NULL,NULL,NULL,105,NULL),('order2023072800003','U829bc8925a60ec2cf8b25aa7d167b0cc','0909678567','2023-07-28 15:19:30',NULL,'預購未取',NULL,NULL,NULL,NULL,220,NULL),('order2023072800004','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-07-28 15:23:29','2023-11-25 03:34:58','預購已取',NULL,NULL,NULL,NULL,220,NULL),('order2023072800005','U829bc8925a60ec2cf8b25aa7d167b0cc','0909764567','2023-07-28 15:27:59',NULL,'預購未取',NULL,NULL,NULL,NULL,220,NULL),('order2023072800006','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-07-28 15:33:52','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,220,NULL),('order2023072800007','U829bc8925a60ec2cf8b25aa7d167b0cc','0952098056','2023-07-28 15:38:55',NULL,'預購未取',NULL,NULL,NULL,NULL,220,NULL),('order2023072800008','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-07-28 15:42:49','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,220,NULL),('order2023072800009','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029156','2023-07-28 15:47:28',NULL,'預購未取',NULL,NULL,NULL,NULL,220,NULL),('order2023072800010','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029876','2023-07-28 15:59:26',NULL,'預購未取',NULL,NULL,NULL,NULL,105,NULL),('order2023072800011','U829bc8925a60ec2cf8b25aa7d167b0cc','0978667456','2023-07-28 16:07:01',NULL,'預購未取',NULL,NULL,NULL,NULL,105,NULL),('order2023072800012','U829bc8925a60ec2cf8b25aa7d167b0cc','0967894568','2023-07-28 16:07:44','2023-07-30 11:07:44','預購進貨',NULL,NULL,NULL,NULL,70,NULL),('order2023072800013','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029456','2023-07-28 17:02:38','2023-07-30 15:42:44','預購已取',NULL,NULL,NULL,NULL,210,NULL),('order2023080100001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952334667','2023-08-01 10:31:17',NULL,'預購未取',NULL,NULL,NULL,NULL,105,NULL),('order2023080100002','U2ec5ee75f06ce4b8efde7604655b194e','0909339101','2023-08-01 21:17:03','2023-11-29 14:36:58','預購已取',NULL,NULL,NULL,NULL,110,NULL),('order2023080300001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-08-03 15:22:10','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,80,NULL),('order2023080400001','Uc52aef2ae05ee1c9356ba20ea470947b','0978215471','2023-08-04 16:57:02','2023-11-18 11:48:17','預購已取',NULL,NULL,NULL,NULL,2200,NULL),('order2023080600001','U829bc8925a60ec2cf8b25aa7d167b0cc','0967800000','2023-08-06 21:32:33',NULL,'預購未取',NULL,NULL,NULL,NULL,110,NULL),('order2023080700001','U829bc8925a60ec2cf8b25aa7d167b0cc','0989678543','2023-08-07 14:13:40',NULL,'預購未取',NULL,NULL,NULL,NULL,220,NULL),('order2023080800001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-08-08 14:20:25','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,2255,NULL),('order2023080800002','U829bc8925a60ec2cf8b25aa7d167b0cc','0956000000','2023-08-08 14:34:27',NULL,'預購未取',NULL,NULL,NULL,NULL,880,NULL),('order2023080800003','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-08-08 14:54:30','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,740,NULL),('order2023081000001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-08-10 14:32:19','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,3120,NULL),('order2023081000002','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-08-10 14:36:31','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,740,NULL),('order2023081100001','U829bc8925a60ec2cf8b25aa7d167b0cc','0989078524','2023-08-11 02:13:37','2023-11-25 04:54:43','預購已取',NULL,NULL,NULL,NULL,105,NULL),('order2023081100002','U829bc8925a60ec2cf8b25aa7d167b0cc','0967867234','2023-08-11 02:15:02',NULL,'預購未取',NULL,NULL,NULL,NULL,105,NULL),('order2023081100003','U829bc8925a60ec2cf8b25aa7d167b0cc','0900000000','2023-08-11 02:16:38',NULL,'預購未取',NULL,NULL,NULL,NULL,55,NULL),('order2023081100004','U829bc8925a60ec2cf8b25aa7d167b0cc','0900000000','2023-08-11 02:17:48',NULL,'預購未取',NULL,NULL,NULL,NULL,105,NULL),('order2023081100005','U829bc8925a60ec2cf8b25aa7d167b0cc','0978567234','2023-08-11 09:36:59',NULL,'預購未取',NULL,NULL,NULL,NULL,200,NULL),('order2023081100006','U829bc8925a60ec2cf8b25aa7d167b0cc','0978567432','2023-08-11 09:50:33',NULL,'預購未取',NULL,NULL,NULL,NULL,510,NULL),('order2023081100007','U829bc8925a60ec2cf8b25aa7d167b0cc','0955456789','2023-08-11 10:31:59',NULL,'預購未取',NULL,NULL,NULL,NULL,105,NULL),('order2023081100008','U829bc8925a60ec2cf8b25aa7d167b0cc','0978567345','2023-08-11 10:32:32','2023-12-08 20:35:03','預購已取',NULL,NULL,NULL,NULL,1700,NULL),('order2023081900001','U3d7c25d64f92dbd3e413f9d238055bbb','0952000000','2023-08-19 13:31:54',NULL,'預購未取',NULL,NULL,NULL,NULL,220,NULL),('order2023082100001','U829bc8925a60ec2cf8b25aa7d167b0cc','0956789000','2023-08-21 12:41:23','2023-11-25 03:44:14','預購已取',NULL,NULL,NULL,NULL,105,NULL),('order2023082100002','U829bc8925a60ec2cf8b25aa7d167b0cc','0956789000','2023-08-21 12:42:46','2023-11-25 03:44:14','預購已取',NULL,NULL,NULL,NULL,220,NULL),('order2023082100003','U829bc8925a60ec2cf8b25aa7d167b0cc','0956789000','2023-08-21 12:44:36','2023-11-25 03:44:14','預購已取',NULL,NULL,NULL,NULL,325,NULL),('order2023082200001','U829bc8925a60ec2cf8b25aa7d167b0cc','0956789000','2023-08-22 16:30:53','2023-11-25 03:44:14','預購已取',NULL,NULL,NULL,NULL,80,NULL),('order2023082200002','U829bc8925a60ec2cf8b25aa7d167b0cc','0956789000','2023-08-22 17:32:36','2023-11-25 03:44:14','預購已取',NULL,NULL,NULL,NULL,105,NULL),('order2023082200003','U829bc8925a60ec2cf8b25aa7d167b0cc','0956789000','2023-08-22 17:33:57','2023-11-25 03:44:14','預購已取',NULL,NULL,NULL,NULL,340,NULL),('order2023082200004','U829bc8925a60ec2cf8b25aa7d167b0cc','0956789000','2023-08-22 17:34:46','2023-11-25 03:44:14','預購已取',NULL,NULL,NULL,NULL,780,NULL),('order2023082200005','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-08-22 18:09:29','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,520,NULL),('order2023082400001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-08-24 11:00:05','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,340,NULL),('order2023082400002','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-08-24 14:50:04','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,660,NULL),('order2023082400003','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-08-24 15:17:15','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,330,NULL),('order2023082500001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-08-25 13:49:00','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,105,NULL),('order2023082500002','Uc52aef2ae05ee1c9356ba20ea470947b','0978215471','2023-08-25 15:45:16','2023-11-18 17:47:23','預購已取',NULL,NULL,NULL,NULL,660,NULL),('order2023082600001','Uc52aef2ae05ee1c9356ba20ea470947b','0978215471','2023-08-26 00:03:24','2023-11-22 10:35:11','預購已取',NULL,NULL,NULL,NULL,660,NULL),('order2023082600002','Uc52aef2ae05ee1c9356ba20ea470947b','0978215471','2023-08-26 00:03:32','2023-11-22 10:35:11','預購已取',NULL,NULL,NULL,NULL,660,NULL),('order2023082600003','Uc52aef2ae05ee1c9356ba20ea470947b','0978215471','2023-08-26 00:04:19','2023-11-13 21:25:53','現購已取',NULL,NULL,NULL,NULL,210,NULL),('order2023082600004','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-08-26 14:18:08','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,105,NULL),('order2023082600005','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-08-26 16:14:58','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,80,NULL),('order2023083000001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-08-30 22:22:40','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,440,NULL),('order2023090600001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-09-06 15:40:25','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,440,NULL),('order2023091200001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-09-12 13:08:07','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,105,NULL),('order2023092000001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-09-20 19:02:19','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,105,NULL),('order2023092000002','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-09-20 19:03:22','2023-11-14 03:27:16','預購已取',NULL,NULL,NULL,NULL,70,NULL),('order2023092000003','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-09-20 19:05:17','2023-11-22 10:36:07','預購已取',NULL,NULL,NULL,NULL,325,NULL),('order2023092100001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-09-21 15:33:30','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,210,NULL),('order2023092100002','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-09-21 16:00:22','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,325,NULL),('order2023092100003','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-09-21 16:11:31','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,325,NULL),('order2023092100004','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-09-21 16:17:54','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,325,NULL),('order2023092100005','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-09-21 16:23:00','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,325,NULL),('order2023092100006','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-09-21 16:30:08','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,325,NULL),('order2023092100007','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-09-21 16:31:14','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,200,NULL),('order2023092200001','Uc52aef2ae05ee1c9356ba20ea470947b','0978215471','2023-09-22 19:17:49','2023-11-13 21:25:53','預購已取',NULL,NULL,NULL,NULL,200,NULL),('order2023092500001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-09-25 15:28:21','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,220,NULL),('order2023093000001','Uef6bbcc0906316aea2debe5d43020602','0978567432','2023-09-30 10:28:52',NULL,'預購未取',NULL,NULL,NULL,NULL,220,NULL),('order2023093000002','Uef6bbcc0906316aea2debe5d43020602','0978567432','2023-09-30 10:29:14',NULL,'預購未取',NULL,NULL,NULL,NULL,780,NULL),('order2023093000003','Uef6bbcc0906316aea2debe5d43020602','0978567432','2023-09-30 10:29:58',NULL,'預購未取',NULL,NULL,NULL,NULL,105,NULL),('order2023093000004','U3d7c25d64f92dbd3e413f9d238055bbb','0952000000','2023-09-30 11:19:57',NULL,'預購未取',NULL,NULL,NULL,NULL,440,NULL),('order2023093000005','U3d7c25d64f92dbd3e413f9d238055bbb','0952000000','2023-09-30 11:20:26',NULL,'預購進貨',NULL,NULL,NULL,NULL,70,NULL),('order2023100700001','Uc52aef2ae05ee1c9356ba20ea470947b','0978215471','2023-10-07 02:22:32','2023-11-13 21:25:53','預購已取',NULL,NULL,NULL,NULL,220,NULL),('order2023100700002','Uc52aef2ae05ee1c9356ba20ea470947b','0978215471','2023-10-07 04:48:44',NULL,'預購已取',NULL,NULL,NULL,NULL,500,NULL),('order2023101100001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-10-11 16:25:58','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,510,NULL),('order2023101100002','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-10-11 16:29:36','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,265,NULL),('order2023101100003','U2ec5ee75f06ce4b8efde7604655b194e','0909339101','2023-10-11 23:48:20','2023-11-29 14:43:16','預購已取',NULL,NULL,NULL,NULL,55,NULL),('order2023102300001','U2ec5ee75f06ce4b8efde7604655b194e','0909339101','2023-10-23 16:14:19',NULL,'預購未取',NULL,NULL,NULL,NULL,60,NULL),('order2023102300002','U2ec5ee75f06ce4b8efde7604655b194e','0909339101','2023-10-23 16:16:25',NULL,'預購未取',NULL,NULL,NULL,NULL,150,NULL),('order2023102500001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-10-25 17:57:48','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,2420,NULL),('order2023102500002','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-10-25 18:05:50','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,530,NULL),('order2023102600001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-10-26 12:36:38','2023-11-25 03:39:03','預購已取',NULL,NULL,NULL,NULL,220,NULL),('order2023111000001','Uc52aef2ae05ee1c9356ba20ea470947b','0978215471','2023-11-10 01:42:26',NULL,'預購',NULL,NULL,NULL,NULL,30,NULL),('order2023111000002','Uc52aef2ae05ee1c9356ba20ea470947b','0978215471','2023-11-10 01:42:43',NULL,'預購',NULL,NULL,NULL,NULL,180,NULL),('order2023111000003','Uc52aef2ae05ee1c9356ba20ea470947b','0978215471','2023-11-10 01:42:56',NULL,'預購',NULL,NULL,NULL,NULL,160,NULL),('order2023111000004','Uc52aef2ae05ee1c9356ba20ea470947b','0978215471','2023-11-10 01:43:09',NULL,'預購',NULL,NULL,NULL,NULL,200,NULL),('order2023111500001','U3d7c25d64f92dbd3e413f9d238055bbb','0952000000','2023-11-15 16:53:38',NULL,'現購未取',NULL,NULL,NULL,NULL,20,'2023-11-16 16:53:38'),('order2023112000001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-11-20 17:14:32','2023-11-25 03:39:03','現購已取',NULL,NULL,NULL,NULL,400,NULL),('order2023112000002','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-11-20 17:18:35','2023-11-25 03:39:03','現購已取',NULL,NULL,NULL,NULL,500,NULL),('order2023112400001','U3d7c25d64f92dbd3e413f9d238055bbb','0952000000','2023-11-24 10:48:46','2023-11-24 02:49:36','現購已取',NULL,NULL,NULL,NULL,55,NULL),('order2023112500001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-11-25 17:18:04','2023-12-14 13:11:23','現購已取',NULL,NULL,NULL,NULL,110,'2023-11-26 17:18:04'),('order2023112500002','Ud816833e08a750c6f70900f0c0bb0790','0952551123','2023-11-25 20:13:58','2023-11-25 12:19:28','現購已取',NULL,NULL,NULL,NULL,330,NULL),('order2023112500003','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-11-25 20:42:59','2023-11-25 12:43:43','現購已取',NULL,NULL,NULL,NULL,75,NULL),('order2023112900001','U2ec5ee75f06ce4b8efde7604655b194e','0909339101','2023-11-29 14:15:36',NULL,'現購未取',NULL,NULL,NULL,NULL,630,'2023-11-30 14:15:36'),('order2023113000001','Uc889c85fdfd36d82a427672383a73572','0967890123','2023-11-30 11:30:04','2023-11-30 11:31:02','現購已取',NULL,NULL,NULL,NULL,330,NULL),('order2023120200001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-02 15:44:27','2023-12-14 21:14:38','現購已取',NULL,NULL,NULL,NULL,340,NULL),('order2023120200002','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-02 15:49:55','2023-12-15 05:01:29','現購已取',NULL,NULL,NULL,NULL,265,NULL),('order2023120200003','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-02 16:05:55',NULL,'現購未取',NULL,NULL,NULL,NULL,0,NULL),('order2023120200004','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-02 16:07:55',NULL,'現購未取',NULL,NULL,NULL,NULL,0,'2023-12-03 16:07:55'),('order2023120200005','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-02 16:19:25','2023-12-02 19:14:38','現購取消',NULL,NULL,NULL,NULL,75,'2023-12-03 16:19:25'),('order2023120200006','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-02 16:21:39','2023-12-02 19:12:54','現購取消',NULL,NULL,NULL,NULL,320,'2023-12-03 16:21:40'),('order2023120200007','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-02 16:22:25','2023-12-02 19:09:15','預購未取',NULL,NULL,NULL,NULL,1240,NULL),('order2023120200008','Uc52aef2ae05ee1c9356ba20ea470947b','0978215471','2023-12-02 19:17:33','2023-12-02 19:18:01','現購取消',NULL,NULL,NULL,NULL,630,'2023-12-03 19:17:33'),('order2023120200009','Uc52aef2ae05ee1c9356ba20ea470947b','0978215471','2023-12-02 19:28:35','2023-12-02 19:29:11','現購取消',NULL,NULL,NULL,NULL,165,'2023-12-03 19:28:35'),('order2023120200010','Uc52aef2ae05ee1c9356ba20ea470947b','0978215471','2023-12-02 19:28:47',NULL,'現購未取',NULL,NULL,NULL,NULL,630,'2023-12-03 19:28:47'),('order2023120200011','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-02 20:05:01','2023-12-02 20:05:13','現購取消',NULL,NULL,NULL,NULL,175,'2023-12-03 20:05:01'),('order2023120200012','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-02 20:06:34','2023-12-02 20:07:00','預購未取',NULL,NULL,NULL,NULL,500,NULL),('order2023120200013','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-02 20:14:30','2023-12-02 20:14:45','預購取消',NULL,NULL,NULL,NULL,300,NULL),('order2023120300001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-03 17:43:46','2023-12-03 17:44:05','預購取消',NULL,NULL,NULL,NULL,14000,NULL),('order2023120500001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-05 13:16:05','2023-12-05 13:16:37','現購取消',NULL,NULL,NULL,NULL,175,'2023-12-06 13:16:05'),('order2023120600001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-06 14:37:52','2023-12-06 14:39:10','現購取消',NULL,NULL,NULL,NULL,735,'2023-12-07 14:37:56'),('order2023120600002','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-06 16:57:56','2023-12-06 16:58:23','預購取消',NULL,NULL,NULL,NULL,700,NULL),('order2023120600003','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-06 17:11:37',NULL,'現購未取',NULL,NULL,NULL,NULL,300,'2023-12-07 17:11:37'),('order2023121000001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-10 20:27:45','2023-12-10 20:28:00','現購取消',NULL,NULL,NULL,NULL,510,'2023-12-11 20:27:45'),('order2023121000002','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-10 20:29:18','2023-12-10 20:29:34','現購取消',NULL,NULL,NULL,NULL,340,'2023-12-11 20:29:18'),('order2023121200001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-12 23:20:50','2023-12-15 04:50:33','現購已取',NULL,NULL,NULL,NULL,175,'2023-12-13 23:20:50'),('order2023121400001','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-14 17:10:22',NULL,'預購未取',NULL,NULL,NULL,NULL,250,NULL),('order2023121400002','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-14 17:19:20','2023-12-14 17:19:35','預購未取',NULL,NULL,NULL,NULL,250,NULL),('order2023121400003','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-14 17:23:31','2023-12-14 17:23:48','現購取消',NULL,NULL,NULL,NULL,375,'2023-12-15 17:23:31'),('order2023121400004','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-14 21:00:22','2023-12-15 05:02:34','現購已取',NULL,NULL,NULL,NULL,75,'2023-12-15 21:00:22'),('order2023121400005','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-14 21:10:18','2023-12-14 21:13:05','現購已取',NULL,NULL,NULL,NULL,150,'2023-12-15 21:10:18'),('order2023121400006','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-14 21:42:22','2023-12-14 21:42:40','現購取消',NULL,NULL,NULL,NULL,75,'2023-12-15 21:42:22'),('order2023121500001','Uc52aef2ae05ee1c9356ba20ea470947b','0978215471','2023-12-15 13:35:27','2023-12-15 13:36:40','現購取消',NULL,NULL,NULL,NULL,220,'2023-12-16 13:35:27'),('order2023121500002','U829bc8925a60ec2cf8b25aa7d167b0cc','0952029143','2023-12-15 13:54:30','2023-12-15 13:54:40','現購取消',NULL,NULL,NULL,NULL,175,'2023-12-16 13:54:30'),('order2023121500003','U3d7c25d64f92dbd3e413f9d238055bbb','0952000000','2023-12-15 14:12:17','2023-12-15 14:12:33','現購取消',NULL,NULL,NULL,NULL,420,'2023-12-16 14:12:17'),('order2023121500004','U3d7c25d64f92dbd3e413f9d238055bbb','0952000000','2023-12-15 14:54:31','2023-12-15 14:54:49','現購取消',NULL,NULL,NULL,NULL,220,'2023-12-16 14:54:31'),('order2023121500005','U3d7c25d64f92dbd3e413f9d238055bbb','0952000000','2023-12-15 15:57:33','2023-12-15 15:58:06','現購取消',NULL,NULL,NULL,NULL,344,'2023-12-16 15:57:33');
/*!40000 ALTER TABLE `Order_information` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Product_information`
--

DROP TABLE IF EXISTS `Product_information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Product_information` (
  `商品ID` char(18) NOT NULL,
  `商品名稱` char(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `現預購商品` char(5) DEFAULT NULL,
  `商品圖片` text,
  `商品簡介` char(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `庫存數量` int DEFAULT NULL,
  `商品單位` char(3) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `售出單價` int NOT NULL,
  `商品建立時間` datetime NOT NULL,
  `預購數量限制_倍數` int DEFAULT NULL,
  `預購截止時間` datetime DEFAULT NULL,
  `商品可否退換貨` char(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `預評_評分數` float DEFAULT NULL,
  `預評_是否上架` tinyint(1) DEFAULT NULL,
  `預評_評分時間` datetime DEFAULT NULL,
  `售出單價2` int DEFAULT NULL,
  `廠商編號` char(18) DEFAULT NULL,
  `訂單剩餘` int DEFAULT NULL,
  PRIMARY KEY (`商品ID`),
  KEY `廠商編號` (`廠商編號`),
  CONSTRAINT `廠商編號` FOREIGN KEY (`廠商編號`) REFERENCES `Manufacturer_Information` (`廠商編號`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Product_information`
--

LOCK TABLES `Product_information` WRITE;
/*!40000 ALTER TABLE `Product_information` DISABLE KEYS */;
INSERT INTO `Product_information` VALUES ('1','ab s','a',NULL,'2',NULL,'2',2,'2023-11-20 11:27:06',NULL,NULL,'2',NULL,NULL,NULL,2,NULL,NULL),('1223','123','123',NULL,'123',NULL,'213',1231,'2023-11-18 17:18:35',NULL,NULL,'123',NULL,NULL,NULL,123,NULL,NULL),('123','123','123',NULL,'123',NULL,'213',1231,'2023-11-18 15:57:42',NULL,NULL,'123',NULL,NULL,NULL,123,NULL,NULL),('dailyuse000000','蛋包飯','現購','789','好好吃',NULL,'盒',120,'2023-11-21 05:07:18',NULL,NULL,'空白',NULL,NULL,NULL,120,NULL,NULL),('dessert000001','?草泥馬卡龍繽紛禮盒?','現購','https://i.imgur.com/J6rWzOk.jpg','一上架就被瘋狂搶購?\n全台限量草泥馬繽紛禮盒\n自吃送禮真的超有面子 人人搶著要\n?選用高級在地食材安佳奶油\n?薄鬆外層搭配柔軟內餡，重量360克（50顆）',51,'組',220,'2023-07-17 08:00:00',NULL,NULL,NULL,NULL,NULL,NULL,210,'manufacturer000002',5),('dessert000002','123','現購','3','So',NULL,'個',2,'2023-11-20 08:13:21',NULL,NULL,'退換',NULL,NULL,NULL,8,NULL,NULL),('dessert000003','櫻桃爺爺南棗核桃糕250g/袋裝(全素)','預購未取','https://i.imgur.com/cZ9NLvj.jpg','?2023年獲得食品界米其林的肯定\n每逢年節必吃的糕點-南棗核桃糕，自古以來被視為養生糕點??\n這款棗香四溢、甜度適中、Q軟剔透不黏牙的南棗核桃糕✨\n讓櫻桃奶奶臉上，終於露出滿意幸福的笑容~~\n為愛而生的美食傳說感動著無數人的心?\n效期：12個月/原產地：台灣\n',20,'袋',300,'2023-11-25 14:00:00',2,'2024-01-04 11:31:00',NULL,NULL,NULL,NULL,240,'manufacturer000001',NULL),('dessert000004','依蕾特經典招牌布丁奶酪-熱銷綜合口味（鮮奶*2 /可可*2 /芒果*2/芝麻*2）8入','預購未取','https://i.imgur.com/Aa5ZpQH.jpg','超夯的台南名產\n✨濃厚奶香味，吃過都回味，多種口味一次滿足',10,'組',320,'2023-11-25 14:00:00',1,'2024-01-10 12:00:00',NULL,NULL,NULL,NULL,310,'manufacturer000001',NULL),('dessert000005','依蕾特經典招牌布丁奶酪-【鮮奶布丁】(奶蛋素)8入','預購未取','https://i.imgur.com/Aa5ZpQH.jpg','超夯的台南名產\n✨濃厚奶香味，吃過都回味，多種口味一次滿足',10,'組',315,'2023-11-25 14:00:00',1,'2023-12-23 00:22:00',NULL,NULL,NULL,NULL,310,'manufacturer000001',NULL),('dessert000006','依蕾特經典招牌布丁奶酪-【可可奶酪】(奶素)8入','預購','https://i.imgur.com/Aa5ZpQH.jpg','超夯的台南名產\n✨濃厚奶香味，吃過都回味，多種口味一次滿足',0,'組',315,'2023-11-25 14:00:00',1,'2023-12-19 23:59:00',NULL,NULL,NULL,NULL,310,'manufacturer000001',NULL),('dessert000007','依蕾特經典招牌布丁奶酪-【芒果奶酪】(奶素)8入','預購','https://i.imgur.com/Aa5ZpQH.jpg','超夯的台南名產\n✨濃厚奶香味，吃過都回味，多種口味一次滿足',0,'組',325,'2023-11-25 14:00:00',1,'2023-12-19 23:59:00',NULL,NULL,NULL,NULL,310,'manufacturer000001',NULL),('dessert000008','依蕾特經典招牌布丁奶酪-【芝麻奶酪】(奶素)8入','預購未取','https://i.imgur.com/Aa5ZpQH.jpg','超夯的台南名產\n✨濃厚奶香味，吃過都回味，多種口味一次滿足',10,'組',315,'2023-11-25 14:00:00',1,'2023-12-19 23:59:00',NULL,NULL,NULL,NULL,310,'manufacturer000001',NULL),('dessert000009','蛋捲','現購','https://i.imgur.com/xJhhlhO.jpg','好吃的',NULL,'包',40,'2023-12-15 14:27:21',NULL,NULL,'可退',NULL,NULL,NULL,30,'manufacturer000001',NULL),('dessert000010','123','現購','https://i.imgur.com/59lAzBw.jpg','488',NULL,'個',388,'2023-12-15 14:34:36',NULL,NULL,'可退',NULL,NULL,NULL,299,'manufacturer000001',NULL),('dessert000011','蛋捲','現購','https://i.imgur.com/rSMviuL.jpg','盒',NULL,'盒',50,'2023-12-15 14:49:07',NULL,NULL,'可換',NULL,NULL,NULL,40,'manufacturer000001',NULL),('dessert000012','蛋捲','現購','https://i.imgur.com/Ptm2n5A.jpg','好吃',NULL,'包',50,'2023-12-15 15:52:56',NULL,NULL,'可退',NULL,NULL,NULL,40,'manufacturer000001',NULL),('drinks000001','有糖豆漿 $55/包','現購','https://i.imgur.com/UM9AdGO.jpg','怎麼放都不會凝固臭酸——粉泡豆漿 成本最便宜\n每次味道不一樣濃淡還有生味——豆腐店的漿水\n中式豆漿店的豆漿—有設備自製沒問題?\n專業HACCP豆漿大廠製，也有OEM別品牌\n⚠請保持冷藏狀態，都不能碰到生水\n⚠保存期限：冷藏6-7天\n規格：一袋都是2500ml（家庭號）',70,'包',55,'2023-07-17 08:00:00',2,'2023-08-31 08:00:00',NULL,NULL,NULL,NULL,NULL,'manufacturer000001',10),('drinks000002','無糖豆漿 $55/包','預購未取','https://i.imgur.com/LNnWROS.jpg','怎麼放都不會凝固臭酸——粉泡豆漿 成本最便宜\n每次味道不一樣濃淡還有生味——豆腐店的漿水\n中式豆漿店的豆漿—有設備自製沒問題?\n專業HACCP豆漿大廠製，也有OEM別品牌\n⚠請保持冷藏狀態，都不能碰到生水\n⚠保存期限：冷藏6-7天\n規格：一袋都是2500ml（家庭號）',10,'包',55,'2023-07-17 08:00:00',2,'2024-01-01 12:15:00',NULL,NULL,NULL,NULL,NULL,'manufacturer000001',NULL),('drinks000003','薏仁漿 $70/包','預購截止','https://i.imgur.com/vrUMR5D.jpg','怎麼放都不會凝固臭酸——粉泡豆漿 成本最便宜\n每次味道不一樣濃淡還有生味——豆腐店的漿水\n中式豆漿店的豆漿—有設備自製沒問題?\n專業HACCP豆漿大廠製，也有OEM別品牌\n⚠請保持冷藏狀態，都不能碰到生水\n⚠保存期限：冷藏6-7天\n規格：一袋都是2500ml（家庭號）',0,'包',70,'2023-07-17 08:00:00',1,'2023-08-31 08:00:00',NULL,NULL,NULL,NULL,NULL,'manufacturer000001',NULL),('drinks000004','米漿 $70/包','預購未取','https://i.imgur.com/n2d9DJe.jpg','怎麼放都不會凝固臭酸——粉泡豆漿 成本最便宜\n每次味道不一樣濃淡還有生味——豆腐店的漿水\n中式豆漿店的豆漿—有設備自製沒問題?\n專業HACCP豆漿大廠製，也有OEM別品牌\n⚠請保持冷藏狀態，都不能碰到生水\n⚠保存期限：冷藏6-7天\n規格：一袋都是2500ml（家庭號）',50,'包',70,'2023-07-17 08:00:00',1,'2023-08-31 08:00:00',NULL,NULL,NULL,NULL,NULL,'manufacturer000001',NULL),('drinks000005','黑豆漿$70/包','現購停售','https://i.imgur.com/gInqh5w.jpg','怎麼放都不會凝固臭酸——粉泡豆漿 成本最便宜\n每次味道不一樣濃淡還有生味——豆腐店的漿水\n中式豆漿店的豆漿—有設備自製沒問題?\n專業HACCP豆漿大廠製，也有OEM別品牌\n⚠請保持冷藏狀態，都不能碰到生水\n⚠保存期限：冷藏6-7天\n規格：一袋都是2500ml（家庭號）',11,'包',70,'2023-07-17 08:00:00',1,'2023-08-31 08:00:00',NULL,NULL,NULL,NULL,NULL,'manufacturer000001',11),('frozen000001','高麗菜豬肉/22顆','現購','https://i.imgur.com/yUvLyqF.jpg','?創立於民國39年 \n最早是以製麵起家，至今已有六十年多的歷史了\n煮好的水餃可以感受到手工的口感，皮Q彈，果然跟機器的有差～\n每款餡料香甜肉扎實，一口咬下還有湯汁\n好吃肉餡不油膩，裏頭的餡料比例調和的十分完美，根本就不要沾醬囉～一口接著一口?',10,'包',175,'2023-07-17 08:00:00',1,'2023-10-29 20:12:00',NULL,NULL,NULL,NULL,172,'manufacturer000003',21),('frozen000002','韭菜豬肉/22顆','現購','https://i.imgur.com/yUvLyqF.jpg','?創立於民國39年 \n最早是以製麵起家，至今已有六十年多的歷史了\n煮好的水餃可以感受到手工的口感，皮Q彈，果然跟機器的有差～\n每款餡料香甜肉扎實，一口咬下還有湯汁\n好吃肉餡不油膩，裏頭的餡料比例調和的十分完美，根本就不要沾醬囉～一口接著一口?',20,'包',175,'2023-07-17 08:00:00',1,'2023-08-31 08:00:00',NULL,NULL,NULL,NULL,NULL,'manufacturer000003',3),('frozen000003','白菜韭黃豬肉/22顆','現購','https://i.imgur.com/yUvLyqF.jpg','?創立於民國39年 \n最早是以製麵起家，至今已有六十年多的歷史了\n煮好的水餃可以感受到手工的口感，皮Q彈，果然跟機器的有差～\n每款餡料香甜肉扎實，一口咬下還有湯汁\n好吃肉餡不油膩，裏頭的餡料比例調和的十分完美，根本就不要沾醬囉～一口接著一口?',19,'包',190,'2023-07-17 08:00:00',1,'2023-08-31 08:00:00',NULL,NULL,NULL,NULL,170,'manufacturer000003',6),('frozen000004','安佳奶油','現購','https://i.imgur.com/7c7Mrrl.jpg','小巧迷你，一顆用一次剛剛好一點都不浪費！數量有限~要搶要快唷！\n天然奶油，無人工反式脂肪無防腐劑，無化學添加物天然純淨美味，紐西蘭原裝進口\n成分：乳脂、水分(含奶類製品)\n規格：7g/顆，20顆/組\n保存方式：冷藏儲存\n原產地：紐西蘭\n有效日期：2023/08/05',12,'組',80,'2023-07-17 08:00:00',2,'2023-08-31 08:00:00',NULL,NULL,NULL,NULL,75,'manufacturer000004',10),('frozen000005','新竹海哥芋頭米粉鍋','現購停售','https://i.imgur.com/B7eqsrk.jpg','採用大甲芋頭口感鬆軟，搭配香菇，五花肉，彈牙米粉加上香濃佐料一起燉煮，芋頭香飄溢好滋味化在濃郁湯汁裏，包準讓你大口大口吃不停。\n成分 : 芋頭、香菇、豬肉絲、蔬菜高湯、米粉、蒜苗、胡椒粉\n商品規格：1600公克±20公克，適合2-3人食用\n保存期限：標示於包裝上\n保存方式：-18℃以下冷凍保存6個月',30,'包',265,'2023-07-17 08:00:00',1,'2023-08-31 08:00:00',NULL,NULL,NULL,NULL,260,'manufacturer000001',60),('frozen000019','鳳梨卡拉蝦球(買一送一)','預購','https://i.imgur.com/MbTgMx5.jpg','獨家販售，團購超人氣多種吃法\n想吃蝦球還在自己剝殼？裹粉？\n弄的一踏糊塗的只為了隻蝦球？好麻煩(ah...) \n看過來！！現在不用再自己剝蝦裹粉\n就能吃到每顆蝦球都是一隻完整的蝦~\n香！酥！脆！ 【氣炸~】【油炸】 【烤箱】都ok\n',0,'組',250,'2023-11-25 14:00:00',1,'2023-12-23 23:59:00',NULL,NULL,NULL,NULL,230,'manufacturer000001',NULL),('frozen000020','?【王牌大廚】泰式蝦捲12條(附醬)買1送1','現購','https://i.imgur.com/Zu5FN6e.jpg','婆婆媽媽們千萬不要錯過這檔超好康\n無基改千張豆皮，取代傳統的豬網油\n捨棄掉油膩的舊式方法，吃的健康無負擔?\n迎接而來的是清爽又美味的新口感\n買回家自己炸，吃的過癮吃的滿足\n也可以放平地鍋煎恰恰超級好吃der',30,'組',175,'2023-11-25 14:00:00',NULL,NULL,NULL,NULL,NULL,NULL,0,'manufacturer000001',30),('frozen000021','王老爹港式蘿蔔糕','現購','https://i.imgur.com/Bg9nuqC.jpg','回購率超高的港式蘿蔔糕來嚕，家裡的小朋友超愛吃，一煎完就被秒殺\n純手工製作，真材實料\n純在來米，絕非便宜的在來粉\n絕非冷凍食品，讓您吃的安心又健康\n好吃高貴，價格實惠，錯過後悔，吃過回味\n一片片都幫你切割好，讓你方便料理，重點不黏鍋\n芋頭糕使用大甲芋頭\n',230,'條',75,'2023-11-25 14:00:00',NULL,NULL,NULL,NULL,NULL,NULL,0,'manufacturer000001',222),('frozen000022','王老爹大甲芋頭糕','現購','https://i.imgur.com/Bg9nuqC.jpg','回購率超高的港式蘿蔔糕來嚕，家裡的小朋友超愛吃，一煎完就被秒殺\n純手工製作，真材實料\n純在來米，絕非便宜的在來粉\n絕非冷凍食品，讓您吃的安心又健康\n好吃高貴，價格實惠，錯過後悔，吃過回味\n一片片都幫你切割好，讓你方便料理，重點不黏鍋\n芋頭糕使用大甲芋頭\n',230,'條',95,'2023-11-25 14:00:00',NULL,NULL,NULL,NULL,NULL,NULL,0,'manufacturer000001',230),('frozen000023','呷厝味-鍋爐爺爺燉雞湯-剝皮辣椒雞1kg','現購','https://i.imgur.com/ZJox5fZ.jpg','CP值超高！大份量！吃過都說讚～\n四季皆可補，免廚藝加熱即食唷✨\n平時就是要來碗熱騰騰的養生雞湯滋補一下\n媽咪料理偷吃步～燉湯再也不用技術囉\n只要有了這一包，隨時隨地都能幫家人滋補一下\n原汁原味最平價養生的雞湯',66,'包',165,'2023-11-25 14:00:00',NULL,NULL,NULL,NULL,NULL,NULL,160,'manufacturer000001',66),('frozen000024','呷厝味-鍋爐爺爺燉雞湯-巴西蘑菇雞1kg','現購','https://i.imgur.com/k36iUd6.jpg','CP值超高！大份量！吃過都說讚～\n四季皆可補，免廚藝加熱即食唷✨\n平時就是要來碗熱騰騰的養生雞湯滋補一下\n媽咪料理偷吃步～燉湯再也不用技術囉\n只要有了這一包，隨時隨地都能幫家人滋補一下\n原汁原味最平價養生的雞湯',56,'包',165,'2023-11-25 14:00:00',NULL,NULL,NULL,NULL,NULL,NULL,0,'manufacturer000001',54),('frozen000025','呷厝味-鍋爐爺爺燉雞湯-枸尾雞湯1kg','現購','https://i.imgur.com/cPDUm14.jpg','CP值超高！大份量！吃過都說讚～\n四季皆可補，免廚藝加熱即食唷✨\n平時就是要來碗熱騰騰的養生雞湯滋補一下\n媽咪料理偷吃步～燉湯再也不用技術囉\n只要有了這一包，隨時隨地都能幫家人滋補一下\n原汁原味最平價養生的雞湯',76,'包',165,'2023-11-25 14:00:00',NULL,NULL,NULL,NULL,NULL,NULL,155,'manufacturer000001',74),('frozen000026','呷厝味-鍋爐爺爺燉雞湯-老薑麻油鴨血雞1kg','現購','https://i.imgur.com/p4TC1Lo.jpg','CP值超高！大份量！吃過都說讚～\n四季皆可補，免廚藝加熱即食唷✨\n平時就是要來碗熱騰騰的養生雞湯滋補一下\n媽咪料理偷吃步～燉湯再也不用技術囉\n只要有了這一包，隨時隨地都能幫家人滋補一下\n原汁原味最平價養生的雞湯',56,'包',165,'2023-11-25 14:00:00',NULL,NULL,NULL,NULL,NULL,NULL,0,'manufacturer000001',56),('frozen000027','呷厝味-鍋爐爺爺燉雞湯-茶樹菇湯1kg','現購','https://i.imgur.com/P3njj47.jpg','CP值超高！大份量！吃過都說讚～\n四季皆可補，免廚藝加熱即食唷✨\n平時就是要來碗熱騰騰的養生雞湯滋補一下\n媽咪料理偷吃步～燉湯再也不用技術囉\n只要有了這一包，隨時隨地都能幫家人滋補一下\n原汁原味最平價養生的雞湯',56,'包',165,'2023-11-25 14:00:00',NULL,NULL,NULL,NULL,NULL,NULL,0,'manufacturer000001',56),('frozen000028','呷厝味-鍋爐爺爺燉雞湯-香濃黑蒜雞1kg','現購','https://i.imgur.com/h3aUhwq.jpg','CP值超高！大份量！吃過都說讚～\n四季皆可補，免廚藝加熱即食唷✨\n平時就是要來碗熱騰騰的養生雞湯滋補一下\n媽咪料理偷吃步～燉湯再也不用技術囉\n只要有了這一包，隨時隨地都能幫家人滋補一下\n原汁原味最平價養生的雞湯',56,'包',165,'2023-11-25 14:00:00',NULL,NULL,NULL,NULL,NULL,NULL,0,'manufacturer000001',56),('frozen000035','顧客取貨','現購','2023-12-26 00:17:00','1',NULL,'個',3,'2023-12-15 00:17:52',388,'2023-12-20 00:17:00',NULL,NULL,NULL,NULL,29,'manufacturer000003',NULL),('frozen000036','1','現購','https://i.imgur.com/wFVgeBB.jpg','1',NULL,'個',1,'2023-12-15 00:45:09',NULL,NULL,'可退',NULL,NULL,NULL,1,'manufacturer000001',NULL),('frozen000037','1','現購','https://i.imgur.com/YnYASOH.jpg','3',NULL,'個',4,'2023-12-15 01:04:04',NULL,NULL,'可退',NULL,NULL,NULL,5,'manufacturer000001',NULL),('frozen000038','1','現購','ttps://i.imgur.com/Qd2rN7y.jpg','2',NULL,'桶',3,'2023-12-15 01:05:17',NULL,NULL,'可退',NULL,NULL,NULL,4,'manufacturer000001',NULL),('frozen000039','1','現購','https://i.imgur.com/hRubp6R.jpg','19',NULL,'個',378,'2023-12-15 14:35:31',NULL,NULL,'可退',NULL,NULL,NULL,2,'manufacturer000001',NULL),('hai00001','海碧哈哈','預購未取',NULL,NULL,20,'顆',50,'2023-10-06 15:11:17',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0),('local000001','福隆便當 香噴噴五花控肉500g','預購','https://i.imgur.com/Yq2hWYb.jpg','你看看！你看看！那肥瘦勻稱的控肉\n油油亮亮的！沒錯……就是這一味\n讓人會懷念的古早味美食?\n特聘福隆便當主廚坐鎮技術監督\n絕對保證色、香、味、俱全',0,'包',155,'2023-11-25 14:00:00',1,'2023-12-23 23:59:00',NULL,NULL,NULL,NULL,150,'manufacturer000001',NULL),('snack000001','爭鮮香甜甘栗分享包(30g*10入)','預購','https://i.imgur.com/UVYylSv.jpg','想吃栗子免剝殼‼️整顆都幫你剝好囉~\n爭鮮甘栗採甘栗中的天王品種\n百分之百原汁原味，不添加任何化學物質\n粒粒香甜又飽滿，口感鬆軟又濃郁\n直接吃或是冰冰的吃，加熱後吃都十分美味可口\n大人小孩都喜歡，絕對讓你一口接著一口停不下來!\n規格：30g/小包 ，10小包/袋，2袋一組\n',0,'包',145,'2023-11-25 14:00:00',1,'2023-12-15 23:59:00',NULL,NULL,NULL,NULL,140,'manufacturer000001',NULL),('staplefood000001','蘑菇鐵板麵','現購','https://i.imgur.com/7f9TASB.jpg','特別選用冷凍覆熱不軟爛的烏龍麵，搭配麵條好夥伴蘑菇醬\n與黑胡椒醬，醬汁超級濃郁，吸附在麵條上，每一口都是幸福的滋味～\n✅規格：290g/包(含1包麵1包醬)；一袋有5包\n✅效期：冷凍一年',75,'袋',120,'2023-07-17 08:00:00',NULL,NULL,NULL,NULL,NULL,NULL,100,'manufacturer000002',23),('staplefood000002','黑胡椒鐵板麵','現購','https://i.imgur.com/wmIZ02Q.jpg','特別選用冷凍覆熱不軟爛的烏龍麵，搭配麵條好夥伴蘑菇醬\n與黑胡椒醬，醬汁超級濃郁，吸附在麵條上，每一口都是幸福的滋味～\n✅規格：290g/包(含1包麵1包醬)；一袋有5包\n✅效期：冷凍一年',50,'袋',145,'2023-07-17 08:00:00',NULL,NULL,NULL,NULL,NULL,NULL,100,'manufacturer000002',17),('test000001','高逸嚴選商品','預購未取','【修改商品資訊】商品名稱','我的抓抓',NULL,'包',1000,'2023-08-02 21:19:00',2,'2023-11-01 19:30:00',NULL,NULL,NULL,NULL,20,NULL,NULL),('test000006','飯糰','現購',NULL,NULL,19,'包',25,'2023-10-06 15:11:17',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,19),('test000007','雲朵棉花糖','現購','https://i.imgur.com/rGlTAt3.jpg','像雲朵一樣入口即化的棉花糖',52,'包',30,'2023-10-06 15:12:18',NULL,NULL,NULL,NULL,NULL,NULL,10,NULL,30),('test000008','台南玉井芒果乾','預購未取',NULL,NULL,335,'包',99,'2023-10-06 15:12:57',NULL,'2023-10-25 22:08:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL),('test000009','有夠香豆干','現購',NULL,'豆干如此方正，買豆干的你(妳)們不是帥哥就是美女呀',37,'包',40,'2023-10-06 15:13:39',NULL,NULL,NULL,NULL,NULL,NULL,38,NULL,20),('test000010','測試商品-轉骨中藥包','現購',NULL,NULL,13,'包',200,'2023-10-06 15:14:24',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),('test000014','皇后麵','預購未取','https://i.imgur.com/rGlTAt3.jpg','好好吃',20,'包',67,'2023-10-23 15:00:00',NULL,'2023-12-07 19:33:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL),('test000015','烏龍麵','預購未取',NULL,'好吃的烏龍麵還不趕快來吃',10,'包',30,'2023-10-23 16:10:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),('test00002','わたし帥布丁','現購','https://i.imgur.com/rGlTAt3.jpg','擁有五官長相的布丁是很帥氣的´･ᴗ･`',150,'顆',20,'2023-08-03 16:57:00',NULL,NULL,NULL,NULL,NULL,NULL,18,NULL,139),('test00003','台東大目釋迦','預購未取','【修改商品資訊】商品名稱','台灣台東的大目釋迦有機無害',10,'顆',55,'2023-08-24 10:27:00',3,'2023-11-03 20:16:00',NULL,NULL,NULL,NULL,50,NULL,1),('test00004','脆笛酥','預購未取',NULL,'還記得小時候的回憶！脆笛酥讓你(妳)像大人一樣帥氣 ( ´Д`)y━･~~',20,'包',30,'2023-09-17 00:00:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,5),('test00005','榴槤','預購未取',NULL,'泰國榴槤',75,'顆',400,'2023-09-17 00:00:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,25),('test00009','嘉興呵呵','預購',NULL,NULL,0,'顆',40,'2023-10-16 15:11:17',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0),('test00010','宜蘭肉圓','預購',NULL,NULL,10,'顆',30,'2023-10-16 16:11:17',NULL,'2023-10-28 18:27:00',NULL,NULL,NULL,NULL,NULL,NULL,0),('test00011','可愛的圓圓','現購','商品管理','我們是好姊妹',10,'顆',110,'2023-10-16 00:00:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0),('測試資料-','豪大香腸','測試',NULL,NULL,50,'根',40,'2023-09-17 00:00:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,50);
/*!40000 ALTER TABLE `Product_information` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Purchase_Information`
--

DROP TABLE IF EXISTS `Purchase_Information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Purchase_Information` (
  `UID` int NOT NULL AUTO_INCREMENT,
  `商品ID` char(18) NOT NULL,
  `廠商方商品序號` char(20) DEFAULT NULL,
  `進貨數量` int NOT NULL,
  `進貨單價` int NOT NULL,
  `商品單位` char(3) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `進貨時間` datetime DEFAULT NULL,
  `匯款時間` datetime DEFAULT NULL,
  `匯款金額` int DEFAULT NULL,
  `進貨狀態` char(3) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`UID`),
  KEY `商品ID` (`商品ID`),
  CONSTRAINT `Purchase_Information_ibfk_1` FOREIGN KEY (`商品ID`) REFERENCES `Product_information` (`商品ID`)
) ENGINE=InnoDB AUTO_INCREMENT=117 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Purchase_Information`
--

LOCK TABLES `Purchase_Information` WRITE;
/*!40000 ALTER TABLE `Purchase_Information` DISABLE KEYS */;
INSERT INTO `Purchase_Information` VALUES (3,'test000001',NULL,0,0,'包','2023-08-02 21:19:00','2023-08-02 21:19:00',0,'已到貨'),(5,'test00003',NULL,10,10,'顆','2023-08-24 16:19:00','2023-08-24 20:19:00',0,'已到貨'),(8,'drinks000003',NULL,30,10,'包','2023-09-25 13:20:00','2023-09-22 14:20:00',300,'已到貨'),(9,'drinks000005',NULL,10,55,'包','2023-09-27 13:20:00','2023-09-23 13:20:00',550,'已到貨'),(10,'staplefood000001',NULL,15,40,'袋','2023-09-29 18:20:00','2023-09-26 13:20:00',600,'已到貨'),(13,'frozen000005',NULL,20,40,'包','2023-10-11 14:30:00','2023-10-11 14:30:00',800,'已到貨'),(14,'frozen000003',NULL,10,20,'包','2023-10-11 14:30:00','2023-10-11 14:30:00',200,'已到貨'),(15,'staplefood000002',NULL,5,40,'袋','2023-10-01 14:10:00','2023-10-01 12:10:00',200,'已到貨'),(23,'drinks000002',NULL,10,50,'包','2023-10-12 14:30:00','2023-10-11 14:30:00',500,'已到貨'),(25,'test00005',NULL,50,100,'顆','2023-10-11 14:30:00','2023-10-09 14:30:00',5000,'已到貨'),(26,'frozen000004',NULL,10,5,'組','2023-10-01 14:10:00','2023-10-01 14:10:00',50,'已到貨'),(27,'test00004',NULL,15,20,'包','2023-10-01 14:10:00','2023-10-01 14:10:00',300,'已到貨'),(31,'frozen000001',NULL,10,150,'包','2023-10-01 14:10:00','2023-10-01 14:10:00',1500,'已到貨'),(32,'drinks000004',NULL,50,30,'包','2023-10-01 14:10:00','2023-10-01 14:10:00',1500,'已到貨'),(35,'frozen000002',NULL,20,30,'包','2023-10-01 14:10:00','2023-10-01 14:10:00',600,'已到貨'),(36,'drinks000001',NULL,30,45,'包','2023-10-10 14:30:00','2023-10-10 14:30:00',1350,'已到貨'),(44,'hai00001',NULL,20,30,'顆','2023-10-13 14:30:00','2023-10-13 14:30:00',600,'已到貨'),(46,'test000007',NULL,10,20,'包','2023-10-13 14:30:00','2023-10-13 14:30:00',200,'已到貨'),(59,'test000014',NULL,10,40,'包','2023-10-23 17:03:05','2023-10-10 13:55:00',400,'已到貨'),(60,'test000008',NULL,50,20,'包','2023-08-02 21:19:00','2023-11-02 21:46:01',1000,'已到貨'),(61,'test000015',NULL,10,50,'包','2023-10-23 18:28:08','2023-10-10 13:55:00',500,'已到貨'),(67,'test000006',NULL,10,30,'包','2023-10-29 19:35:03',NULL,300,'已到貨'),(69,'test000009',NULL,20,30,'包','2023-10-31 23:43:28',NULL,600,'已到貨'),(70,'test000009',NULL,10,30,'顆','2023-10-23 23:36:00','2023-11-01 19:06:00',300,'進貨中'),(71,'test000010',NULL,10,60,'包','2023-11-07 14:17:20',NULL,600,'已到貨'),(73,'dessert000001',NULL,10,60,'組','2023-11-07 16:40:25',NULL,600,'已到貨'),(83,'test00003',NULL,10,30,'顆','2023-11-08 22:46:42','2023-11-08 22:47:00',300,'已到貨'),(84,'test00011',NULL,10,40,'顆','2023-11-08 23:13:46',NULL,400,'已到貨'),(85,'test000007',NULL,25,30,'包','2023-11-09 22:53:37',NULL,750,'已到貨'),(86,'test000008',NULL,10,30,'包','2023-11-09 23:24:51','2023-11-09 23:25:26',300,'已到貨'),(87,'test000007',NULL,15,40,'包','2023-11-09 23:45:11',NULL,600,'已到貨'),(88,'test000008',NULL,15,50,'包','2023-11-09 23:46:16','2023-11-09 23:47:27',750,'已到貨'),(89,'test000008',NULL,10,50,'包','2023-11-09 23:57:30',NULL,500,'已到貨'),(90,'test000008',NULL,40,60,'包','2023-11-09 23:59:23','2023-11-09 23:59:47',2400,'已到貨'),(91,'dessert000001',NULL,10,30,'組','2023-11-11 19:11:43','2023-11-11 19:11:00',300,'已到貨'),(92,'dessert000001',NULL,10,30,'組','2023-11-11 19:20:24','2023-11-11 19:20:00',300,'已到貨'),(93,'dessert000001',NULL,10,30,'組','2023-11-11 19:27:12','2023-11-11 19:27:00',300,'已到貨'),(94,'dessert000001',NULL,10,30,'組','2023-11-11 19:38:21','2023-11-11 19:38:00',300,'已到貨'),(95,'dessert000001',NULL,5,450,'組','2023-11-11 19:39:23','2023-11-14 19:45:00',2250,'已到貨'),(96,'dessert000001',NULL,10,30,'組','2023-11-11 19:51:59','2023-11-11 19:52:00',300,'已到貨'),(97,'frozen000004',NULL,2,5,'組','2023-11-13 18:15:21','2023-12-09 18:15:00',10,'已到貨'),(98,'test000014',NULL,10,50,'包','2023-11-14 11:19:41','2023-11-14 11:19:00',500,'已到貨'),(99,'dessert000003',NULL,10,30,'袋','2023-12-04 13:19:16','2023-12-04 13:19:00',300,'已到貨'),(100,'frozen000020',NULL,10,40,'組','2023-12-04 13:19:37','2023-12-04 13:19:00',400,'已到貨'),(101,'dessert000004',NULL,10,50,'組','2023-12-05 23:15:34','2023-12-05 23:15:00',500,'已到貨'),(102,'drinks000005',NULL,1,65,'包','2023-12-13 23:02:52','2023-12-13 23:02:00',65,'已到貨'),(103,'dessert000005',NULL,10,40,'組','2023-12-15 05:02:00','2023-12-14 21:01:00',400,'已到貨'),(104,'frozen000005',NULL,10,30,'包','2023-12-15 05:04:04','2023-12-14 21:04:00',300,'已到貨'),(105,'dessert000003',NULL,20,25,'袋','2023-12-15 05:04:30','2023-12-14 21:04:00',500,'已到貨'),(106,'dessert000006',NULL,10,50,'組','2023-12-14 21:20:04','2023-12-14 21:20:00',500,'進貨中'),(107,'frozen000023',NULL,10,60,'包','2023-12-14 21:21:16','2023-12-14 21:21:00',600,'已到貨'),(108,'frozen000025',NULL,20,200,'包','2023-12-14 22:52:24','2023-12-28 22:52:00',4000,'已到貨'),(109,'dessert000003',NULL,10,50,'袋','2023-12-15 00:06:07','2023-12-15 00:06:00',500,'進貨中'),(110,'frozen000001',NULL,1,150,'包','2023-12-15 00:20:33','2023-12-15 00:20:00',150,'進貨中'),(111,'dessert000007',NULL,15,250,'組','2023-12-15 11:27:53','2023-12-15 11:27:00',3750,'進貨中'),(112,'dessert000001',NULL,20,100,'組','2023-12-15 11:28:38','2023-12-15 11:28:00',2000,'進貨中'),(113,'dessert000003',NULL,13,50,'袋','2023-12-15 11:29:08','2023-12-15 11:29:00',650,'進貨中'),(114,'staplefood000001',NULL,10,50,'袋','2023-12-15 11:40:20','2023-12-15 11:40:00',500,'已到貨'),(115,'snack000001',NULL,10,50,'包','2023-12-15 14:51:03','2023-12-15 14:50:00',500,'進貨中'),(116,'dessert000008',NULL,10,30,'組','2023-12-15 15:53:53','2023-12-15 15:53:00',300,'已到貨');
/*!40000 ALTER TABLE `Purchase_Information` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Questions_and_Answers`
--

DROP TABLE IF EXISTS `Questions_and_Answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Questions_and_Answers` (
  `UID` int NOT NULL AUTO_INCREMENT,
  `類別` char(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `問題` char(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `回答` char(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`UID`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Questions_and_Answers`
--

LOCK TABLES `Questions_and_Answers` WRITE;
/*!40000 ALTER TABLE `Questions_and_Answers` DISABLE KEYS */;
INSERT INTO `Questions_and_Answers` VALUES (1,'常見類','五大功能簡單介紹','1.團購商品：這邊提供兩大類商品列表。\n2.營業資訊：這邊有關於高逸嚴選百貨團購的簡介與地點導航。\n3.訂單/購物車查詢：可以查看所有的訂單狀態、購物車的內容與修改。\n4.許願商品：遇到喜歡的商品可以推薦給團媽呦～\n5.問題提問：提供簡單的問題為您提供簡易的解決辦法。'),(2,'操作類','營業地點在哪裡？','請點擊下方功能中的「營業資訊」取得營業地點，如果不熟悉地點的話也可以按下 ”地圖導航按鈕”，快速開啟地圖呦～'),(3,'操作類','該如何瀏覽商品呢？','請點擊下方功能中的「團購商品」，此處分為兩大類商品(現購商品、預購商品)找尋商品喔！'),(4,'操作類','商品列表瀏覽方式？','進入「團購商品/現購商品列表或預購商品列表」後，以左右滑動方式瀏覽商品。'),(5,'操作類','商品列表瀏覽到底怎麼辦？','進入「團購商品/現購商品列表或預購商品列表」後，瀏覽到底時。\n1.如遇到還有商品的話請點擊最後一個框框中的下一頁即可繼續瀏覽其他商品。\n2.如遇到沒有商品了則會顯示”已到底”，此時點擊此訊息則會回到團購商品的兩大分類選擇。'),(6,'操作類','如何加入購物車？','進入「團購商品/現購商品列表」後，選擇欲加入購物車的商品，點擊商品資訊框下方的 ”加入購物車”按鈕，依照流程填寫即可喔！'),(7,'操作類','什麼商品能加入購物車？','加入購物的商品須為兩大類中的現購商品呦～'),(8,'操作類','購物車最多能放幾個商品呢？','購物車最多能放5種商品，其商品數量不限喔！'),(9,'操作類','如何查看購物車？','1.進入「訂單/購物車查詢 / 購物車查詢」即可。\n2. 進入「團購商品/現購商品列表」點擊商品資訊框下方的 ”查看購物車”按鈕。'),(10,'操作類','如何修改購物車內的內容','進入「訂單/購物車查詢 / 購物車查詢」，可以進行商品的數量修改、移除商品名單。'),(11,'商品類','兩大類商品分為什麼？','分為現購商品、預購商品。\n1.現購商品是店內已有該商品庫存，下單即可前往營業地點取貨。\n2.預購商品是下單後要等待預購商品截止時團媽才會進行商品下訂，商品到店後會發送取貨通知，此類商品可以得到更優惠的價格，但需要等待。'),(12,'商品類','有哪些商品呢？','我們提供冷凍食品、日常用品、甜點、地方特產、主食、常溫食品、美妝保養、零食、保健食品、飲品，10種不同的商品類別呦～'),(13,'商品類','許願商品功能是什麼？','您可以利用這邊的功能提供有興趣的商品，團媽會看到呦！”有可能的話”會為大家爭取到更優惠的團購價格。'),(14,'訂單類','該怎麼建立訂單？','訂單有分為現購訂單、預購訂單、購物車訂單，\n1.前兩者需要先進入「團購商品/現購商品列表或預購商品列表」後，點擊商品資訊框下方的”立即購買”或”手刀預購”，接著跟著流程填寫就可以囉！\n2.購物車訂單則要先前往購物車，再點擊”送出購物車訂單”即可。');
/*!40000 ALTER TABLE `Questions_and_Answers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Statistical_Product`
--

DROP TABLE IF EXISTS `Statistical_Product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Statistical_Product` (
  `UID` int NOT NULL AUTO_INCREMENT,
  `年月` varchar(7) NOT NULL,
  `月成本_圖` text,
  `月利潤_圖` text,
  `月熱門商品_圖` text,
  `月成本_值` int DEFAULT NULL,
  `月利潤_值` int DEFAULT NULL,
  `年利潤_圖` text,
  `年成本_圖` text,
  PRIMARY KEY (`UID`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Statistical_Product`
--

LOCK TABLES `Statistical_Product` WRITE;
/*!40000 ALTER TABLE `Statistical_Product` DISABLE KEYS */;
INSERT INTO `Statistical_Product` VALUES (22,'2023-07','https://i.imgur.com/JvWc2Fn.jpg','https://i.imgur.com/SvhLNQZ.jpg','https://i.imgur.com/o85c7uO.jpg',4040,220,NULL,NULL),(23,'2023-08','https://i.imgur.com/QOgPekp.jpg','https://i.imgur.com/oOGgpRr.jpg','https://i.imgur.com/LPlECjT.jpg',5705,290,NULL,NULL),(24,'2023-99',NULL,NULL,NULL,NULL,NULL,'https://i.imgur.com/BQQN2sh.jpg','https://i.imgur.com/KBz3c7F.jpg');
/*!40000 ALTER TABLE `Statistical_Product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Statistics_Data`
--

DROP TABLE IF EXISTS `Statistics_Data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Statistics_Data` (
  `UID` int NOT NULL AUTO_INCREMENT,
  `年月` varchar(7) NOT NULL,
  `訂單編號` char(18) DEFAULT NULL,
  `商品ID` char(18) DEFAULT NULL,
  `商品名稱` char(50) DEFAULT NULL,
  `訂購數量` int DEFAULT NULL,
  `進貨單價` int DEFAULT NULL,
  `商品小計` int DEFAULT NULL,
  `建立時間` datetime NOT NULL,
  PRIMARY KEY (`UID`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Statistics_Data`
--

LOCK TABLES `Statistics_Data` WRITE;
/*!40000 ALTER TABLE `Statistics_Data` DISABLE KEYS */;
INSERT INTO `Statistics_Data` VALUES (9,'2023-07','order2023072300001','tests100006','奶奶酥餅',6,90,570,'2023-07-23 11:25:21'),(10,'2023-07','order2023072400001','tests100005','石二鍋佛跳牆湯包',2,320,650,'2023-07-24 15:27:11'),(11,'2023-07','order2023072400002','tests100007','新竹海哥芋頭鍋',5,150,800,'2023-07-24 10:55:47'),(12,'2023-07','order2023072700001','tests100006','奶奶酥餅',4,90,380,'2023-07-27 20:49:01'),(13,'2023-07','order2023072800001','tests100008','爭鮮甘栗子',4,140,600,'2023-07-30 10:49:35'),(14,'2023-07','order2023073000001','tests100009','高麗菜水餃',7,170,1260,'2023-07-30 11:35:10'),(15,'2023-08','order2023080100001','tests100010','韭菜水餃',5,170,900,'2023-08-01 10:48:15'),(16,'2023-08','order2023080100002','tests100005','石二鍋佛跳牆湯包',4,320,1300,'2023-08-01 11:09:12'),(17,'2023-08','order2023080300001','tests100007','新竹海哥芋頭鍋',3,150,480,'2023-08-03 19:59:51'),(18,'2023-08','order2023080300002','tests100008','爭鮮甘栗子',10,140,1500,'2023-08-03 21:36:29'),(19,'2023-08','order2023080400001','tests100011','玉米筍',5,115,600,'2023-08-04 10:39:10'),(20,'2023-08','order2023080400002','tests100009','高麗菜水餃',2,170,360,'2023-08-04 14:15:20'),(21,'2023-08','order2023080600001','tests100006','奶奶酥餅',9,90,855,'2023-08-06 15:20:05'),(22,'2023-08','order2023080700001','tests100006','奶奶酥餅',3,90,285,'2023-08-07 18:22:05');
/*!40000 ALTER TABLE `Statistics_Data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `member_profile`
--

DROP TABLE IF EXISTS `member_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member_profile` (
  `會員_LINE_ID` char(33) NOT NULL,
  `會員信賴度_取貨率退貨率` float DEFAULT NULL,
  `加入時間` datetime NOT NULL,
  `身分別` char(3) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`會員_LINE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member_profile`
--

LOCK TABLES `member_profile` WRITE;
/*!40000 ALTER TABLE `member_profile` DISABLE KEYS */;
INSERT INTO `member_profile` VALUES ('U2ec5ee75f06ce4b8efde7604655b194e',0.8,'2023-07-27 14:06:04','消費者'),('U3d7c25d64f92dbd3e413f9d238055bbb',0.8,'2023-08-02 09:19:32','消費者'),('U663bc4730a60ec2af8b25cc7d167b0dd',NULL,'2023-06-29 15:35:00','管理者'),('U829bc8925a60ec2cf8b25aa7d167b0cc',0.8,'2023-07-24 13:25:13','消費者'),('U829bc9000a60ec2af8b25aa7d167b0dd',0.85,'2023-06-30 10:30:03','消費者'),('Uc52aef2ae05ee1c9356ba20ea470947b',0.8,'2023-07-24 15:20:23','消費者'),('Uc889c85fdfd36d82a427672383a73572',0.8,'2023-08-01 14:22:09','消費者'),('Ucbff1a4f64c00c0a1d7a1611c1bf739a',0.8,'2023-11-19 14:43:20','消費者'),('Ud816833e08a750c6f70900f0c0bb0790',0.8,'2023-11-25 20:13:12','消費者'),('Uef6bbcc0906316aea2debe5d43020602',0.8,'2023-09-30 09:41:52','消費者');
/*!40000 ALTER TABLE `member_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_details`
--

DROP TABLE IF EXISTS `order_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_details` (
  `UID` int NOT NULL AUTO_INCREMENT,
  `訂單編號` char(18) NOT NULL,
  `商品ID` char(18) NOT NULL,
  `訂購數量` int NOT NULL,
  `商品小計` int NOT NULL,
  PRIMARY KEY (`UID`),
  KEY `訂單編號` (`訂單編號`),
  KEY `商品ID` (`商品ID`),
  CONSTRAINT `order_details_ibfk_1` FOREIGN KEY (`訂單編號`) REFERENCES `Order_information` (`訂單編號`),
  CONSTRAINT `order_details_ibfk_2` FOREIGN KEY (`商品ID`) REFERENCES `Product_information` (`商品ID`)
) ENGINE=InnoDB AUTO_INCREMENT=313 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_details`
--

LOCK TABLES `order_details` WRITE;
/*!40000 ALTER TABLE `order_details` DISABLE KEYS */;
INSERT INTO `order_details` VALUES (2,'order2023072500001','drinks000001',1,55),(3,'order2023072500001','dessert000001',3,660),(4,'order2023072500002','drinks000001',1,55),(5,'order2023072500002','dessert000001',3,660),(6,'order2023072500003','frozen000005',1,265),(7,'order2023072500003','drinks000003',2,70),(23,'order2023072600001','frozen000005',1,265),(24,'order2023072600001','frozen000005',2,260),(25,'order2023072600002','staplefood000002',1,105),(26,'order2023072600002','frozen000005',2,260),(27,'order2023072600003','staplefood000002',1,105),(28,'order2023072600003','frozen000005',2,260),(29,'order2023072600004','staplefood000002',1,105),(30,'order2023072600004','frozen000005',2,260),(31,'order2023072600006','dessert000001',3,660),(32,'order2023072600007','drinks000001',2,55),(33,'order2023072700001','dessert000001',3,660),(34,'order2023072700002','staplefood000001',6,100),(35,'order2023072700003','frozen000004',10,80),(37,'order2023072800001','dessert000001',3,660),(38,'order2023072800002','staplefood000002',1,105),(39,'order2023072800003','dessert000001',3,660),(40,'order2023072800004','dessert000001',3,660),(41,'order2023072800005','dessert000001',3,660),(42,'order2023072800006','dessert000001',3,660),(43,'order2023072800007','dessert000001',3,660),(44,'order2023072800008','dessert000001',3,660),(45,'order2023072800009','dessert000001',3,660),(46,'order2023072800010','staplefood000001',1,105),(47,'order2023072800011','staplefood000002',1,105),(48,'order2023072800012','drinks000004',1,70),(49,'order2023072800013','drinks000003',3,210),(50,'order2023080100001','staplefood000001',1,105),(51,'order2023080100002','drinks000001',2,110),(59,'order2023080400001','dessert000001',10,2200),(60,'cart20230727000001','dessert000001',2,420),(78,'order2023080600001','drinks000001',2,110),(96,'order2023080700001','dessert000001',1,220),(98,'order2023080800001','staplefood000001',1,105),(100,'order2023080800001','dessert000001',7,1540),(101,'order2023080800001','staplefood000002',5,500),(104,'order2023080800001','staplefood000002',1,55),(105,'order2023080800001','staplefood000002',1,55),(106,'order2023080800002','dessert000001',4,880),(107,'order2023080800003','dessert000001',2,440),(108,'order2023080800003','staplefood000001',3,300),(116,'order2023081000002','dessert000001',2,440),(117,'order2023080300001','frozen000004',1,80),(118,'order2023081000001','frozen000005',12,3120),(119,'order2023081000002','staplefood000001',3,300),(123,'order2023081100001','staplefood000002',1,105),(124,'order2023081100002','staplefood000002',1,105),(125,'order2023081100003','drinks000002',1,55),(126,'order2023081100004','staplefood000002',1,105),(127,'order2023081100005','staplefood000002',2,200),(129,'order2023081100006','frozen000002',3,510),(130,'order2023081100007','staplefood000002',1,105),(131,'order2023081100008','frozen000001',10,1700),(136,'order2023081900001','dessert000001',1,220),(138,'order2023082100003','dessert000001',1,220),(139,'order2023082100001','staplefood000002',1,105),(140,'order2023082100002','drinks000001',4,220),(141,'order2023082100003','staplefood000001',1,105),(144,'order2023082200001','frozen000004',1,80),(145,'order2023082200002','staplefood000002',1,105),(146,'order2023082200003','frozen000002',2,340),(147,'order2023082200004','frozen000005',3,780),(148,'order2023082200005','frozen000005',2,520),(150,'order2023082400001','frozen000003',2,340),(151,'order2023082400002','dessert000001',3,660),(152,'order2023082400003','drinks000001',6,330),(153,'order2023082500001','staplefood000002',1,105),(155,'order2023082500002','dessert000001',3,660),(156,'order2023082600001','dessert000001',3,660),(157,'order2023082600002','dessert000001',3,660),(158,'order2023082600003','drinks000003',3,210),(159,'order2023082600004','staplefood000002',1,105),(160,'order2023082600005','frozen000004',1,80),(162,'order2023092200001','staplefood000002',2,200),(171,'order2023083000001','dessert000001',2,440),(175,'order2023090600001','dessert000001',2,440),(176,'order2023091200001','staplefood000001',1,105),(178,'order2023092000003','dessert000001',1,220),(179,'order2023092000001','staplefood000002',1,105),(180,'order2023092000002','drinks000005',1,70),(181,'order2023092000003','staplefood000001',1,105),(182,'order2023092100001','staplefood000001',1,105),(183,'order2023092100001','staplefood000002',1,105),(184,'order2023092100002','dessert000001',1,220),(185,'order2023092100002','staplefood000001',1,105),(186,'order2023092100003','dessert000001',1,220),(187,'order2023092100003','staplefood000001',1,105),(188,'order2023092100004','dessert000001',1,220),(189,'order2023092100004','staplefood000001',1,105),(190,'order2023092100005','dessert000001',1,220),(191,'order2023092100005','staplefood000001',1,105),(192,'order2023092100006','dessert000001',1,220),(193,'order2023092100006','staplefood000001',1,105),(194,'order2023092100007','staplefood000001',2,200),(198,'order2023092500001','drinks000001',4,220),(210,'order2023093000001','dessert000001',1,220),(211,'order2023093000002','frozen000005',3,780),(212,'order2023093000003','staplefood000001',1,105),(214,'order2023093000004','dessert000001',2,440),(215,'order2023093000005','drinks000004',1,70),(216,'order2023100700001','drinks000001',4,220),(217,'order2023100700002','staplefood000001',5,500),(218,'order2023101100001','frozen000003',3,510),(219,'order2023101100002','frozen000005',1,265),(220,'order2023101100003','drinks000002',1,55),(223,'order2023102300001','test00010',2,60),(224,'order2023102300002','test00010',5,150),(227,'order2023102500001','dessert000001',11,2420),(228,'order2023102500002','test000007',2,90),(229,'order2023102500002','dessert000001',2,440),(233,'order2023102600001','dessert000001',1,220),(239,'order2023111000001','test00010',1,30),(240,'order2023111000002','test00010',6,180),(241,'order2023111000003','test00009',4,160),(242,'order2023111000004','test00009',5,200),(245,'order2023111500001','test00002',1,20),(248,'order2023112000001','staplefood000002',4,400),(249,'order2023112000002','staplefood000002',5,500),(254,'order2023112400001','drinks000001',1,55),(256,'order2023112500001','drinks000001',2,110),(260,'order2023112500002','frozen000025',2,330),(261,'order2023112500003','frozen000021',1,75),(262,'order2023112900001','dessert000001',3,630),(263,'order2023113000001','frozen000024',2,330),(264,'order2023120200001','frozen000001',2,340),(265,'order2023120200002','frozen000005',1,265),(266,'order2023120200005','frozen000021',1,75),(267,'order2023120200006','frozen000021',3,225),(268,'order2023120200006','frozen000022',1,95),(269,'order2023120200007','dessert000004',4,1240),(270,'order2023120200008','dessert000001',3,630),(271,'order2023120200009','drinks000001',3,165),(272,'order2023120200010','dessert000001',3,630),(273,'order2023120200011','frozen000001',1,175),(274,'order2023120200012','dessert000003',2,500),(275,'order2023120200013','test00010',10,300),(276,'order2023120600001','frozen000021',1,75),(277,'order2023120600001','frozen000023',2,330),(278,'order2023120300001','snack000001',100,14000),(279,'order2023120500001','frozen000001',1,175),(280,'order2023120600001','frozen000027',2,330),(281,'order2023120600002','snack000001',5,700),(282,'order2023120600003','frozen000021',4,300),(283,'order2023121000001','frozen000001',3,510),(284,'order2023121000002','frozen000001',2,340),(286,'order2023121200001','frozen000001',1,175),(296,'order2023121400001','dessert000003',1,250),(297,'order2023121400002','dessert000003',1,250),(299,'order2023121400003','frozen000021',5,375),(303,'cart20230724000001','frozen000002',1,175),(305,'order2023121400004','frozen000021',1,75),(306,'order2023121400005','frozen000021',2,150),(307,'order2023121400006','frozen000021',1,75),(308,'order2023121500001','dessert000001',1,220),(309,'order2023121500002','frozen000001',1,175),(310,'order2023121500003','dessert000001',2,420),(311,'order2023121500004','dessert000001',1,220),(312,'order2023121500005','frozen000001',2,344);
/*!40000 ALTER TABLE `order_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wishlist`
--

DROP TABLE IF EXISTS `wishlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wishlist` (
  `UID` int NOT NULL AUTO_INCREMENT,
  `商品名稱` char(15) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `商品圖片` text,
  `推薦原因` char(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `願望建立時間` datetime NOT NULL,
  `會員_LINE_ID` char(33) NOT NULL,
  `資料來源` text,
  PRIMARY KEY (`UID`),
  KEY `會員_LINE_ID` (`會員_LINE_ID`),
  CONSTRAINT `wishlist_ibfk_1` FOREIGN KEY (`會員_LINE_ID`) REFERENCES `member_profile` (`會員_LINE_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wishlist`
--

LOCK TABLES `wishlist` WRITE;
/*!40000 ALTER TABLE `wishlist` DISABLE KEYS */;
INSERT INTO `wishlist` VALUES (1,'宜蘭三星蔥',NULL,'想要吃到健康不嗆辣的蔥','2023-07-01 18:00:04','U829bc9000a60ec2af8b25aa7d167b0dd',NULL),(2,'宜蘭鴨賞',NULL,'想要吃到健康水嫩的鴨賞','2023-07-02 08:56:01','U829bc9000a60ec2af8b25aa7d167b0dd',NULL),(3,'素肉','https://i.imgur.com/t320FY3.jpg','網路上看到所以想提供看看','2023-08-14 00:00:00','U829bc8925a60ec2cf8b25aa7d167b0cc','網路上'),(4,'宜蘭香菇','https://i.imgur.com/s9lN4UJ.jpg','想要煮香菇雞湯希望團媽能夠上架這個商品','2023-08-14 15:28:17','U829bc8925a60ec2cf8b25aa7d167b0cc','網路上'),(5,'魚蛋','https://i.imgur.com/PVYmDpv.jpg','前陣子吃了魚蛋，但現在好像不太便宜希望團媽能夠尋得價格可以又新鮮的~','2023-08-15 10:28:29','U829bc8925a60ec2cf8b25aa7d167b0cc','前陣子吃的'),(10,'礁溪伴手禮-可可德歐','https://i.imgur.com/foXN7PS.jpg','想買來送禮','2023-08-23 11:34:19','U829bc8925a60ec2cf8b25aa7d167b0cc','https://www.welcometw.com/%E5%AE%9C%E8%98%AD%E5%90%8D%E7%94%A2-%E6%8E%A8%E8%96%A6%E5%BF%85%E8%B2%B720%E9%96%93%E5%AE%9C%E8%98%AD%E4%BC%B4%E6%89%8B%E7%A6%AE%EF%BC%8C%E9%80%81%E7%A6%AE%E5%A4%A7%E6%96%B9%E5%8F%88%E5%A5%BD/'),(21,'日式巧克力奶凍','https://i.imgur.com/eZF05T0.jpg','搭配下午茶最佳的甜點~想吃','2023-11-25 21:10:37','U829bc8925a60ec2cf8b25aa7d167b0cc','https://shop.cakenobel.com.tw/Product/ProductDetail?type=0002&subtype=00001&id=0101111');
/*!40000 ALTER TABLE `wishlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `商品`
--

DROP TABLE IF EXISTS `商品`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `商品` (
  `商品ID` varchar(45) NOT NULL,
  `商品名稱` varchar(45) NOT NULL,
  `廠商編號` varchar(45) DEFAULT NULL,
  `廠商商品序號` varchar(45) DEFAULT NULL,
  `庫存數量` int NOT NULL DEFAULT '0',
  `商品狀態` varchar(45) NOT NULL,
  `進貨單價` int NOT NULL,
  `單件售價` int NOT NULL,
  PRIMARY KEY (`商品ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='現貨/退貨';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `商品`
--

LOCK TABLES `商品` WRITE;
/*!40000 ALTER TABLE `商品` DISABLE KEYS */;
/*!40000 ALTER TABLE `商品` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `會員資料`
--

DROP TABLE IF EXISTS `會員資料`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `會員資料` (
  `會員LINEID` varchar(45) NOT NULL,
  `會員名稱` varchar(45) NOT NULL,
  `電話` varchar(45) DEFAULT NULL,
  `會員信賴度` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`會員LINEID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `會員資料`
--

LOCK TABLES `會員資料` WRITE;
/*!40000 ALTER TABLE `會員資料` DISABLE KEYS */;
INSERT INTO `會員資料` VALUES ('U663cc','林瑞','0952168834',1),('U663gg','小源','0978215471',1);
/*!40000 ALTER TABLE `會員資料` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `訂單資訊`
--

DROP TABLE IF EXISTS `訂單資訊`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `訂單資訊` (
  `訂單編號` int NOT NULL AUTO_INCREMENT,
  `會員lineID` varchar(45) NOT NULL,
  `下訂時間` datetime NOT NULL,
  `取貨完成時間` datetime DEFAULT NULL,
  `訂單狀態` varchar(45) NOT NULL,
  PRIMARY KEY (`訂單編號`)
) ENGINE=InnoDB AUTO_INCREMENT=332 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='未取/已取';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `訂單資訊`
--

LOCK TABLES `訂單資訊` WRITE;
/*!40000 ALTER TABLE `訂單資訊` DISABLE KEYS */;
INSERT INTO `訂單資訊` VALUES (4,'134865795','2023-07-22 00:00:00',NULL,'-1'),(12,'415346824','2023-07-20 00:00:00',NULL,'0'),(297,'134865795','2023-07-21 00:08:00','2023-07-23 00:00:00','1'),(331,'348642156','2023-07-21 00:10:00',NULL,'-1');
/*!40000 ALTER TABLE `訂單資訊` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `購物車資訊`
--

DROP TABLE IF EXISTS `購物車資訊`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `購物車資訊` (
  `UID` int NOT NULL AUTO_INCREMENT,
  `會員LINEID` varchar(45) NOT NULL,
  `商品ID` varchar(45) NOT NULL,
  `商品數量` int NOT NULL,
  `商品總額` int NOT NULL,
  PRIMARY KEY (`UID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `購物車資訊`
--

LOCK TABLES `購物車資訊` WRITE;
/*!40000 ALTER TABLE `購物車資訊` DISABLE KEYS */;
/*!40000 ALTER TABLE `購物車資訊` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-19 10:59:45
