-- 理由：取张璁全部华盖殿任官及备注、来源，备注里写有出处。
SELECT o.c_office_chn AS office, p.c_firstyear, p.c_lastyear, p.c_fy_nh_year, p.c_posting_id, t.c_title_chn AS source, p.c_notes
FROM POSTED_TO_OFFICE_DATA p JOIN OFFICE_CODES o ON o.c_office_id=p.c_office_id JOIN BIOG_MAIN b ON b.c_personid=p.c_personid LEFT JOIN TEXT_CODES t ON t.c_textid=p.c_source
WHERE p.c_personid=68266 AND o.c_office_chn='華蓋殿大學士' ORDER BY p.c_firstyear;
