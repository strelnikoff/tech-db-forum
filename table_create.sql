CREATE TABLE forums (
  slug CHARACTER VARYING PRIMARY KEY,
  title CHARACTER VARYING,
  nickname CHARACTER VARYING
);
CREATE INDEX idx_slug_hash_forum
ON forums USING hash (lower(slug));

CREATE INDEX idx_lower_slug_forum
ON forums (LOWER(slug)) ;


CREATE TABLE users (
  nickname TEXT,
  about TEXT,
  email TEXT,
  fullname TEXT
);

CREATE INDEX idx_nickname_hash
ON users USING hash (lower(nickname));

CREATE INDEX idx_lower_nickname
ON users (LOWER(nickname)) ;

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

CREATE INDEX idx_slug_hash_threads
ON threads USING hash (lower(slug));

CREATE INDEX idx_lower_slug_threads
ON threads (lower(slug));

CREATE TABLE posts (
  nickname CHARACTER VARYING NOT NULL ,
  created TIMESTAMP WITH TIME ZONE,
  forum CHARACTER VARYING,
  id BIGSERIAL PRIMARY KEY,
  isEdited BOOLEAN DEFAULT FALSE,
  message CHARACTER VARYING,
  parent BIGINT DEFAULT 0,
  thread BIGINT,
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

CREATE FUNCTION create_post() RETURNS TRIGGER AS $create_post$
DECLARE
  partent_thread BIGINT;
BEGIN
  IF NEW.parent = 0::BIGINT THEN
    RETURN NEW;
  END IF;
  SELECT thread INTO partent_thread FROM posts WHERE id=NEW.parent;
  IF partent_thread != NEW.thread OR partent_thread IS NULL THEN
    RETURN NULL;
  END IF;
  RETURN NEW;
END;
$create_post$ LANGUAGE plpgsql;

CREATE TRIGGER new_post BEFORE INSERT ON posts
  FOR EACH ROW EXECUTE PROCEDURE create_post();