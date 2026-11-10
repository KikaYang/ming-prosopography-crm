-- 理由：书与人的关系在 BIOG_TEXT_DATA；《祀儀成典》按 TEXT_CODES 书名取。
SELECT b.c_name_chn AS person, d.c_personid, r.c_role_desc_chn AS role, t.c_title_chn AS title, d.c_notes
FROM BIOG_TEXT_DATA d JOIN TEXT_CODES t ON t.c_textid=d.c_textid JOIN BIOG_MAIN b ON b.c_personid=d.c_personid JOIN TEXT_ROLE_CODES r ON r.c_role_id=d.c_role_id
WHERE t.c_title_chn LIKE '%祀儀成典%' ORDER BY d.c_personid;
