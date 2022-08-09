DROP DATABASE IF EXISTS tentative_opinions;
CREATE DATABASE tentative_opinions;
USE tentative_opinions;

DROP TABLE IF EXISTS Email;
DROP TABLE IF EXISTS Courthouse;
DROP TABLE IF EXISTS Email_courthouse;

CREATE TABLE Email(
	email_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    email_address VARCHAR(50) NOT NULL
);

CREATE TABLE Courthouse(
	courthouse_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    courthouse_name VARCHAR(100) NOT NULL
);

CREATE TABLE Email_courthouse(
	email_id INT NOT NULL,
    courthouse_id INT NOT NULL,
    FOREIGN KEY (email_id) REFERENCES Email(email_id),
    FOREIGN KEY (courthouse_id) REFERENCES Courthouse(courthouse_id)
);

INSERT INTO tentative_opinions.Email(`email_address`) VALUES ('srinidhi@gmail.com');
INSERT INTO tentative_opinions.Email(`email_address`) VALUES ('noooo@gmail.com');
INSERT INTO tentative_opinions.Courthouse(`courthouse_name`) VALUES ('Los Angeles Courthouse');
INSERT INTO tentative_opinions.Email_courthouse(`email_id`, `courthouse_id`) VALUES ('1', '1');
INSERT INTO tentative_opinions.Email_courthouse(`email_id`, `courthouse_id`) VALUES ('2', '1');
select * from courthouse where `courthouse_name` = 'Los Angeles Courthouse';
select * from email_courthouse where `courthouse_id`='1';