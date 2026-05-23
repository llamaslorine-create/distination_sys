/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80018 (8.0.18)
 Source Host           : localhost:3306
 Source Schema         : novel_sys

 Target Server Type    : MySQL
 Target Server Version : 80018 (8.0.18)
 File Encoding         : 65001

 Date: 06/05/2026 11:44:03
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin`  (
  `admin_id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_account` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `admin_password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `admin_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `role_id` int(11) NULL DEFAULT NULL,
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `status` smallint(6) NULL DEFAULT 1,
  PRIMARY KEY (`admin_id`) USING BTREE,
  UNIQUE INDEX `admin_account`(`admin_account` ASC) USING BTREE,
  INDEX `role_id`(`role_id` ASC) USING BTREE,
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES (1, 'admin', '$2b$12$EixZaYbB.rK4fl8x2q7Meu6Q6D2V5fF5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q', '系统管理员', 1, '2026-05-06 11:32:43', '2026-05-06 11:32:43', 1);

-- ----------------------------
-- Table structure for carousel
-- ----------------------------
DROP TABLE IF EXISTS `carousel`;
CREATE TABLE `carousel`  (
  `carousel_id` int(11) NOT NULL AUTO_INCREMENT,
  `carousel_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `novel_id` int(11) NULL DEFAULT NULL,
  `sort` int(11) NULL DEFAULT 0,
  `status` smallint(6) NULL DEFAULT 1,
  PRIMARY KEY (`carousel_id`) USING BTREE,
  INDEX `novel_id`(`novel_id` ASC) USING BTREE,
  CONSTRAINT `carousel_ibfk_1` FOREIGN KEY (`novel_id`) REFERENCES `novel` (`novel_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of carousel
-- ----------------------------
INSERT INTO `carousel` VALUES (1, 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=fantasy%20novel%20cover%20art%20with%20dragon%20and%20warrior&image_size=landscape_16_9', 1, 1, 1);
INSERT INTO `carousel` VALUES (2, 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=xianxia%20immortal%20cultivation%20novel%20cover%20with%20mountains&image_size=landscape_16_9', 2, 2, 1);
INSERT INTO `carousel` VALUES (3, 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=urban%20city%20night%20scene%20modern%20novel%20cover&image_size=landscape_16_9', 3, 3, 1);

-- ----------------------------
-- Table structure for category
-- ----------------------------
DROP TABLE IF EXISTS `category`;
CREATE TABLE `category`  (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `category_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `parent_id` int(11) NULL DEFAULT NULL,
  `sort` int(11) NULL DEFAULT 0,
  `status` smallint(6) NULL DEFAULT 1,
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`category_id`) USING BTREE,
  UNIQUE INDEX `category_name`(`category_name` ASC) USING BTREE,
  INDEX `idx_category_parent`(`parent_id` ASC) USING BTREE,
  CONSTRAINT `category_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `category` (`category_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of category
-- ----------------------------
INSERT INTO `category` VALUES (1, '玄幻', NULL, 1, 1, '2026-05-06 11:32:50', '2026-05-06 11:32:50');
INSERT INTO `category` VALUES (2, '仙侠', NULL, 2, 1, '2026-05-06 11:32:50', '2026-05-06 11:32:50');
INSERT INTO `category` VALUES (3, '都市', NULL, 3, 1, '2026-05-06 11:32:50', '2026-05-06 11:32:50');
INSERT INTO `category` VALUES (4, '历史', NULL, 4, 1, '2026-05-06 11:32:50', '2026-05-06 11:32:50');
INSERT INTO `category` VALUES (5, '科幻', NULL, 5, 1, '2026-05-06 11:32:50', '2026-05-06 11:32:50');
INSERT INTO `category` VALUES (6, '悬疑', NULL, 6, 1, '2026-05-06 11:32:50', '2026-05-06 11:32:50');

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment`  (
  `comment_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `novel_id` int(11) NULL DEFAULT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `audit_status` smallint(6) NULL DEFAULT 0,
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`comment_id`) USING BTREE,
  INDEX `idx_comment_user`(`user_id` ASC) USING BTREE,
  INDEX `idx_comment_novel`(`novel_id` ASC) USING BTREE,
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`novel_id`) REFERENCES `novel` (`novel_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of comment
-- ----------------------------

-- ----------------------------
-- Table structure for novel
-- ----------------------------
DROP TABLE IF EXISTS `novel`;
CREATE TABLE `novel`  (
  `novel_id` int(11) NOT NULL AUTO_INCREMENT,
  `novel_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `author` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `category_id` int(11) NULL DEFAULT NULL,
  `cover_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `introduction` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `total_words` int(11) NULL DEFAULT 0,
  `original_data` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `status` smallint(6) NULL DEFAULT 1,
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`novel_id`) USING BTREE,
  INDEX `idx_novel_category`(`category_id` ASC) USING BTREE,
  CONSTRAINT `novel_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`category_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of novel
-- ----------------------------
INSERT INTO `novel` VALUES (1, '斗破苍穹', '天蚕土豆', 1, '/static/images/doupo.jpg', '天才少年萧炎因斗气尽失，遭未婚妻退婚，却意外获得神秘戒指，从此踏上逆袭之路...', 5200000, NULL, 1, '2026-05-06 11:32:57', '2026-05-06 11:32:57');
INSERT INTO `novel` VALUES (2, '凡人修仙传', '忘语', 2, '/static/images/fanren.jpg', '普通山村少年韩立，偶然进入当地江湖小门派，成了一名记名弟子，踏上修仙之路...', 7700000, NULL, 1, '2026-05-06 11:32:57', '2026-05-06 11:32:57');
INSERT INTO `novel` VALUES (3, '都市特种兵', '夜十三', 3, '/static/images/dushi.jpg', '特种兵王回归都市，掀起惊天波澜，保护美女总裁，纵横花都...', 2100000, NULL, 1, '2026-05-06 11:32:57', '2026-05-06 11:32:57');
INSERT INTO `novel` VALUES (4, '明朝那些事儿', '当年明月', 4, '/static/images/mingchao.jpg', '以史料为基础，以年代和具体人物为主线，全景式展现明朝两百多年的历史...', 1200000, NULL, 1, '2026-05-06 11:32:57', '2026-05-06 11:32:57');
INSERT INTO `novel` VALUES (5, '三体', '刘慈欣', 5, '/static/images/santi.jpg', '地球文明与三体文明的史诗级碰撞，人类文明在宇宙中的艰难生存...', 510000, NULL, 1, '2026-05-06 11:32:57', '2026-05-06 11:32:57');
INSERT INTO `novel` VALUES (6, '盗墓笔记', '南派三叔', 6, '/static/images/daomu.jpg', '吴邪、张起灵、王胖子三人的盗墓传奇，揭开古老神秘的地下世界...', 2200000, NULL, 1, '2026-05-06 11:32:57', '2026-05-06 11:32:57');

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role`  (
  `role_id` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `permissions` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `remark` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`role_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES (1, '超级管理员', 'all', '系统最高权限角色', '2026-05-06 11:32:38', '2026-05-06 11:32:38');

-- ----------------------------
-- Table structure for system_log
-- ----------------------------
DROP TABLE IF EXISTS `system_log`;
CREATE TABLE `system_log`  (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) NULL DEFAULT NULL,
  `operate_type` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `operate_content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `operate_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `ip_address` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`log_id`) USING BTREE,
  INDEX `idx_log_admin`(`admin_id` ASC) USING BTREE,
  INDEX `idx_log_time`(`operate_time` ASC) USING BTREE,
  CONSTRAINT `system_log_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`admin_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of system_log
-- ----------------------------

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `nickname` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `avatar_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `status` smallint(6) NULL DEFAULT 1,
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------

-- ----------------------------
-- Table structure for visual_config
-- ----------------------------
DROP TABLE IF EXISTS `visual_config`;
CREATE TABLE `visual_config`  (
  `config_id` int(11) NOT NULL AUTO_INCREMENT,
  `config_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `chart_type` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `data_dimension` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_ai_support` smallint(6) NULL DEFAULT 0,
  `status` smallint(6) NULL DEFAULT 1,
  `update_admin_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`config_id`) USING BTREE,
  UNIQUE INDEX `config_name`(`config_name` ASC) USING BTREE,
  INDEX `update_admin_id`(`update_admin_id` ASC) USING BTREE,
  CONSTRAINT `visual_config_ibfk_1` FOREIGN KEY (`update_admin_id`) REFERENCES `admin` (`admin_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of visual_config
-- ----------------------------
INSERT INTO `visual_config` VALUES (1, '小说分类分布', 'pie', 'category', 1, 1, 1);
INSERT INTO `visual_config` VALUES (2, '小说字数统计', 'bar', 'word_count', 0, 1, 1);
INSERT INTO `visual_config` VALUES (3, '评论数量趋势', 'line', 'comment_count', 0, 1, 1);
INSERT INTO `visual_config` VALUES (4, '用户活跃度', 'bar', 'user_activity', 1, 1, 1);

-- ----------------------------
-- View structure for comment_with_user
-- ----------------------------
DROP VIEW IF EXISTS `comment_with_user`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `comment_with_user` AS select `c`.`comment_id` AS `comment_id`,`c`.`user_id` AS `user_id`,`c`.`novel_id` AS `novel_id`,`c`.`content` AS `content`,`c`.`audit_status` AS `audit_status`,`c`.`create_time` AS `create_time`,`u`.`nickname` AS `nickname`,`u`.`avatar_url` AS `avatar_url` from (`comment` `c` left join `user` `u` on((`c`.`user_id` = `u`.`user_id`)));

-- ----------------------------
-- View structure for novel_with_category
-- ----------------------------
DROP VIEW IF EXISTS `novel_with_category`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `novel_with_category` AS select `n`.`novel_id` AS `novel_id`,`n`.`novel_name` AS `novel_name`,`n`.`author` AS `author`,`n`.`category_id` AS `category_id`,`n`.`cover_url` AS `cover_url`,`n`.`introduction` AS `introduction`,`n`.`total_words` AS `total_words`,`n`.`original_data` AS `original_data`,`n`.`status` AS `status`,`n`.`create_time` AS `create_time`,`n`.`update_time` AS `update_time`,`c`.`category_name` AS `category_name` from (`novel` `n` left join `category` `c` on((`n`.`category_id` = `c`.`category_id`)));

-- ----------------------------
-- Table structure for checkin_spot
-- ----------------------------
DROP TABLE IF EXISTS `checkin_spot`;
CREATE TABLE `checkin_spot`  (
  `spot_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `category` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `image_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `rating` double NULL DEFAULT 0,
  `checkin_count` int(11) NULL DEFAULT 0,
  `status` smallint(6) NULL DEFAULT 1,
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`spot_id`) USING BTREE,
  INDEX `idx_category`(`category` ASC) USING BTREE,
  INDEX `idx_status`(`status` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of checkin_spot
-- ----------------------------
INSERT INTO `checkin_spot` VALUES (1, '星巴克臻选', '北京市朝阳区三里屯太古里南区', 39.9396, 116.4458, '咖啡馆', '位于三里屯核心商圈的星巴克臻选店，环境优雅，适合打卡拍照', NULL, 4.8, 1256, 1, '2026-05-13 10:00:00', '2026-05-13 10:00:00');
INSERT INTO `checkin_spot` VALUES (2, 'page one书店', '北京市西城区西单北大街120号', 39.9142, 116.3763, '书店', '集阅读、咖啡、文创于一体的综合性书店', NULL, 4.9, 892, 1, '2026-05-13 10:00:00', '2026-05-13 10:00:00');
INSERT INTO `checkin_spot` VALUES (3, '红砖美术馆', '北京市朝阳区崔各庄乡', 39.9908, 116.5122, '美术馆', '以红砖为建筑特色的现代美术馆，艺术氛围浓厚', NULL, 4.7, 2341, 1, '2026-05-13 10:00:00', '2026-05-13 10:00:00');
INSERT INTO `checkin_spot` VALUES (4, '杨梅竹斜街', '北京市西城区杨梅竹斜街', 39.9108, 116.3972, '小众景点', '老北京胡同改造的文艺街区，充满烟火气', NULL, 4.5, 5678, 1, '2026-05-13 10:00:00', '2026-05-13 10:00:00');
INSERT INTO `checkin_spot` VALUES (5, 'Wood Garden餐厅', '北京市东城区东四十条', 39.9301, 116.4228, '餐厅', '主打创意料理的网红餐厅，环境优美', NULL, 4.6, 1890, 1, '2026-05-13 10:00:00', '2026-05-13 10:00:00');

-- ----------------------------
-- Table structure for visit_report
-- ----------------------------
DROP TABLE IF EXISTS `visit_report`;
CREATE TABLE `visit_report`  (
  `report_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `spot_id` int(11) NULL DEFAULT NULL,
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `rating` double NOT NULL,
  `image_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `status` smallint(6) NULL DEFAULT 1,
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`report_id`) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_spot_id`(`spot_id` ASC) USING BTREE,
  CONSTRAINT `visit_report_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `visit_report_ibfk_2` FOREIGN KEY (`spot_id`) REFERENCES `checkin_spot` (`spot_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for badge
-- ----------------------------
DROP TABLE IF EXISTS `badge`;
CREATE TABLE `badge`  (
  `badge_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `icon_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `condition_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `condition_value` int(11) NULL DEFAULT NULL,
  `status` smallint(6) NULL DEFAULT 1,
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`badge_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of badge
-- ----------------------------
INSERT INTO `badge` VALUES (1, '初来乍到', '完成第一次打卡', NULL, 'checkin_count', 1, 1, '2026-05-13 10:00:00');
INSERT INTO `badge` VALUES (2, '打卡达人', '完成10次打卡', NULL, 'checkin_count', 10, 1, '2026-05-13 10:00:00');
INSERT INTO `badge` VALUES (3, '探店高手', '发布5篇探店报告', NULL, 'report_count', 5, 1, '2026-05-13 10:00:00');
INSERT INTO `badge` VALUES (4, '路线规划师', '创建3条打卡路线', NULL, 'route_count', 3, 1, '2026-05-13 10:00:00');

-- ----------------------------
-- Table structure for checkin_route
-- ----------------------------
DROP TABLE IF EXISTS `checkin_route`;
CREATE TABLE `checkin_route`  (
  `route_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `cover_image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `status` smallint(6) NULL DEFAULT 1,
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`route_id`) USING BTREE,
  INDEX `idx_route_user`(`user_id` ASC) USING BTREE,
  CONSTRAINT `checkin_route_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for route_spot
-- ----------------------------
DROP TABLE IF EXISTS `route_spot`;
CREATE TABLE `route_spot`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `route_id` int(11) NULL DEFAULT NULL,
  `spot_id` int(11) NULL DEFAULT NULL,
  `order_num` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_route`(`route_id` ASC) USING BTREE,
  INDEX `idx_spot`(`spot_id` ASC) USING BTREE,
  CONSTRAINT `route_spot_ibfk_1` FOREIGN KEY (`route_id`) REFERENCES `checkin_route` (`route_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `route_spot_ibfk_2` FOREIGN KEY (`spot_id`) REFERENCES `checkin_spot` (`spot_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user_checkin
-- ----------------------------
DROP TABLE IF EXISTS `user_checkin`;
CREATE TABLE `user_checkin`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `spot_id` int(11) NULL DEFAULT NULL,
  `checkin_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_user_checkin`(`user_id` ASC) USING BTREE,
  INDEX `idx_spot_checkin`(`spot_id` ASC) USING BTREE,
  CONSTRAINT `user_checkin_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_checkin_ibfk_2` FOREIGN KEY (`spot_id`) REFERENCES `checkin_spot` (`spot_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user_badge
-- ----------------------------
DROP TABLE IF EXISTS `user_badge`;
CREATE TABLE `user_badge`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `badge_id` int(11) NULL DEFAULT NULL,
  `obtain_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_user_badge`(`user_id` ASC) USING BTREE,
  INDEX `idx_badge_user`(`badge_id` ASC) USING BTREE,
  CONSTRAINT `user_badge_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_badge_ibfk_2` FOREIGN KEY (`badge_id`) REFERENCES `badge` (`badge_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
