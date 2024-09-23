SELECT 
    s.name AS student_name,
    g.grade,
    g.date
FROM 
    grades g
JOIN 
    students s ON g.student_id = s.id
JOIN 
    groups grp ON s.group_id = grp.id
JOIN 
    subjects sub ON g.subject_id = sub.id
WHERE 
    grp.group_name = 'Gamma' 
    AND sub.subject_name = 'Careers adviser' 
    AND g.date = (
        SELECT MAX(g2.date)
        FROM grades g2
        WHERE g2.subject_id = g.subject_id
    )
