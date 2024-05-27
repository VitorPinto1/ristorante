CREATE DATABASE IF NOT EXISTS dbrestaurant_silkspeech;

USE dbrestaurant_silkspeech;



CREATE TABLE IF NOT EXISTS reservation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    totalPerson INT,
    day DATE,
    time TIME,
    email VARCHAR(100)
);
