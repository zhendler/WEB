SELECT 
    s.id,
    s.name
FROM 
    students s
JOIN 
    groups gr ON s.group_id = gr.id
WHERE 
    gr.group_name = 'Alpha'
ORDER BY 
    s.name;
