-- 迁移脚本：tag 表新增 sort 排序字段
-- 执行时机：V1.1 上线前在已有数据库上执行一次

USE my_shop;

ALTER TABLE tag
    ADD COLUMN sort INT NOT NULL DEFAULT 0 COMMENT '排序值，越小越靠前'
    AFTER parent_id;
