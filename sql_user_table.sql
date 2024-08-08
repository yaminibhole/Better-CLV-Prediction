show databases;

create database clv;

use clv;


CREATE TABLE users (
    user_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) DEFAULT NULL,
    username VARCHAR(50) DEFAULT NULL,
    email VARCHAR(50) DEFAULT NULL UNIQUE,
    password VARCHAR(100) DEFAULT NULL,
    phone BIGINT DEFAULT NULL UNIQUE,
    img VARCHAR(1000) DEFAULT NULL,
    PRIMARY KEY (user_id)
);



INSERT INTO users (name, username, email, password, phone, img)
VALUES 
    ('John Doe', 'johndoe1', 'john1@example.com', 'password123', 1234567890, 'https://static.vecteezy.com/system/resources/previews/001/840/612/large_2x/picture-profile-icon-male-icon-human-or-people-sign-and-symbol-free-vector.jpg'),
    ('Jane Smith', 'janesmith1', 'jane1@example.com', 'password456', 2345678901, 'https://static.vecteezy.com/system/resources/previews/001/840/612/large_2x/picture-profile-icon-male-icon-human-or-people-sign-and-symbol-free-vector.jpg'),
    ('Alice Johnson', 'alicejohnson1', 'alice1@example.com', 'password789', 3456789012, 'https://static.vecteezy.com/system/resources/previews/001/840/612/large_2x/picture-profile-icon-male-icon-human-or-people-sign-and-symbol-free-vector.jpg'),
    ('Bob Brown', 'bobbrown1', 'bob1@example.com', 'password101', 4567890123, 'https://static.vecteezy.com/system/resources/previews/001/840/612/large_2x/picture-profile-icon-male-icon-human-or-people-sign-and-symbol-free-vector.jpg'),
    ('Charlie Davis', 'charliedavis1', 'charlie1@example.com', 'password202', 5678901234, 'https://static.vecteezy.com/system/resources/previews/001/840/612/large_2x/picture-profile-icon-male-icon-human-or-people-sign-and-symbol-free-vector.jpg');

select * from users;
