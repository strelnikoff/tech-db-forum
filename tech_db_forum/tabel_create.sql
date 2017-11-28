DROP TABLE forums;
DROP TABLE users;
DROP TABLE threads;
DROP TABLE posts;

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
  slug CHARACTER VARYING
);

CREATE TABLE posts (
  nickname CHARACTER VARYING,
  created TIMESTAMP,
  forum CHARACTER VARYING,
  id INTEGER PRIMARY KEY,
  isEditer BOOLEAN DEFAULT FALSE,
  message CHARACTER VARYING,
  parent INTEGER DEFAULT 0,
  tread INTEGER
);

CREATE TABLE votes (
  id INTEGER PRIMARY KEY,
  nickname CHARACTER VARYING,
  voice INTEGER,
  thread CHARACTER VARYING
);

TRUNCATE TABLE users, posts, threads, votes, forums;
SELECT COUNT(*) FROM users;

INSERT INTO users (nickname, about, email, fullname) VALUES ('oleg', 'about me', 'oleg@mail.ru', 'Full Oleg');
INSERT INTO users VALUES ("oleg", "about me", "oleg@mail.ru", "Full Oleg");
SELECT * FROM users WHERE email = "oleg";
SELECT * FROM votes WHERE id=1 AND t;

SELECT * FROM test WHERE test_id =1;
CREATE TABLE test2 (
  test_id CHARACTER(5)
);
DROP TABLE test;
INSERT INTO test2 VALUES ('w');
SELECT * FROM users WHERE nickname != 'oleg';