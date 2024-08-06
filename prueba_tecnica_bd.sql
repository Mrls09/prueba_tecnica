CREATE DATABASE test_interview;
USE test_interview;

CREATE TABLE name_customer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL
);

CREATE TABLE customer (
    phone INT(10) PRIMARY KEY,
    age INT NOT NULL,
    name_customer_id INT UNIQUE NOT NULL,
    FOREIGN KEY (name_customer_id) REFERENCES name_customer(id) ON DELETE CASCADE
);




