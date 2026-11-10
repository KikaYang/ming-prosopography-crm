-- 理由：工程差遣在官名或备注里会有“建造/工程/規制”等字样；取嘉靖九年前后的这类记录，并取同人是否有祀儀成典的记录。
SELECT b.c_name_chn AS person, p.c_personid, o.c_office_chn AS office, p.c_firstyear, p.c_posting_id, p.c_notes,
  (SELECT count(*) FROM POSTED_TO_OFFICE_DATA q JOIN OFFICE_CODES r ON r.c_office_id=q.c_office_id WHERE q.c_personid=p.c_personid AND (r.c_office_chn LIKE '%祀儀成典%' OR q.c_notes LIKE '%祀儀成典%')) AS book_postings
FROM POSTED_TO_OFFICE_DATA p JOIN OFFICE_CODES o ON o.c_office_id=p.c_office_id JOIN BIOG_MAIN b ON b.c_personid=p.c_personid
WHERE (o.c_office_chn LIKE '%建造%' OR o.c_office_chn LIKE '%工程%' OR o.c_office_chn LIKE '%規制%' OR p.c_notes LIKE '%建造%' OR p.c_notes LIKE '%工程%' OR p.c_notes LIKE '%規制%')
  AND p.c_firstyear BETWEEN 1529 AND 1531 ORDER BY p.c_personid, p.c_posting_id;
