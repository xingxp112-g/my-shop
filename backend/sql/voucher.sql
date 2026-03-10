-- 代金券表（增量，不重建已有表）
CREATE TABLE IF NOT EXISTS voucher (
    id            INT PRIMARY KEY AUTO_INCREMENT,
    code          VARCHAR(6)     NOT NULL UNIQUE,
    amount        DECIMAL(10,2)  NOT NULL,
    start_date    DATE           NOT NULL,
    end_date      DATE           NOT NULL,
    status        VARCHAR(10)    NOT NULL DEFAULT 'unused',
    used_at       DATETIME       NULL,
    used_by       VARCHAR(50)    NULL,
    batch_no      VARCHAR(50)    NULL,
    created_at    DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_code (code),
    INDEX idx_status (status),
    INDEX idx_batch (batch_no),
    INDEX idx_end_date (end_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
