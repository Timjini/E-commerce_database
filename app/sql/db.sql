-- Vendors Table
CREATE TABLE vendors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    contact_name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255) NOT NULL,
    contact_phone VARCHAR(20),
    company_name VARCHAR(255) NOT NULL,
    tax_number VARCHAR(20),
    address VARCHAR(255),
    commission_rate DECIMAL(5, 2) NOT NULL
);

-- Shoppers Table
CREATE TABLE shoppers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255),
    phone_number VARCHAR(20),
    address VARCHAR(255),
    is_member BOOLEAN DEFAULT FALSE
);

-- Products Table
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    cost DECIMAL(10, 2) NOT NULL
);

-- Vendor Products (many-to-many between vendors and products)
CREATE TABLE vendor_products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id INT NOT NULL,
    product_id INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (vendor_id) REFERENCES vendors(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Orders Table
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    shopper_id INT NOT NULL,
    status ENUM('complete', 'incomplete') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2),
    FOREIGN KEY (shopper_id) REFERENCES shoppers(id)
);

-- Order Items (Products in Orders)
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    vendor_product_id INT NOT NULL,
    vendor_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (vendor_product_id) REFERENCES vendor_products(id),
    FOREIGN KEY (vendor_id) REFERENCES vendors(id)
);

-- Reviews Table (Shopper Experience)
CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_product_id INT NOT NULL,
    shopper_id INT NOT NULL,
    rating INT NOT NULL,
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vendor_product_id) REFERENCES vendor_products(id),
    FOREIGN KEY (shopper_id) REFERENCES shoppers(id)
);

-- Time Spent on Site (Shopper Experience)
CREATE TABLE time_spent (
    id INT AUTO_INCREMENT PRIMARY KEY,
    shopper_id INT NOT NULL,
    duration_minutes INT NOT NULL,
    session_date DATE,
    FOREIGN KEY (shopper_id) REFERENCES shoppers(id)
);

-- Costs Table
CREATE TABLE costs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    type ENUM('delivery_failure', 're_attempt', 'return_fraud') NOT NULL,
    cost_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- Revenue Table
CREATE TABLE revenue (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    vendor_id INT NOT NULL,
    commission_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (vendor_id) REFERENCES vendors(id)
);
