CREATE TABLE users (
  nickname citext UNIQUE NOT NULL,
  about TEXT,
  email citext UNIQUE NOT NULL,
  fullname TEXT
);

CREATE INDEX idx_nickname_user
ON users USING hash (nickname);

CREATE INDEX idx_email_user
ON users USING hash (email);


CREATE TABLE forums (
  slug citext PRIMARY KEY,
  title CHARACTER VARYING,
  nickname citext NOT NULL
);

CREATE INDEX idx_slug_forum
ON forums  USING hash  (slug) ;

CREATE TABLE threads (
  nickname citext NOT NULL,
  created TIMESTAMP WITH TIME ZONE,
  forum citext NOT NULL,
  id BIGSERIAL PRIMARY KEY ,
  message TEXT,
  slug citext UNIQUE,
  title CHARACTER VARYING,
  votes INTEGER DEFAULT 0
);

CREATE INDEX idx_slug_threads
ON threads  USING hash (slug);

CREATE INDEX idx_forum_threads
ON threads  USING hash (forum);

CREATE TABLE posts (
  nickname citext NOT NULL,
  created TIMESTAMP WITH TIME ZONE,
  forum citext NOT NULL,
  id BIGSERIAL PRIMARY KEY,
  isEdited BOOLEAN DEFAULT FALSE,
  message CHARACTER VARYING,
  parent BIGINT DEFAULT 0,
  thread BIGINT NOT NULL,
  path BIGINT []
);

CREATE INDEX idx_forum_posts
ON posts  USING hash (forum);

CREATE INDEX idx_nickname_posts
ON posts  USING hash (nickname);

CREATE INDEX idx_message_posts
ON posts USING hash (message);

CREATE INDEX idx_thread_posts
ON posts (thread);


CREATE TABLE votes (
  id BIGSERIAL PRIMARY KEY,
  nickname citext NOT NULL references users(nickname),
  voice INTEGER,
  thread BIGINT NOT NULL REFERENCES threads(id)
);

CREATE INDEX idx_nickname_votes
ON votes  USING hash (nickname);

CREATE INDEX idx_thread_votes
ON votes (thread);

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