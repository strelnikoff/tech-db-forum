SELECT COUNT(*) FROM threads;
SELECT count(*) FROM forums;


SELECT slug,
  nickname,
  title,
  (SELECT COUNT(*) FROM posts WHERE forum = 'ar8fT6rS6ARer') AS posts,
  (SELECT COUNT(*) FROM threads WHERE forum = 'ar8fT6rS6ARer') AS threads
FROM forums WHERE slug = 'ar8fT6rS6ARer';

SELECT *
FROM threads WHERE forum = (SELECT slug FROM forums WHERE forums.slug='XQ2Cqikkol8e8') AND slug ='asdf';

SELECT * FROM forums LIMIT 10;

SELECT p.nickname as nickname,
  p.created as created,
  p.forum as forum,
  p.id as id,
  p.thread as thread,
  p.message as message,
  p.isedited as isedited,
  p.parent as parent,
  u.fullname as fullname,
  u.email as email,
  u.about as about,
  t.message as tmessage,
  t.created as tcreated,
  t.votes as tvotes,
  t.slug as tslug,
  t.id as tid,
  t.title as ttitle,
  f.title as ftitle
FROM posts as p
  INNER JOIN threads as t ON p.thread = t.id
  INNER JOIN users as u ON p.nickname = u.nickname
  INNER JOIN forums AS f ON p.forum=f.slug AND p.id = 827382;

SELECT * FROM posts LIMIT 10;

INSERT INTO forums(slug, title, nickname) VALUES ('UcXJ6Ik9iLRXr', 'Audi pro illi.', (SELECT nickname FROM users WHERE nickname = 'etiam.8Cd5hhpSm3JD7V')) RETURNING *;


SELECT * FROM posts WHERE forum='oH6yylEY-m8xs';
SELECT * FROM threads WHERE forum='oH6yylEY-m8xs';

SELECT * FROM users WHERE nickname IN (SELECT nickname FROM forums_users WHERE slug = 'oH6yylEY-m8xs')

CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
SELECT pg_stat_statements_reset();

SELECT * FROM pg_stat_statements;
SELECT nickname, email, about, fullname, test.slug FROM users RIGHT JOIN (SELECT slug FROM forums WHERE slug = 'wT6nBv8b3m8Ek') as test ON nickname IN ( SELECT nickname FROM forums_users WHERE slug = 'wT6nBv8b3m8Ek') AND nickname > 'r53g0VPy39717.Zod'
COLLATE ucs_basic ORDER BY nickname COLLATE ucs_basic;

SELECT nickname, email, about, fullname, test.slug  FROM users RIGHT JOIN
  (SELECT slug FROM forums WHERE slug='_s19xUF_lMS2r') AS test
    ON
      nickname IN (SELECT nickname FROM forums_users WHERE slug = '_s19xUF_lMS2r')  AND nickname > '09gsUxc09L7dr.Zod' COLLATE ucs_basic
ORDER BY nickname COLLATE ucs_basic  LIMIT 100;

SELECT nickname, email, about, fullname  FROM users WHERE nickname IN (SELECT nickname FROM forums_users WHERE slug = '_s19xUF_lMS2r');



SELECT nickname, email, about, fullname, test.slug  FROM users RIGHT JOIN (SELECT slug FROM forums WHERE slug='_s19xUF_lMS2r') AS test ON nickname IN (SELECT nickname FROM forums_users WHERE slug = '_s19xUF_lMS2r')  ORDER BY nickname COLLATE ucs_basic  LIMIT 100


SELECT nickname, email, about, fullname, test.slug  FROM users RIGHT JOIN (SELECT slug FROM forums WHERE slug='395831yHMak2r') AS test ON nickname IN (SELECT nickname FROM forums_users WHERE slug = '395831yHMak2r')  ORDER BY nickname COLLATE ucs_basic  LIMIT 10


INSERT INTO posts (thread, nickname, forum, created, message, parent) VALUES (68, 'solebat.RaHyaRh7F37up1', 'ay-1HSOk5MSeSx', '2018-01-14 18:57:02.117698+03:00', 'Deum illam cognoscam hae quamquam, ab. Has spes id multa iamque pulvere iste eos rem auri cibo fui tu en ne. Qui os tuo aurium en dominos, valeret. Suam discere. Statuit pugno species humanus requiruntur pax nusquam pax ut sono spe, reconciliare. Opus olent ita hic percipitur tuo respondi fudi. Agnovi. Confitente seu pane te tu hymnus plus hic semel me meas obtentu nollent. Sacrifico eo hae notatum ibi scis potestates quoniam agro inquit eas vi intus, colligenda. Bibendo pollutum calidum fores dei incorruptione. Eum habeas vos desiderans salutem exultans ab es tria os eum levia grave meo remotum. Tu eo id.', 0) RETURNING *;

INSERT INTO posts (thread, nickname, forum, created, message, parent) VALUES (68, 'praeditum.g3C840ljIkp1Jd', '1XcWP_L8fLKxsE', '2018-01-14 19:12:52.137277+03:00', 'Vivendum timere abs nominum aut beati laude luminibus me os fueramus. Fuit. Mea leges circumstant tuus me via sapientiae. Laetamur servo esau mirabiliter his eos, conor adest trium et. En hi amo volo opus ex tam, tui mea vix oleat fastu. Sua placet te. Id quia catervas et hi quippe vivat disputando salubritatis has rem qui longius illac dixit placeant formas respondit una. Spectandum eos hac consumma, rapiatur fit fui innumerabiles mole. Proximum a se pax piae solo iamque, apparens cur de. Opus varia ita respuimus inlecebras ullo, divitiae autem amplexum ne. Cui ita. Pretium quaestio inhiant consulerem, qua. Erro visco piae ut erit ea ne, intellegimus nam levia laudis. Rem remisisti eius conatur temptat hic seu ea fuerunt o fixit prodeunt.', 0) RETURNING *;


INSERT INTO posts (thread, nickname, forum, created, message, parent) VALUES (68, 'praeditum.g3C840ljIkp1Jd', '1XcWP_L8fLKxsE', '2018-01-14 19:12:52.137277+03:00', 'Vivendum timere abs nominum aut beati laude luminibus me os fueramus. Fuit. Mea leges circumstant tuus me via sapientiae. Laetamur servo esau mirabiliter his eos, conor adest trium et. En hi amo volo opus ex tam, tui mea vix oleat fastu. Sua placet te. Id quia catervas et hi quippe vivat disputando salubritatis has rem qui longius illac dixit placeant formas respondit una. Spectandum eos hac consumma, rapiatur fit fui innumerabiles mole. Proximum a se pax piae solo iamque, apparens cur de. Opus varia ita respuimus inlecebras ullo, divitiae autem amplexum ne. Cui ita. Pretium quaestio inhiant consulerem, qua. Erro visco piae ut erit ea ne, intellegimus nam levia laudis. Rem remisisti eius conatur temptat hic seu ea fuerunt o fixit prodeunt.', 0) RETURNING *
;