-- 创建旅游博客表

CREATE TABLE IF NOT EXISTS `blog_post` (
    `post_id` INT NOT NULL AUTO_INCREMENT,
    `author_name` VARCHAR(50) NOT NULL COMMENT '作者昵称',
    `title` VARCHAR(200) NOT NULL COMMENT '博文标题',
    `content` TEXT NOT NULL COMMENT '博文内容',
    `status` TINYINT DEFAULT 1 COMMENT '状态:0-禁用,1-正常',
    `view_count` INT DEFAULT 0 COMMENT '浏览次数',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`post_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='旅游博文表';

CREATE TABLE IF NOT EXISTS `blog_comment` (
    `comment_id` INT NOT NULL AUTO_INCREMENT,
    `post_id` INT NOT NULL COMMENT '博文ID',
    `author_name` VARCHAR(50) NOT NULL COMMENT '评论者昵称',
    `content` TEXT NOT NULL COMMENT '评论内容',
    `status` TINYINT DEFAULT 1 COMMENT '状态:0-禁用,1-正常',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`comment_id`),
    INDEX `idx_post_id` (`post_id`),
    FOREIGN KEY (`post_id`) REFERENCES `blog_post`(`post_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='博文评论表';

-- 插入示例数据
INSERT INTO `blog_post` (`author_name`, `title`, `content`) VALUES 
('旅游达人小王', '武汉三日游攻略分享', '刚刚从武汉回来，和大家分享一下我的旅游攻略！第一天：黄鹤楼、武汉长江大桥、户部巷；第二天：湖北省博物馆、东湖；第三天：楚河汉街、江汉路步行街。非常充实的一次旅行！'),
('美食探索家', '武汉必吃美食推荐', '武汉不仅是九省通衢，更是美食之都！热干面、周黑鸭、武昌鱼、糊汤粉...每一样都让人回味无穷！强烈推荐大家去户部巷和万松园品尝美食。');

INSERT INTO `blog_comment` (`post_id`, `author_name`, `content`) VALUES 
(1, '背包客小李', '攻略写得太好了！我正准备去武汉呢，收藏了！'),
(1, '摄影爱好者', '请问黄鹤楼的门票多少钱？'),
(2, '吃货一枚', '作为武汉人，这个推荐太精准了！万松园才是真正的美食天堂！');

SELECT '博客数据表创建完成！' AS message;