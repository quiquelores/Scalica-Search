/* Create our database */
CREATE DATABASE scalica CHARACTER SET utf8;

/* Setup permissions for the server */
CREATE USER 'appserver'@'localhost' IDENTIFIED BY 'foobarzoot';
GRANT ALL ON scalica.* TO 'appserver'@'localhost';
