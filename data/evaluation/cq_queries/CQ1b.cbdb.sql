-- 理由：“掌部事”在 CBDB 没有专门字段，能查的只有官名和备注文字，所以两处都按“掌吏部/掌部事”模糊匹配，范围取 1528–1532。
SELECT b.c_name_chn AS person, p.c_personid, o.c_office_chn AS office, p.c_firstyear, p.c_lastyear, p.c_posting_id, p.c_notes
FROM POSTED_TO_OFFICE_DATA p JOIN OFFICE_CODES o ON o.c_office_id=p.c_office_id JOIN BIOG_MAIN b ON b.c_personid=p.c_personid
WHERE (o.c_office_chn LIKE '%掌吏部%' OR o.c_office_chn LIKE '%掌部事%' OR p.c_notes LIKE '%掌吏部%' OR p.c_notes LIKE '%掌部事%')
  AND p.c_firstyear BETWEEN 1528 AND 1532
ORDER BY p.c_firstyear, p.c_posting_id;
