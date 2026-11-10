-- 理由：先按官名取 1534 年在任的全部提学类官职（含提調學校、提學使），并带出任职地点，看浙江是谁。
SELECT b.c_name_chn AS person, p.c_personid, o.c_office_chn AS office, p.c_firstyear, p.c_lastyear, ad.c_name_chn AS place, p.c_posting_id, p.c_notes
FROM POSTED_TO_OFFICE_DATA p JOIN OFFICE_CODES o ON o.c_office_id=p.c_office_id JOIN BIOG_MAIN b ON b.c_personid=p.c_personid LEFT JOIN POSTED_TO_ADDR_DATA pa ON pa.c_posting_id=p.c_posting_id LEFT JOIN ADDR_CODES ad ON ad.c_addr_id=pa.c_addr_id
WHERE (o.c_office_chn LIKE '%提學%' OR o.c_office_chn LIKE '%提調學%') AND p.c_firstyear<=1534 AND p.c_firstyear>0 AND p.c_lastyear>=1534
ORDER BY p.c_firstyear, p.c_posting_id;
