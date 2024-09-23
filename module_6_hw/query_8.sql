SELECT 
    t.id,
    t.name,
    AVG(g.grade) AS average_grade_given
FROM 
    teachers t
JOIN 
    subjects sub ON t.id = sub.teacher_id
JOIN 
    grades g ON sub.id = g.subject_id
WHERE 
    t.name = 'Mercedes Mitchell' 
GROUP BY 
    t.id, t.name;
