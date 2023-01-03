CREATE DATABASE covid_vaccination;

USE covid_vaccination;

CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  role ENUM('user', 'admin') NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE centers (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  location VARCHAR(255) NOT NULL,
  capacity INT NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE dosages (
  id INT NOT NULL AUTO_INCREMENT,
  center_id INT NOT NULL,
  date DATE NOT NULL,
  dosage INT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (center_id) REFERENCES centers(id)
);

