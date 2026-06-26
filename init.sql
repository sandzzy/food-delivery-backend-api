-- ============================================================
-- 🍔 Food Delivery DB - MySQL Init Script
-- Run this to create the database and all tables from scratch
-- ============================================================

CREATE DATABASE IF NOT EXISTS food_delivery_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE food_delivery_db;

-- ─────────────────────────────────────────────
-- USERS
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100)  NOT NULL,
    email       VARCHAR(100)  NOT NULL UNIQUE,
    phone       VARCHAR(20)   DEFAULT NULL,
    password    VARCHAR(255)  NOT NULL,
    role        ENUM('admin', 'restaurant_owner', 'customer') NOT NULL DEFAULT 'customer',
    created_at  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_users_email (email)
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────
-- RESTAURANTS
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS restaurants (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    owner_id      INT           NOT NULL,
    name          VARCHAR(150)  NOT NULL,
    description   VARCHAR(500)  DEFAULT NULL,
    email         VARCHAR(100)  DEFAULT NULL,
    phone         VARCHAR(20)   DEFAULT NULL,
    address       VARCHAR(300)  DEFAULT NULL,
    image         VARCHAR(300)  DEFAULT NULL,
    opening_time  TIME          DEFAULT NULL,
    closing_time  TIME          DEFAULT NULL,
    rating        FLOAT         NOT NULL DEFAULT 0.0,
    status        TINYINT(1)    NOT NULL DEFAULT 1,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────
-- CATEGORIES
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS categories (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id  INT          NOT NULL,
    name           VARCHAR(100) NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────
-- MENU ITEMS
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS menu_items (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id  INT           NOT NULL,
    category_id    INT           DEFAULT NULL,
    name           VARCHAR(150)  NOT NULL,
    description    VARCHAR(500)  DEFAULT NULL,
    price          FLOAT         NOT NULL,
    image          VARCHAR(300)  DEFAULT NULL,
    is_available   TINYINT(1)    NOT NULL DEFAULT 1,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id)   REFERENCES categories(id)  ON DELETE SET NULL
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────
-- ADDRESSES
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS addresses (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    user_id   INT          NOT NULL,
    house_no  VARCHAR(50)  DEFAULT NULL,
    street    VARCHAR(150) DEFAULT NULL,
    city      VARCHAR(100) NOT NULL,
    state     VARCHAR(100) NOT NULL,
    pincode   VARCHAR(20)  NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────
-- COUPONS
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS coupons (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    code           VARCHAR(50) NOT NULL UNIQUE,
    discount       FLOAT       NOT NULL,
    expiry_date    DATE        NOT NULL,
    minimum_order  FLOAT       NOT NULL DEFAULT 0.0,
    INDEX idx_coupons_code (code)
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────
-- CART
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS cart (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    user_id  INT NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────
-- CART ITEMS
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS cart_items (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    cart_id       INT NOT NULL,
    menu_item_id  INT NOT NULL,
    quantity      INT NOT NULL DEFAULT 1,
    FOREIGN KEY (cart_id)      REFERENCES cart(id)       ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────
-- ORDERS
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS orders (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT    NOT NULL,
    restaurant_id   INT    NOT NULL,
    address_id      INT    DEFAULT NULL,
    total_amount    FLOAT  NOT NULL,
    coupon_id       INT    DEFAULT NULL,
    payment_status  ENUM('pending', 'paid', 'failed', 'refunded') NOT NULL DEFAULT 'pending',
    order_status    ENUM('pending', 'confirmed', 'preparing', 'out_for_delivery', 'delivered', 'cancelled') NOT NULL DEFAULT 'pending',
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)       REFERENCES users(id)       ON DELETE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE,
    FOREIGN KEY (address_id)    REFERENCES addresses(id)   ON DELETE SET NULL,
    FOREIGN KEY (coupon_id)     REFERENCES coupons(id)     ON DELETE SET NULL,
    INDEX idx_orders_user (user_id),
    INDEX idx_orders_restaurant (restaurant_id)
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────
-- ORDER ITEMS
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS order_items (
    id            INT   AUTO_INCREMENT PRIMARY KEY,
    order_id      INT   NOT NULL,
    menu_item_id  INT   NOT NULL,
    quantity      INT   NOT NULL,
    price         FLOAT NOT NULL,
    FOREIGN KEY (order_id)     REFERENCES orders(id)     ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────
-- PAYMENTS
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS payments (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    order_id        INT          NOT NULL UNIQUE,
    payment_method  ENUM('cash', 'card', 'upi', 'wallet') NOT NULL,
    transaction_id  VARCHAR(150) DEFAULT NULL,
    payment_status  ENUM('pending', 'paid', 'failed', 'refunded') NOT NULL DEFAULT 'pending',
    paid_at         DATETIME     DEFAULT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────
-- REVIEWS
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS reviews (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    user_id        INT           NOT NULL,
    restaurant_id  INT           NOT NULL,
    rating         FLOAT         NOT NULL,
    review         VARCHAR(1000) DEFAULT NULL,
    created_at     DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)       REFERENCES users(id)       ON DELETE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE,
    INDEX idx_reviews_restaurant (restaurant_id)
) ENGINE=InnoDB;

-- ============================================================
-- 🌱 SEED DATA (optional — delete if not needed)
-- ============================================================

-- Admin user  (password: admin123)
INSERT IGNORE INTO users (name, email, phone, password, role) VALUES
('Admin', 'admin@foodapp.com', '0000000000',
 '$2b$12$KIXaOVOQl.P6rRoHqyD5lOZHi3jJcJk5uX3gBR0R5FFJYQ2CW2pEe',
 'admin');

-- Restaurant owner  (password: owner123)
INSERT IGNORE INTO users (name, email, phone, password, role) VALUES
('Pizza Owner', 'owner@pizzaplace.com', '9876543210',
 '$2b$12$0QkqW6jNqZ5nD4HhFmW6F.V5qPIxRD0k7D.SaKvnQsMpLhRlGUz7K',
 'restaurant_owner');

-- Sample restaurant
INSERT IGNORE INTO restaurants (owner_id, name, description, phone, address, opening_time, closing_time, status)
SELECT id, 'Pizza Palace', 'Best pizzas in town', '9876543210', '123 Main St', '09:00:00', '23:00:00', 1
FROM users WHERE email = 'owner@pizzaplace.com' LIMIT 1;

-- Categories
INSERT IGNORE INTO categories (restaurant_id, name)
SELECT id, 'Pizzas'   FROM restaurants WHERE name = 'Pizza Palace' LIMIT 1;
INSERT IGNORE INTO categories (restaurant_id, name)
SELECT id, 'Sides'    FROM restaurants WHERE name = 'Pizza Palace' LIMIT 1;
INSERT IGNORE INTO categories (restaurant_id, name)
SELECT id, 'Beverages' FROM restaurants WHERE name = 'Pizza Palace' LIMIT 1;

-- Menu items
INSERT IGNORE INTO menu_items (restaurant_id, category_id, name, description, price, is_available)
SELECT r.id, c.id, 'Margherita Pizza', 'Classic tomato and mozzarella', 12.99, 1
FROM restaurants r JOIN categories c ON c.restaurant_id = r.id AND c.name = 'Pizzas'
WHERE r.name = 'Pizza Palace' LIMIT 1;

INSERT IGNORE INTO menu_items (restaurant_id, category_id, name, description, price, is_available)
SELECT r.id, c.id, 'Pepperoni Pizza', 'Loaded with pepperoni', 14.99, 1
FROM restaurants r JOIN categories c ON c.restaurant_id = r.id AND c.name = 'Pizzas'
WHERE r.name = 'Pizza Palace' LIMIT 1;

INSERT IGNORE INTO menu_items (restaurant_id, category_id, name, description, price, is_available)
SELECT r.id, c.id, 'Garlic Bread', 'Toasted with garlic butter', 4.49, 1
FROM restaurants r JOIN categories c ON c.restaurant_id = r.id AND c.name = 'Sides'
WHERE r.name = 'Pizza Palace' LIMIT 1;

INSERT IGNORE INTO menu_items (restaurant_id, category_id, name, description, price, is_available)
SELECT r.id, c.id, 'Cola', '330ml can', 1.99, 1
FROM restaurants r JOIN categories c ON c.restaurant_id = r.id AND c.name = 'Beverages'
WHERE r.name = 'Pizza Palace' LIMIT 1;

-- Sample coupon
INSERT IGNORE INTO coupons (code, discount, expiry_date, minimum_order) VALUES
('WELCOME10', 10.00, DATE_ADD(CURDATE(), INTERVAL 1 YEAR), 20.00),
('SAVE5',      5.00, DATE_ADD(CURDATE(), INTERVAL 6 MONTH), 15.00);

-- ============================================================
-- ✅ Done! Run: mysql -u root -p < init.sql
-- ============================================================
