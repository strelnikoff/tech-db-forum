DROP TABLE IF EXISTS users CASCADE ;
DROP TABLE IF EXISTS forums CASCADE ;
DROP TABLE IF EXISTS forums_users CASCADE;
DROP TABLE IF EXISTS threads CASCADE;
DROP TABLE IF EXISTS posts CASCADE;
DROP TABLE IF EXISTS votes CASCADE;

DROP FUNCTION IF EXISTS create_post();
DROP FUNCTION IF EXISTS create_forum();
DROP FUNCTION IF EXISTS create_thread();
DROP FUNCTION IF EXISTS create_path();
DROP FUNCTION IF EXISTS add_voice();
DROP FUNCTION IF EXISTS update_voice();


CREATE TABLE users (
  nickname citext UNIQUE NOT NULL,
  about CHARACTER VARYING,
  email citext UNIQUE NOT NULL,
  fullname CHARACTER VARYING
);

-- CREATE INDEX idx_nickname_hash_user
-- ON users USING hash (nickname);

CREATE INDEX idx_nickname_user
ON users USING BTREE (nickname);

-- CREATE INDEX idx_email_user
-- ON users USING hash (email);

CREATE TABLE forums (
  slug citext PRIMARY KEY,
  title CHARACTER VARYING,
  nickname citext NOT NULL,
  posts INTEGER DEFAULT 0,
  threads INTEGER DEFAULT 0
);

-- CREATE INDEX idx_slug_hash_forum
-- ON forums  USING hash  (slug) ;

CREATE INDEX idx_slug_forum
ON forums  USING hash  (slug);
--
-- CREATE FUNCTION create_forum() RETURNS TRIGGER AS $create_forum$
-- BEGIN
--   INSERT INTO forums_users(slug, nickname) SELECT NEW.slug, NEW.nickname WHERE NOT EXISTS (
--       SELECT * FROM forums_users WHERE forums_users.nickname = NEW.nickname AND forums_users.slug=NEW.slug
--   );
--   RETURN NEW;
-- END;
-- $create_forum$ LANGUAGE plpgsql;
--
-- CREATE TRIGGER new_forum AFTER INSERT ON forums
--   FOR EACH ROW EXECUTE PROCEDURE create_forum();

CREATE TABLE forums_users (
  slug citext NOT NULL,
  nickname citext NOT NULL
);
--
-- CREATE INDEX idx_slug_forums_users
-- ON forums_users  USING hash  (slug) ;

CREATE UNIQUE INDEX idx_forums_users
ON forums_users(slug, nickname) ;

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

CREATE FUNCTION create_thread() RETURNS TRIGGER AS $create_thread$
BEGIN
  UPDATE forums SET threads = forums.threads + 1 WHERE slug = NEW.forum;
  BEGIN
      INSERT INTO forums_users(slug, nickname) VALUES (NEW.forum, NEW.nickname);
    EXCEPTION
      WHEN OTHERS THEN NULL ;
    END;
  RETURN NEW;
END;
$create_thread$ LANGUAGE plpgsql;

CREATE TRIGGER new_thread AFTER INSERT ON threads
  FOR EACH ROW EXECUTE PROCEDURE create_thread();

-- CREATE INDEX idx_slug_threads
-- ON threads  USING hash (slug);

CREATE INDEX idx_forum_threads
ON threads (forum);

CREATE INDEX idx_forum_created_threads
ON threads USING BTREE (forum, created);

CREATE INDEX idx_slug_thread
ON threads (slug);

CREATE INDEX idx_id_thread
ON threads (id);

CREATE TABLE posts (
  nickname citext NOT NULL,
  created TIMESTAMP WITH TIME ZONE,
  forum citext NOT NULL,
  id BIGSERIAL PRIMARY KEY,
  isEdited BOOLEAN DEFAULT FALSE,
  message CHARACTER VARYING,
  parent BIGINT DEFAULT 0,
  thread BIGINT NOT NULL,
  path BIGINT [],
  root BIGINT DEFAULT 0
);

-- CREATE INDEX idx_forum_posts
-- ON posts(forum);

-- CREATE INDEX idx_nickname_posts
-- ON posts  USING hash (nickname);

-- CREATE INDEX idx_message_posts
-- ON posts USING hash (message);

CREATE INDEX idx_thread_posts
ON posts (thread);

CREATE INDEX idx_thread_id_posts
ON posts (thread, id DESC);

CREATE INDEX idx_root_posts
ON posts (root);

CREATE INDEX idx_thread_parent_posts
ON posts (thread, parent);

CREATE INDEX idx_thread_path_posts
ON posts (thread, path DESC);


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

CREATE INDEX idx_nickname_thread_btree_votes
ON votes USING BTREE (nickname, thread) ;

CREATE UNIQUE INDEX idx_nickname_thread_votes
ON votes(nickname, thread) ;


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
  nick_name citext;
BEGIN
  SELECT nickname INTO nick_name FROM users WHERE nickname=new.nickname;
  NEW.nickname = nick_name;
  IF NEW.parent = 0::BIGINT
  THEN
    NEW.path = ARRAY[NEW.id];
    NEW.root = NEW.id;
  ELSE
    SELECT thread INTO partent_thread FROM posts WHERE id=NEW.parent;
    IF partent_thread != NEW.thread OR partent_thread IS NULL THEN
      RETURN NULL;
    END IF;
    NEW.path = (SELECT p.path || NEW.id FROM posts p WHERE id = NEW.parent);
    NEW.root = NEW.path[1];
  END IF;

  BEGIN
    INSERT INTO forums_users(slug, nickname) VALUES (NEW.forum, NEW.nickname);
  EXCEPTION
    WHEN OTHERS THEN NULL ;
  END;
  RETURN NEW;
END;
$create_post$ LANGUAGE plpgsql;

CREATE TRIGGER new_post BEFORE INSERT ON posts
  FOR EACH ROW EXECUTE PROCEDURE create_post();
