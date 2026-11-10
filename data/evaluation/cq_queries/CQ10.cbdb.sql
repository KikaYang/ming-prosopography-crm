-- 理由：CBDB 没有分歧结构，能做的通用检查是：三人的任官中，备注文字不含编码官名的记录（编码与备注不合）；不针对已知的条目。
SELECT b.c_name_chn AS person, p.c_posting_id, o.c_office_chn AS office, p.c_firstyear, p.c_lastyear, p.c_notes
FROM POSTED_TO_OFFICE_DATA p JOIN OFFICE_CODES o ON o.c_office_id=p.c_office_id JOIN BIOG_MAIN b ON b.c_personid=p.c_personid WHERE p.c_personid IN (68266,68194,68547) AND p.c_notes IS NOT NULL AND p.c_notes!='' AND instr(p.c_notes, o.c_office_chn)=0
ORDER BY p.c_personid, p.c_posting_id;
