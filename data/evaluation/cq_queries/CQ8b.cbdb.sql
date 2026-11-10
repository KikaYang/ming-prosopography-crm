-- 理由：提学记录常无地点，所以再找：1534 年有提学类官职、且同年另有一条任职地点在浙江的人，那条就是候选本官。
SELECT b.c_name_chn AS person, p.c_personid, o.c_office_chn AS office, p.c_firstyear, p.c_lastyear, x.c_posting_id AS other_posting, xo.c_office_chn AS other_office, x.c_firstyear AS other_first, x.c_lastyear AS other_last, ad.c_name_chn AS other_place
FROM POSTED_TO_OFFICE_DATA p JOIN OFFICE_CODES o ON o.c_office_id=p.c_office_id JOIN BIOG_MAIN b ON b.c_personid=p.c_personid
JOIN POSTED_TO_OFFICE_DATA x ON x.c_personid=p.c_personid AND x.c_posting_id!=p.c_posting_id
JOIN OFFICE_CODES xo ON xo.c_office_id=x.c_office_id
JOIN POSTED_TO_ADDR_DATA pa ON pa.c_posting_id=x.c_posting_id JOIN ADDR_CODES ad ON ad.c_addr_id=pa.c_addr_id
WHERE (o.c_office_chn LIKE '%提學%' OR o.c_office_chn LIKE '%提調學%') AND p.c_firstyear<=1534 AND p.c_firstyear>0 AND p.c_lastyear>=1534
  AND ad.c_name_chn LIKE '%浙江%' AND x.c_firstyear<=1534 AND x.c_lastyear>=1534
ORDER BY p.c_personid;
