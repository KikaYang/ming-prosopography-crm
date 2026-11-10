-- 理由：取少傅一条及同年起始的全部任官；任命方式字段和备注是 CBDB 里最接近授予者、起因的地方，一并取出。
SELECT o.c_office_chn AS office, p.c_firstyear, p.c_lastyear, a.c_appt_desc_chn AS appointment, t.c_title_chn AS source, p.c_posting_id, p.c_notes
FROM POSTED_TO_OFFICE_DATA p JOIN OFFICE_CODES o ON o.c_office_id=p.c_office_id JOIN BIOG_MAIN b ON b.c_personid=p.c_personid LEFT JOIN APPOINTMENT_CODES a ON a.c_appt_code=p.c_appt_code LEFT JOIN TEXT_CODES t ON t.c_textid=p.c_source
WHERE p.c_personid=68266 AND p.c_firstyear=(SELECT c_firstyear FROM POSTED_TO_OFFICE_DATA q JOIN OFFICE_CODES r ON r.c_office_id=q.c_office_id WHERE q.c_personid=68266 AND r.c_office_chn='少傅')
ORDER BY p.c_posting_id;
