-- 理由：CBDB 只到年，所以取起始年不晚于 1532、止年不早于 1532（或无止年）的全部任官；官职类别为空，分不出衔与差遣，不另筛。
SELECT o.c_office_chn AS office, p.c_firstyear, p.c_lastyear, p.c_posting_id, p.c_notes
FROM POSTED_TO_OFFICE_DATA p JOIN OFFICE_CODES o ON o.c_office_id=p.c_office_id JOIN BIOG_MAIN b ON b.c_personid=p.c_personid
WHERE p.c_personid=68266 AND p.c_firstyear<=1532 AND p.c_firstyear>0 AND (p.c_lastyear>=1532 OR p.c_lastyear IS NULL OR p.c_lastyear=0)
ORDER BY p.c_firstyear, p.c_posting_id;
