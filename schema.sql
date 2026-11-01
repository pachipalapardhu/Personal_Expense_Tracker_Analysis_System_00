-- Multi-user MySQL schema for Personal Expense Tracker.
-- Each row is owned by an authenticated account's numeric user_id.
-- Run init_db.py for an existing installation so it can migrate safely.
CREATE DATABASE IF NOT EXISTS expense_tracker_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE expense_tracker_db;

CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    category_name VARCHAR(100) NOT NULL,
    INDEX idx_categories_user (user_id),
    UNIQUE KEY uq_user_category (user_id, category_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS expenses (
    expense_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    expense_date DATE NOT NULL,
    category_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    description VARCHAR(255) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    INDEX idx_expenses_user_date (user_id, expense_date),
    INDEX idx_expenses_user_category (user_id, category_id),
    CONSTRAINT chk_positive_amount CHECK (amount > 0),
    CONSTRAINT fk_expense_category FOREIGN KEY (category_id)
        REFERENCES categories(category_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Categories are created separately for each newly verified account by the app.
-- Do not insert global demo expenses: all real expense rows must have an owner.
