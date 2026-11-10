-- 理由：官名“吏部尚書”（明代 70658）按年份取 1528 年在任者；CBDB 只到年，且不分衔与职，所以直接按官职查。止年为空的记录不能算作在任，只保留起始年在 1518 年以后的（否则会把明初以来的尚书都算进去）。
SELECT b.c_name_chn AS person, p.c_personid, o.c_office_chn AS office, p.c_firstyear, p.c_lastyear, p.c_posting_id, a.c_appt_desc_chn AS appointment
FROM POSTED_TO_OFFICE_DATA p JOIN OFFICE_CODES o ON o.c_office_id=p.c_office_id JOIN BIOG_MAIN b ON b.c_personid=p.c_personid LEFT JOIN APPOINTMENT_CODES a ON a.c_appt_code=p.c_appt_code
WHERE o.c_office_id=70658 AND p.c_firstyear<=1528 AND p.c_firstyear>0 AND (p.c_lastyear>=1528 OR ((p.c_lastyear IS NULL OR p.c_lastyear=0) AND p.c_firstyear>=1518))
ORDER BY p.c_firstyear, p.c_posting_id;
