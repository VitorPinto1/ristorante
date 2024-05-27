CREATE DATABASE IF NOT EXISTS dbrestaurant_silkspeech;

USE dbrestaurant_silkspeech;



CREATE TABLE IF NOT EXISTS reservation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    person VARCHAR(50),
    totalPerson VARCHAR(50),
    day DATE,
    time TIME
);
