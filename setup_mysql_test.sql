-- Script prepares a MySQL server with:
-- A database hbnb_test_db
-- A new user hbnb_test (in localhost)
-- hbnb_test having all privileges on the database hbnb_test_db only
-- hbnb_test having SELECT privilege on the database performance_schema

CREATE DATABASE IF NOT EXISTS hbnb_test_db;
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
