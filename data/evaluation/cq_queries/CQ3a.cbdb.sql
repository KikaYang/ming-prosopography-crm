-- 理由：入阁在 CBDB 里只能靠大学士类官职的起止年看；本题关心时段，所以把张璁全部大学士任官按年排出。
SELECT o.c_office_chn AS office, p.c_firstyear, p.c_lastyear, p.c_posting_id, p.c_notes
FROM POSTED_TO_OFFICE_DATA p JOIN OFFICE_CODES o ON o.c_office_id=p.c_office_id JOIN BIOG_MAIN b ON b.c_personid=p.c_personid
WHERE p.c_personid=68266 AND o.c_office_chn LIKE '%大學士%' ORDER BY p.c_firstyear, p.c_posting_id;
