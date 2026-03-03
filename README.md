/*
 Navicat Premium Data Transfer

 Source Server         : carrental
 Source Server Type    : MySQL
 Source Server Version : 80045 (8.0.45)
 Source Host           : localhost:3306
 Source Schema         : car_rental_system

 Target Server Type    : MySQL
 Target Server Version : 80045 (8.0.45)
 File Encoding         : 65001

 Date: 02/03/2026 21:13:51
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for cars
-- ----------------------------
DROP TABLE IF EXISTS `cars`;
CREATE TABLE `cars`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` enum('pending','approved','rejected','Available','Rented','Maintenance') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'pending',
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `owner_id` int NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `rating` float NULL DEFAULT 5,
  `discount` int NULL DEFAULT 0,
  `price` int NULL DEFAULT 0,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 123 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cars
-- ----------------------------
INSERT INTO `cars` VALUES (102, 'Honda Civic Type R', 'Available', 'Honda_Civic_Type_R_.jpg', NULL, '2026-02-01 16:23:37', 4, 10, 200000, '5 chỗ, số tự động, máy xăng, ship tận nơi\r\nLiên hệ: 0123456789');
INSERT INTO `cars` VALUES (103, 'Ford Mustang Fastback', 'Available', 'Ford_Mustang_Fastback.jpg', NULL, '2026-02-01 16:23:37', 4, 5, 300000, 'Xe cơ bắp Mỹ, 4 chỗ (2+2), số tự động 10 cấp, động cơ V8 mạnh mẽ, nội thất da cao cấp, thích hợp đi sự kiện hoặc trải nghiệm tốc độ.\r\nLiên hệ: 0987654321');
INSERT INTO `cars` VALUES (104, 'BMW M3', 'Available', 'BMW_M3.jpg', NULL, '2026-02-01 16:23:37', 5, 2, 400000, '5 chỗ, số tự động 8 cấp M Steptronic, động cơ 3.0L TwinPower Turbo (510 HP), dẫn động 4 bánh xDrive linh hoạt, nội thất carbon, màn hình cong cực đại, phong cách thể thao đầy uy lực.\r\nLiên hệ: 0378917491');
INSERT INTO `cars` VALUES (105, 'Audi A4', 'Rented', 'Audi_A4.jpg', NULL, '2026-02-01 16:23:37', 5, 4, 1000000, 'Xe sang nhập khẩu Đức, nội thất bọc da cao cấp, hệ thống đèn LED đặc trưng của Audi. Cảm giác lái đầm chắc, cách âm cực tốt, phù hợp đi gặp đối tác hoặc dự sự kiện sang trọng.\r\nLiên hệ: 092837451');
INSERT INTO `cars` VALUES (106, 'Jeep Compass', 'Available', 'Jeep_Compass.jpg', NULL, '2026-02-01 16:23:37', 5, 5, 600000, 'SUV đậm chất Mỹ, dẫn động 4 bánh toàn thời gian (4x4), nội thất da cao cấp, hệ thống giải trí Uconnect 5 hiện đại. Xe cứng cáp, phong cách off-road nhẹ nhàng, phù hợp cho những chuyến đi dã ngoại hoặc chụp ảnh ngoại cảnh độc đáo.\r\nLiên hệ: 082374192');
INSERT INTO `cars` VALUES (107, 'Mercedes-Benz E-Class', 'Available', 'Mercedes-Benz_E-Class.jpg', NULL, '2026-02-01 16:23:37', 4, 5, 900000, 'Đỉnh cao sang trọng với gói nội thất AMG, cửa sổ trời toàn cảnh Panorama, hệ thống loa Burmester cực đỉnh. Đèn Multibeam LED thông minh, hỗ trợ lái an toàn, không gian hàng ghế sau rộng rãi, lịch lãm.\r\nLiên hệ: 077283914');
INSERT INTO `cars` VALUES (108, 'Volkswagen Passat R-Line', 'Rented', 'Volkswagen_Passat_R-Line.jpg', NULL, '2026-02-01 16:23:37', 4, 5, 600000, 'Sedan hạng D chuẩn Đức, gói ngoại thất R-Line thể thao, động cơ TSI mạnh mẽ, nội thất bọc da Nappa cao cấp. Ghế massage cho người lái, điều hòa 3 vùng độc lập, cách âm cực tốt, mang lại trải nghiệm êm ái trên mọi hành trình.\r\nliên hệ: 033948219');
INSERT INTO `cars` VALUES (109, 'Kia Stinger GT', 'Available', 'Kia_Stinger_GT.jpg', NULL, '2026-02-01 16:23:37', 4, 5, 1000000, 'Sedan thể thao kiểu dáng Fastback độc đáo, động cơ V6 mạnh mẽ 365 mã lực, tăng tốc từ 0-100km/h chỉ trong 4.9 giây. Nội thất da Nappa đỏ cá tính, hệ thống âm thanh Harman Kardon 15 loa, cửa sổ trời, mang lại cảm giác lái phấn khích như siêu xe.\r\nLiên hệ: 082731892');
INSERT INTO `cars` VALUES (110, 'Lexus RX 500h F Sport', 'Rented', 'Lexus_RX_500h_F_Sport.jpg', NULL, '2026-02-01 16:23:37', 5, 5, 1200000, 'SUV hạng sang đỉnh cao, động cơ Hybrid 2.4L Turbo mạnh mẽ (366 mã lực), dẫn động 4 bánh DIRECT4. Gói ngoại thất F Sport thể thao, nội thất da Alcantara cao cấp, âm thanh Mark Levinson 21 loa, màn hình 14 inch, vận hành cực kỳ yên tĩnh và sang trọng.\r\nLiên hệ: 029948819');
INSERT INTO `cars` VALUES (111, 'Nissan Altima SR Midnight Edition', 'Rented', 'Nissan_Altima_SR_Midnight_Edition.jpg', NULL, '2026-02-01 16:23:37', 3, 7, 300000, 'Phiên bản Midnight Edition độc đáo với lưới tản nhiệt V-Motion đen bóng, la-zăng 19 inch đen và cánh lướt gió thể thao. Nội thất hiện đại với ghế bọc da chỉnh điện, hỗ trợ Apple CarPlay/Android Auto. Xe vận hành êm ái, tiết kiệm nhiên liệu, lý tưởng cho cả đi phố và đi tỉnh.\r\nLiên hệ: 0926738182');
INSERT INTO `cars` VALUES (112, 'Dodge Charger Scat Pack Widebody', 'Rented', 'Dodge_Charger_Scat_Pack_Widebody.jpg', NULL, '2026-02-01 16:23:37', 4, 15, 700000, 'Quái thú\" sedan 4 cửa mạnh nhất phân khúc với gói thân rộng (Widebody) hầm hố. Động cơ V8 6.4L HEMI sản sinh 485 mã lực, âm thanh ống xả uy lực đặc trưng. Trang bị phanh Brembo 6 piston, lốp bản rộng bám đường cực tốt, nội thất thể thao với ghế bọc da Alcantara cao cấp.\r\nLiên hệ: 0928335971');
INSERT INTO `cars` VALUES (113, 'Subaru WRX STI', 'Rented', 'Subaru_WRX_STI.jpg', NULL, '2026-02-01 16:23:37', 4, 10, 400000, 'Động cơ Boxer 2.5L tăng áp, hộp số sàn 6 cấp cho cảm giác lái cực bốc. Cánh gió sau cỡ lớn đặc trưng, phanh Brembo hiệu năng cao và ghế thể thao Recaro ôm sát người lái.\r\nLiên hệ: 089283174');
INSERT INTO `cars` VALUES (114, 'Porsche Panamera 4 E-Hybrid', 'Rented', 'Porsche_Panamera_4_E-Hybrid.jpg', NULL, '2026-02-01 16:23:37', 5, 10, 700000, 'tổng công suất 470 mã lực. Hệ thống treo khí nén chủ động giúp xe vận hành cực kỳ êm ái. Nội thất sang trọng với màn hình cho ghế phụ, âm thanh vòm Bose/Burmester, cửa sổ trời toàn cảnh\r\nLiên hệ: 0789271826');
INSERT INTO `cars` VALUES (115, 'Volvo S90 Inscription', 'Available', 'Volvo_S90_Inscription.jpg', NULL, '2026-02-01 16:23:37', 3, 7, 500000, 'Nội thất da Nappa, ốp gỗ tự nhiên, cần số pha lê Orrefors chế tác thủ công. Hệ thống âm thanh Bowers & Wilkins 19 loa đỉnh cao, hỗ trợ lái Pilot Assist và hệ thống lọc không khí sạch\r\nLiên hệ: 0123459876');
INSERT INTO `cars` VALUES (116, 'Tavera', 'Available', 'Tavera.jpg', NULL, '2026-02-01 16:23:37', 5, 20, 400000, 'Dòng xe MUV đa dụng siêu bền bỉ, không gian nội thất cực rộng với cấu hình lên tới 9 chỗ ngồi. Động cơ Diesel tiết kiệm, khung gầm chắc chắn, điều hòa mát sâu cho tất cả các hàng ghế. Lựa chọn kinh tế nhất cho các chuyến đi đông người, dã ngoại hoặc chở đồ cồng kềnh.\r\nLiên hệ: 0905879312');

-- ----------------------------
-- Table structure for favorites
-- ----------------------------
DROP TABLE IF EXISTS `favorites`;
CREATE TABLE `favorites`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NULL DEFAULT NULL,
  `car_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `car_id`(`car_id` ASC) USING BTREE,
  CONSTRAINT `favorites_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `favorites_ibfk_2` FOREIGN KEY (`car_id`) REFERENCES `cars` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of favorites
-- ----------------------------
INSERT INTO `favorites` VALUES (4, 2, 103);

-- ----------------------------
-- Table structure for rentals
-- ----------------------------
DROP TABLE IF EXISTS `rentals`;
CREATE TABLE `rentals`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `car_id` int NOT NULL,
  `start_date` date NULL DEFAULT NULL,
  `end_date` date NULL DEFAULT NULL,
  `total_price` int NULL DEFAULT NULL,
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `car_id`(`car_id` ASC) USING BTREE,
  CONSTRAINT `rentals_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `rentals_ibfk_2` FOREIGN KEY (`car_id`) REFERENCES `cars` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of rentals
-- ----------------------------

-- ----------------------------
-- Table structure for user_documents
-- ----------------------------
DROP TABLE IF EXISTS `user_documents`;
CREATE TABLE `user_documents`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NULL DEFAULT NULL,
  `cccd_img` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `license_img` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `cavet_img` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `status` enum('pending','approved','rejected') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'pending',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_documents
-- ----------------------------
INSERT INTO `user_documents` VALUES (1, 2, 'CCCD.jpg', 'BangLaiXe.jpg', 'caVet.jpg', 'pending');
INSERT INTO `user_documents` VALUES (2, 2, 'CCCD.jpg', 'BangLaiXe.jpg', 'caVet.jpg', 'pending');
INSERT INTO `user_documents` VALUES (3, 2, 'CCCD.jpg', 'BangLaiXe.jpg', 'caVet.jpg', 'pending');
INSERT INTO `user_documents` VALUES (4, 1, 'CCCD.jpg', 'BangLaiXe.jpg', 'caVet.jpg', 'pending');
INSERT INTO `user_documents` VALUES (5, 2, 'CCCD.jpg', 'BangLaiXe.jpg', 'caVet.jpg', 'pending');
INSERT INTO `user_documents` VALUES (6, 2, 'CCCD.jpg', 'BangLaiXe.jpg', 'caVet.jpg', 'pending');
INSERT INTO `user_documents` VALUES (7, 2, 'CCCD.jpg', 'BangLaiXe.jpg', 'caVet.jpg', 'pending');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'user',
  `full_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'admin', 'adamin', 'admin', NULL, NULL, NULL, NULL);
INSERT INTO `users` VALUES (2, 'nhanTest', '123', 'user', 'Tran Phuoc Nhan', 'test@gmail.com', '123456789', NULL);

SET FOREIGN_KEY_CHECKS = 1;
