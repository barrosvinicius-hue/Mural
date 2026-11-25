-- =====================================================================
-- Consultas de exemplo (rode no SQLite: sqlite3 instance/wallpapers.db)
-- =====================================================================

-- 1) JOIN: wallpapers com o nome da categoria
SELECT w.titulo, c.nome AS categoria, w.largura || 'x' || w.altura AS resolucao
FROM wallpaper w
JOIN categoria c ON c.id = w.categoria_id
ORDER BY w.titulo;

-- 2) GROUP BY + LEFT JOIN: quantos wallpapers cada categoria tem (inclui as vazias)
SELECT c.nome, COUNT(w.id) AS total
FROM categoria c
LEFT JOIN wallpaper w ON w.categoria_id = c.id
GROUP BY c.id
ORDER BY total DESC, c.nome;

-- 3) HAVING: categorias com mais de um wallpaper
SELECT c.nome, COUNT(*) AS total
FROM categoria c
JOIN wallpaper w ON w.categoria_id = c.id
GROUP BY c.id
HAVING COUNT(*) > 1;

-- 4) N:N: wallpapers e suas tags
SELECT w.titulo, GROUP_CONCAT(t.nome, ', ') AS tags
FROM wallpaper w
JOIN wallpaper_tag wt ON wt.wallpaper_id = w.id
JOIN tag t            ON t.id = wt.tag_id
GROUP BY w.id;

-- 5) Subconsulta: wallpapers que têm a tag 'celular'
SELECT titulo
FROM wallpaper
WHERE id IN (
    SELECT wt.wallpaper_id
    FROM wallpaper_tag wt
    JOIN tag t ON t.id = wt.tag_id
    WHERE t.nome = 'celular'
);

-- 6) VIEW: só os wallpapers em retrato
SELECT titulo, orientacao FROM vw_wallpaper_completo WHERE orientacao = 'Retrato';

-- 7) Função de agregação: maior resolução cadastrada (em pixels)
SELECT titulo, largura * altura AS pixels
FROM wallpaper
WHERE largura * altura = (SELECT MAX(largura * altura) FROM wallpaper);

-- 8) UPDATE / DELETE (exemplos)
-- UPDATE wallpaper SET favorito = 1 WHERE id = 2;
-- DELETE FROM wallpaper WHERE id = 5;
