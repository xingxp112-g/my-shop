-- 增量变更：tag 表新增 parent_id 字段
-- 执行时间：2026-03-11
-- 说明：为标签二级管理功能添加自关联字段，不影响现有数据

USE my_shop;

ALTER TABLE tag
    ADD COLUMN parent_id INT NULL DEFAULT NULL COMMENT '父标签 id，NULL 表示一级标签',
    ADD CONSTRAINT fk_tag_parent FOREIGN KEY (parent_id) REFERENCES tag (id);
