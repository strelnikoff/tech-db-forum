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
  created TIMESTAMP WITH TIME ZONE,
  forum CHARACTER VARYING,
  id BIGSERIAL PRIMARY KEY ,
  message TEXT,
  slug CHARACTER VARYING,
  title CHARACTER VARYING,
  votes INTEGER DEFAULT 0
);

CREATE TABLE posts (
  nickname CHARACTER VARYING,
  created TIMESTAMP WITH TIME ZONE,
  forum CHARACTER VARYING,
  id BIGSERIAL PRIMARY KEY,
  isEdited BOOLEAN DEFAULT FALSE,
  message CHARACTER VARYING,
  parent BIGINT DEFAULT 0,
  thread INTEGER,
  path BIGINT []
);

CREATE TABLE votes (
  id BIGSERIAL PRIMARY KEY,
  nickname CHARACTER VARYING,
  voice INTEGER,
  thread INTEGER
);



SELECT id, message, thread, forum, nickname, created, isedited, parent FROM posts
WHERE thread = 1 AND
      CASE WHEN $2 > -1
        THEN
          CASE WHEN $3 = 'DESC'
            THEN
              path < (
                SELECT p1.path FROM posts p1
                WHERE p1.id = $2)
          WHEN $3 = 'ASC'
            THEN path > (
              SELECT p1.path
              FROM post p1
              WHERE p1.id = $2)
          ELSE TRUE
          END
      ELSE
        TRUE
      END
ORDER BY path DESC, thread DESC LIMIT 10

INSERT INTO posts (thread, nickname, forum, created, message, parent) VALUES (1, 'sdas', 1, '2017-12-08T05:13:23.721+03:00', 'sdfasdf', 0) RETURNING thread, nickname, forum, created, message, parent, path;
INSERT INTO posts (thread, nickname, forum, created, message, parent) VALUES (1, 'sdas', 1, '2017-12-08T05:13:23.721+03:00', 'sdfasdf', 1) RETURNING thread, nickname, forum, created, message, parent, path;

INSERT INTO posts (thread, nickname, forum, created, message, parent) VALUES (1, 'sdas', 1, '2017-12-08T05:13:23.721+03:00', 'sdfasdf', 5) RETURNING thread, nickname, forum, created, message, parent, path;


CREATE FUNCTION create_path() RETURNS TRIGGER AS $create_path$
DECLARE
  old_path BIGINT[];
  new_path BIGINT[];
BEGIN
  IF NEW.parent = 0 THEN
    UPDATE posts SET path= ARRAY [0, NEW.id] WHERE id=NEW.id;
  ELSE
    SELECT path INTO old_path FROM posts WHERE id=NEW.parent;
    new_path:=array_append(old_path, NEW.id);
    UPDATE posts SET path=new_path WHERE id=NEW.id;
  END IF;
  RETURN NEW;
END;
$create_path$ LANGUAGE plpgsql;
CREATE TRIGGER set_path AFTER INSERT ON posts
  FOR EACH ROW EXECUTE PROCEDURE create_path();

DROP TRIGGER set_path ON posts;
DROP FUNCTION create_path();
TRUNCATE posts;
SELECT id, path FROM posts ORDER BY path;

SELECT (SELECT path FROM posts WHERE id=2) || ARRAY[ BIGINT (1)]