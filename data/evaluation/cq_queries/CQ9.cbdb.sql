-- 理由：取徐阶起止年落在 1534 的任官及任职地点；机构在 CBDB 里只能由官名加地点看出。
SELECT o.c_office_chn AS office, p.c_firstyear, p.c_lastyear, ad.c_name_chn AS place, p.c_posting_id, p.c_notes
FROM POSTED_TO_OFFICE_DATA p JOIN OFFICE_CODES o ON o.c_office_id=p.c_office_id JOIN BIOG_MAIN b ON b.c_personid=p.c_personid LEFT JOIN POSTED_TO_ADDR_DATA pa ON pa.c_posting_id=p.c_posting_id LEFT JOIN ADDR_CODES ad ON ad.c_addr_id=pa.c_addr_id
WHERE p.c_personid=68547 AND (p.c_firstyear=1534 OR p.c_lastyear=1534) ORDER BY p.c_lastyear, p.c_posting_id;
