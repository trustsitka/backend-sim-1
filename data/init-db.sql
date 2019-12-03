DROP TABLE IF EXISTS animals;
CREATE TABLE animals (id INTEGER primary key NOT NULL, name text, species text);

INSERT INTO animals VALUES 
    (1, 'Bob', 'Llama'),
    (2, 'Jim', 'Lemur'),
    (3, 'Franklin', 'Donkey'),
    (4, 'Tim', 'Mouse'),
    (5, 'Joe', 'Elephant'),
    (6, 'Matt', 'Monkey'),
    (7, 'Mark', 'Lemur'),
    (8, 'Roscoe', 'Lemur'),
    (9, 'Laurel', 'Llama'),
    (10, 'David', 'Monkey')
;

DROP TABLE IF EXISTS users;
CREATE TABLE `users` ( `user_id` INTEGER NOT NULL, `username` TEXT NOT NULL,
    `password` TEXT NOT NULL, `role_id` INTEGER, `status` INTEGER, `created_date` TEXT,
     `updated_date` TEXT, PRIMARY KEY(`user_id`) );

INSERT INTO users VALUES
(1, 'DVader','placeholder', 1, 1, datetime('now'), datetime('now')),
(2, 'Mark','placeholder', 1, 1, datetime('now'), datetime('now')),
(3, 'GHalleck','placeholder', 1, 1, datetime('now'), datetime('now')),
(4, 'RLupin','placeholder', 1, 1, datetime('now'), datetime('now'))
;