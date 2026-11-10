-- 理由：修书差遣也可能记在任官表，书名在官名或备注里（如“總裁官(祀儀成典)”）；两处都匹配。
SELECT b.c_name_chn AS person, p.c_personid, o.c_office_chn AS office, p.c_firstyear, p.c_posting_id, p.c_notes
FROM POSTED_TO_OFFICE_DATA p JOIN OFFICE_CODES o ON o.c_office_id=p.c_office_id JOIN BIOG_MAIN b ON b.c_personid=p.c_personid WHERE o.c_office_chn LIKE '%祀儀成典%' OR p.c_notes LIKE '%祀儀成典%' ORDER BY p.c_personid, p.c_posting_id;
