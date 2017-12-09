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
  thread BIGINT
);

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

CREATE FUNCTION add_voice() RETURNS TRIGGER AS $add_voice$
BEGIN
  UPDATE threads SET votes=votes+NEW.voice WHERE id=NEW.thread;
  RETURN NEW;
END;
$add_voice$ LANGUAGE plpgsql;
CREATE TRIGGER ins_voice AFTER INSERT ON votes
  FOR EACH ROW EXECUTE PROCEDURE add_voice();

CREATE FUNCTION update_voice() RETURNS TRIGGER AS $add_voice$
BEGIN
  UPDATE threads SET votes=votes-OLD.voice+NEW.voice WHERE id=NEW.thread;
  RETURN NEW;
END;
$add_voice$ LANGUAGE plpgsql;
CREATE TRIGGER upd_voice AFTER UPDATE ON votes
  FOR EACH ROW EXECUTE PROCEDURE update_voice();


SELECT * FROM votes;
SELECT * FROM threads;
SELECT * FROM threads WHERE id=36079;
DROP TRIGGER upd_voice ON votes;
DROP FUNCTION create_path();
