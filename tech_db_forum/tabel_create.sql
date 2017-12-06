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
  parent INTEGER DEFAULT 0,
  thread INTEGER
);

CREATE TABLE votes (
  id BIGSERIAL PRIMARY KEY,
  nickname CHARACTER VARYING,
  voice INTEGER,
  thread INTEGER
);

SELECT *  FROM threads;
SELECT * FROM users WHERE nickname ='eam.GUwxXMk9lL47Rv' ;
SELECT * FROM forums WHERE lower(slug) = lower('_h4gLXCmaM4kK' );

UPDATE users SET nickname='q' WHERE nickname='oleg';

TRUNCATE TABLE users, posts, threads, votes, forums;

SELECT * FROM threads WHERE forum = '8_80ym335a0sk' AND created >= '2016-12-08T10:08:43.545Z' ORDER BY created DESC LIMIT 4

SELECT * FROM users WHERE nickname IS NULL ;



--http://127.0.0.1:8000/forum/g-3cqmOmy3p8S/users?desc=false&limit=100
SELECT * FROM users WHERE nickname IN (SELECT DISTINCT posts.nickname FROM posts INNER JOIN threads ON (posts.forum = threads.forum AND threads.forum= 'HCtVWWaau34kk')) ORDER BY lower(nickname) COLLATE ucs_basic LIMIT 100;
SELECT * FROM posts WHERE nickname='piZd5p5kS347j.joe';

SELECT DISTINCT * FROM users WHERE nickname IN (SELECT nickname FROM threads WHERE forum='g34s585AU3nRr') OR nickname IN (SELECT nickname FROM posts WHERE forum='g34s585AU3nRr');

SELECT DISTINCT * FROM users WHERE nickname IN (SELECT nickname FROM posts WHERE forum='g34s585AU3nRr') OR nickname IN (SELECT nickname FROM threads WHERE forum='g34s585AU3nRr');
SELECT DISTINCT posts.nickname FROM posts INNER JOIN threads ON (posts.forum = threads.forum AND threads.forum= 'g34s585AU3nRr' AND posts.forum= 'g34s585AU3nRr');
SELECT * FROM users WHERE nickname IN (SELECT DISTINCT posts.nickname AS nickname FROM posts                           FULL OUTER JOIN threads ON (posts.forum = threads.forum AND threads.forum = 'hi_vlCKLwMPk8')                           ORDER BY lower(nickname)  DESC)  AND lower(nickname) != lower('N516LCRlT34rP.Zod') LIMIT 4

SELECT DISTINCT * FROM users WHERE nickname IN (SELECT posts.nickname FROM posts FULL OUTER JOIN threads ON (posts.forum='oQ3EnSZlwM4SR' OR threads.forum='oQ3EnSZlwM4SR')) ORDER BY nickname;

SELECT * FROM (SELECT DISTINCT * FROM users WHERE
  (nickname IN (SELECT nickname FROM threads WHERE forum='01FPYGj59lpr8') OR
  nickname IN (SELECT nickname FROM posts WHERE forum='01FPYGj59lpr8')))
  AS foo  ORDER BY lower(nickname) COLLATE ucs_basic ;
SELECT DISTINCT nickname FROM threads WHERE forum='01FPYGj59lpr8';
SELECT DISTINCT nickname FROM posts WHERE forum='01FPYGj59lpr8';
SELECT * FROM (SELECT DISTINCT * FROM users WHERE nickname IN (SELECT nickname FROM threads WHERE forum='oQ3EnSZlwM4SR') OR nickname IN (SELECT nickname FROM posts WHERE forum='oQ3EnSZlwM4SR')  AND lower(nickname) != lower('3oEdNpq9X9n77.Zod')) AS foo ORDER BY nickname COLLATE ucs_basic

SELECT * FROM (SELECT DISTINCT * FROM users WHERE (nickname IN (SELECT nickname FROM threads WHERE lower(forum)=lower('3fr8qi05y3nk8')) OR nickname IN (SELECT nickname FROM posts WHERE lower(forum)=lower('3fr8qi05y3nk8'))) ) AS foo  ORDER BY lower(nickname) COLLATE ucs_basic  LIMIT 10;
SELECT * FROM forums WHERE lower(slug)=lower('3fr8qi05y3nk8')

UPDATE threads SET votes = votes+(1) WHERE id = 545
SELECT * FROM users WHERE lower(nickname)=lower('ENSv9Oiz9MPRS');
SELECT * FROM forums WHERE lower(slug)=lower('ENSv9Oiz9MPRS')
UPDATE posts SET isediter=TRUE, message='Exarsi ipsi exciderat amo homo nolle tam adpellata ait quot. Seducam pane eo eum quo, ob. Tuo ore suo inest fit, fatemur rapiunt sed tunc imples ad es splendeat impium occursantur sui sentire re tua. Gerit exciderat tum. Falsi perditum a iterum ob pius laetitiam amo demonstrare noe habito, adamavi hoc avide contemnat, cui sua placent. Detruncata adflatu opificiis metuebam has si perierat alio pius ac membra vix obruitur solae auget miseria. Tali diversisque recognoscimus erit volo dicat conperero ut fui nesciat es. Si curam. Os audi colligimus ridentem his, tot defrito cessare aer, detestetur perit ioseph fastu istas conectitur considero. Vox campos tum re animas turibulis quodam ex his nusquam ei o, nescit at da christus creator mei nomino. Ne hi ut denuo. Et dolor utinam usum ista te ad idem dona tam ibi tuo surgere consulentibus procedunt, de retrusa. Reperiret augendo fias audieris, ei, tolerare tota inquiunt. Agit repositi. Ne serie sim toleret absunt vim quamquam ne.' WHERE id=818
