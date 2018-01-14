SELECT threads.slug, nickname,title, votes, created, message,id, forum, test.slug as test FROM threads RIGHT JOIN (SELECT slug FROM forums WHERE slug='5MYY6IEM5LRE8') AS test ON forum = '5MYY6IEM5LRE8'
SELECT threads.slug, nickname,title, votes, created, message,id, forum, test.slug as test FROM threads RIGHT JOIN (SELECT slug FROM forums WHERE slug='3V59-OXAJM82R') AS test ON forum = '3V59-OXAJM82R'
SELECT threads.slug, nickname,title, votes, created, message,id, forum, test.slug as test FROM threads RIGHT JOIN (SELECT slug FROM forums WHERE slug='ZKyY6-VmCArXr') AS test ON forum = 'ZKyY6-VmCArXr'
SELECT threads.slug, nickname,title, votes, created, message,id, forum, test.slug as test FROM threads RIGHT JOIN (SELECT slug FROM forums WHERE slug='zkYy6-vMcaRxR') AS test ON forum = 'zkYy6-vMcaRxR'

SELECT threads.slug, nickname,title, votes, created, message,id, forum, test.slug as test FROM threads RIGHT JOIN (SELECT slug FROM forums WHERE slug='3V59-OXAJM82R') AS test ON forum = '3V59-OXAJM82R' ORDER BY created LIMIT 15

SELECT threads.slug, nickname,title, votes, created, message,id, forum, test.slug as test FROM threads RIGHT JOIN (SELECT slug FROM forums WHERE slug='ZKyY6-VmCArXr') AS test ON forum = 'ZKyY6-VmCArXr' AND created >= '2017-10-11T12:18:36.159+03:00' ORDER BY created LIMIT 15

SELECT threads.slug, nickname,title, votes, created, message,id, forum, test.slug as test FROM threads RIGHT JOIN (SELECT slug FROM forums WHERE slug='zkYy6-vMcaRxR') AS test ON forum = 'zkYy6-vMcaRxR' AND created <= '2018-10-23T07:18:20.067+03:00' ORDER BY created DESC LIMIT 15