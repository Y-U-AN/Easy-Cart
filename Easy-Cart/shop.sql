/*
 Navicat Premium Data Transfer

 Source Server         : 1
 Source Server Type    : MySQL
 Source Server Version : 80035 (8.0.35)
 Source Host           : localhost:3306
 Source Schema         : shop

 Target Server Type    : MySQL
 Target Server Version : 80035 (8.0.35)
 File Encoding         : 65001

 Date: 15/03/2024 20:18:11
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for cart
-- ----------------------------
DROP TABLE IF EXISTS `cart`;
CREATE TABLE `cart`  (
  `cart_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL DEFAULT 1,
  `added_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`cart_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cart
-- ----------------------------
INSERT INTO `cart` VALUES (5, 1, 2, 2, '2024-02-21 13:00:06');

-- ----------------------------
-- Table structure for comments
-- ----------------------------
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments`  (
  `comment_id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `order_id` int NOT NULL,
  `user_id` int NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`comment_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of comments
-- ----------------------------
INSERT INTO `comments` VALUES (1, 1, 1, 4, '1', '2024-02-16 17:58:51');
INSERT INTO `comments` VALUES (2, 4, 2, 4, '32', '2024-02-16 17:59:15');
INSERT INTO `comments` VALUES (3, 3, 11, 11, 'The performance of this one is excellent', '2024-02-22 11:03:34');
INSERT INTO `comments` VALUES (4, 9, 12, 11, 'Buying the Millennium Falcon was a fantastic choice: fast, full of character, a bit old but extremely reliable.', '2024-02-24 10:52:19');
INSERT INTO `comments` VALUES (5, 8, 14, 11, 'balabalabala', '2024-02-24 11:13:11');
INSERT INTO `comments` VALUES (6, 2, 15, 9, 'balabalabala', '2024-02-26 12:19:11');

-- ----------------------------
-- Table structure for orders
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders`  (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NULL DEFAULT NULL,
  `product_id` int NULL DEFAULT NULL,
  `quantity` int NULL DEFAULT NULL,
  `unit_price` decimal(10, 2) NULL DEFAULT NULL,
  `total_price` decimal(10, 2) NULL DEFAULT NULL,
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`order_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of orders
-- ----------------------------
INSERT INTO `orders` VALUES (1, 4, 1, 2, 499.99, 999.98, 'pending', '2024-02-16 13:11:07');
INSERT INTO `orders` VALUES (2, 4, 4, 4, 599.99, 2159.96, 'pending', '2024-02-16 16:30:16');
INSERT INTO `orders` VALUES (3, 4, 2, 5, 349.99, 1749.95, 'pending', '2024-02-18 10:34:24');
INSERT INTO `orders` VALUES (4, 4, 2, 5, 349.99, 1749.95, 'pending', '2024-02-18 10:37:24');
INSERT INTO `orders` VALUES (5, 4, 2, 6, 349.99, 2099.94, 'pending', '2024-02-21 12:46:46');
INSERT INTO `orders` VALUES (6, 4, 2, 4, 349.99, 1259.96, 'pending', '2024-02-21 12:46:59');
INSERT INTO `orders` VALUES (7, 4, 2, 9, 349.99, 3149.91, 'pending', '2024-02-21 13:02:42');
INSERT INTO `orders` VALUES (8, 1, 2, 2, 349.99, 699.98, 'pending', '2024-02-21 13:00:10');
INSERT INTO `orders` VALUES (9, 1, 2, 2, 349.99, 699.98, 'pending', '2024-02-21 15:33:15');
INSERT INTO `orders` VALUES (10, 11, 2, 2, 349.99, 699.98, 'pending', '2024-02-22 11:02:43');
INSERT INTO `orders` VALUES (11, 11, 3, 1, 599.99, 539.99, 'pending', '2024-02-22 11:02:53');
INSERT INTO `orders` VALUES (12, 11, 9, 1, 99999999.00, 89999999.10, 'pending', '2024-02-24 10:49:55');
INSERT INTO `orders` VALUES (13, 11, 2, 2, 349.99, 699.98, 'pending', '2024-02-24 11:10:53');
INSERT INTO `orders` VALUES (14, 11, 8, 1, 999999.00, 999999.00, 'pending', '2024-02-24 11:12:11');
INSERT INTO `orders` VALUES (15, 9, 2, 2, 349.99, 699.98, 'pending', '2024-02-26 12:19:01');

-- ----------------------------
-- Table structure for products
-- ----------------------------
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `img_src` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `category` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `price` decimal(10, 2) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of products
-- ----------------------------
INSERT INTO `products` VALUES (2, 'https://static.dw.com/image/48200523_401.jpg', 'MINI PRO12', 'Advanced Performance in a Small Package.', 'Drones', 349.99);
INSERT INTO `products` VALUES (3, 'https://cdn.sputniknews.cn/img/102875/99/1028759979_0:257:4928:3029_1920x0_80_0_0_177f8d2ae74e808f7b194edec4edfbb5.jpg', 'MINI PRO13', 'Unleash Your Potential with the Ultimate Drone Experience.', 'Drones', 599.99);
INSERT INTO `products` VALUES (8, 'http://127.0.0.1:5000/static/YILONG.jpg', 'Pterodactyl drone', '', 'Drones', 999999.00);
INSERT INTO `products` VALUES (9, 'http://127.0.0.1:5000/static/OIP.jpg', 'Millennium Falcon', '', 'Airship', 99999999.00);
INSERT INTO `products` VALUES (10, 'http://127.0.0.1:5000/static/v2-8719fe831c9ca41c4bbbe2f083c36ce3_720w.webp', 'Flask', '', 'flask', 5.00);

-- ----------------------------
-- Table structure for user_chat_history
-- ----------------------------
DROP TABLE IF EXISTS `user_chat_history`;
CREATE TABLE `user_chat_history`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `chat_history` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_chat_history
-- ----------------------------
INSERT INTO `user_chat_history` VALUES (1, 4, '	Support: 额\nCustomer: 啊啊啊\nCustomer: e1\nCustomer: e1\nCustomer: e1\nSupport: 1\nSupport: 2\nSupport: e1\nCustomer: e1\nCustomer: e1\nCustomer: 额\nSupport: e1\nSupport: e1\nSupport: skdksdkks\nSupport: kkk\nSupport: 12\nSupport: e1\nSupport: e1\nSupport: e2', '2024-02-21 12:52:26');
INSERT INTO `user_chat_history` VALUES (2, 1, 'Customer: 你好', '2024-02-21 13:53:59');
INSERT INTO `user_chat_history` VALUES (3, 11, 'Customer: hi\nSupport: hi\nSupport: hi\nCustomer: hello\nCustomer: hello', '2024-02-26 12:17:06');
INSERT INTO `user_chat_history` VALUES (4, 9, 'Customer: hi', '2024-02-26 12:18:12');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `region` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `is_singer` tinyint(1) NULL DEFAULT NULL,
  `role` enum('user','admin') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'user',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `email`(`email` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'example@example.com', '123456', 'John DoeES', 'US', NULL, 1, 'admin');
INSERT INTO `users` VALUES (2, 'example2@example.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'EEhn Doe', 'US', '1234567890', 0, 'user');
INSERT INTO `users` VALUES (3, 'example@Eexample.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'DOE', 'US', '18829938182', 0, 'user');
INSERT INTO `users` VALUES (4, '888@qq.com', '123456', '8888', 'UK', NULL, 0, 'user');
INSERT INTO `users` VALUES (5, '632891@qq.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'UseD', 'US', '18293893821', 0, 'user');
INSERT INTO `users` VALUES (6, '623586617@qq.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'aaa', 'US', '18244210125', 0, 'user');
INSERT INTO `users` VALUES (7, '123456@qq.com', '12832183281', NULL, NULL, NULL, NULL, 'user');
INSERT INTO `users` VALUES (8, '1234256@qq.com', '12832183281', NULL, NULL, NULL, NULL, 'user');
INSERT INTO `users` VALUES (9, '183991@qq.com', '123456', NULL, NULL, NULL, NULL, 'user');
INSERT INTO `users` VALUES (10, '12939@qq.com', '123456', NULL, NULL, NULL, NULL, 'user');
INSERT INTO `users` VALUES (11, 'root@root.com', 'root', NULL, NULL, NULL, NULL, 'user');
INSERT INTO `users` VALUES (12, 'ccym078@gmail.com', '123', NULL, NULL, NULL, NULL, 'user');
INSERT INTO `users` VALUES (13, '1234567@gmail.com', '123456', NULL, NULL, NULL, NULL, 'user');
INSERT INTO `users` VALUES (14, 'presenation@Tonysmail.co.uk', '123456', NULL, NULL, NULL, NULL, 'user');

SET FOREIGN_KEY_CHECKS = 1;
