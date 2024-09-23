SELECT 
    sub.id,
    sub.subject_name 
FROM 
    subjects sub
JOIN 
    teachers t ON sub.teacher_id = t.id
WHERE 
    t.name = 'Mercedes Mitchell'
    
    

SELECT 
    sub.id,
    sub.subject_name 
FROM 
    subjects sub
WHERE 
    sub.teacher_id = 15;

