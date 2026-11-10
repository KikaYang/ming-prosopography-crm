-- 理由：致仕、罢、召还如有记录，应在 STATUS_DATA 或 EVENTS_DATA；两表都查。
SELECT 'STATUS_DATA' AS src, s.c_status_desc_chn AS what, d.c_firstyear, d.c_lastyear, d.c_notes
FROM STATUS_DATA d JOIN STATUS_CODES s ON s.c_status_code=d.c_status_code WHERE d.c_personid=68266
UNION ALL
SELECT 'EVENTS_DATA', e.c_event, e.c_year, NULL, e.c_notes FROM EVENTS_DATA e WHERE e.c_personid=68266;
