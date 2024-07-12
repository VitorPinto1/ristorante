START TRANSACTION;

CREATE DATABASE IF NOT EXISTS testrestaurant;

USE testrestaurant;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE,
    token VARCHAR(255),
    active BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS reservation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    totalPerson INT,
    day DATE,
    time TIME,
    email VARCHAR(100), 
    user_id INT, 
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

COMMIT;