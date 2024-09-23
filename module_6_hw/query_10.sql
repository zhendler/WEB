SELECT DISTINCT 
    sub.id,
    sub.subject_name 
FROM 
    students s
JOIN 
    grades g ON s.id = g.student_id
JOIN 
    subjects sub ON g.subject_id = sub.id
JOIN 
    teachers t ON sub.teacher_id = t.id
WHERE 
    s.name = 'Jennifer Rose' 
    AND t.name = 'Janet Carr'
ORDER BY 
    sub.subject_name;
