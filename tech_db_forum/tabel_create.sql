DROP TABLE forums;
DROP TABLE users;
DROP TABLE threads;
DROP TABLE posts;
DROP TABLE votes;

CREATE TABLE forums (
  slug CHARACTER VARYING PRIMARY KEY,
  title CHARACTER VARYING,
  nickname CHARACTER VARYING
);

CREATE TABLE users (
  nickname TEXT,
  about TEXT,
  email TEXT,
  fullname TEXT
);

CREATE TABLE threads (
  nickname CHARACTER VARYING,
  created TIMESTAMP,
  forum CHARACTER VARYING,
  id INTEGER PRIMARY KEY,
  message TEXT,
  slug CHARACTER VARYING,
  title CHARACTER VARYING,
  votes INTEGER
);

CREATE TABLE posts (
  nickname CHARACTER VARYING,
  created TIMESTAMP,
  forum CHARACTER VARYING,
  id INTEGER PRIMARY KEY,
  isEditer BOOLEAN DEFAULT FALSE,
  message CHARACTER VARYING,
  parent INTEGER DEFAULT 0,
  thread INTEGER
);

CREATE TABLE votes (
  id INTEGER PRIMARY KEY,
  nickname CHARACTER VARYING,
  voice INTEGER,
  thread INTEGER
);

SELECT * FROM users;

UPDATE users SET about = 'i update it' WHERE nickname='oleg';

TRUNCATE TABLE users, posts, threads, votes, forums;