-- 美妆内部销售系统 建表 SQL
-- 数据库: my_shop

SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS my_shop DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE my_shop;

-- 品牌表
CREATE TABLE IF NOT EXISTS brand (
    id   INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '品牌名称'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 标签表
CREATE TABLE IF NOT EXISTS tag (
    id   INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '标签名称'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 商品表
CREATE TABLE IF NOT EXISTS product (
    id         INT PRIMARY KEY AUTO_INCREMENT,
    name       VARCHAR(200)   NOT NULL COMMENT '商品名称',
    brand_id   INT            NOT NULL COMMENT '品牌 ID',
    price      DECIMAL(10, 2) NOT NULL COMMENT '销售价格',
    image_url  VARCHAR(500)            COMMENT '商品图片 URL',
    remark     TEXT                    COMMENT '商品备注',
    status     TINYINT        NOT NULL DEFAULT 1 COMMENT '1=上架 0=下架',
    created_at DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (brand_id) REFERENCES brand (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 商品-标签关联表（多对多）
CREATE TABLE IF NOT EXISTS product_tag (
    product_id INT NOT NULL,
    tag_id     INT NOT NULL,
    PRIMARY KEY (product_id, tag_id),
    FOREIGN KEY (product_id) REFERENCES product (id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id)     REFERENCES tag (id)     ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 订单表
CREATE TABLE IF NOT EXISTS orders (
    id            INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(100)   NOT NULL COMMENT '客户姓名',
    phone         VARCHAR(20)    NOT NULL COMMENT '联系方式',
    total_amount  DECIMAL(10, 2) NOT NULL COMMENT '订单总金额',
    remark        TEXT                    COMMENT '订单备注',
    status        VARCHAR(20)    NOT NULL DEFAULT '待处理' COMMENT '待处理/已确认/已完成/已取消',
    created_at    DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 订单明细表
CREATE TABLE IF NOT EXISTS order_items (
    id         INT PRIMARY KEY AUTO_INCREMENT,
    order_id   INT            NOT NULL,
    product_id INT            NOT NULL,
    quantity   INT            NOT NULL COMMENT '数量',
    price      DECIMAL(10, 2) NOT NULL COMMENT '下单时单价（快照）',
    FOREIGN KEY (order_id)   REFERENCES orders  (id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES product (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
