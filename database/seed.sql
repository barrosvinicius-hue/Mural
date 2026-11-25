-- Dados de exemplo (as imagens estão em app/static/uploads/seed_*.jpg)
INSERT INTO categoria (id, nome, descricao) VALUES
    (1, 'Natureza',    'Montanhas, florestas e paisagens'),
    (2, 'Abstrato',    'Formas, ondas e gradientes'),
    (3, 'Cidades',     'Skylines, ruas e luzes noturnas'),
    (4, 'Minimalista', 'Poucos elementos e muito espaço'),
    (5, 'Espaço',      'Céu noturno, estrelas e nebulosas');

INSERT INTO wallpaper (id, titulo, descricao, arquivo, largura, altura, autor, favorito, categoria_id) VALUES
    (1, 'Amanhecer na serra', 'Sol nascendo atrás de três camadas de montanhas.', 'seed_amanhecer.jpg', 1280, 720, 'Equipe do projeto', 1, 1),
    (2, 'Floresta em névoa',  'Pinheiros no fim da tarde, versão para celular.',  'seed_floresta.jpg',  720, 1280, 'Equipe do projeto', 0, 1),
    (3, 'Ondas cobalto',      'Faixas onduladas em tons de azul.',                'seed_ondas.jpg',    1280, 720, 'Equipe do projeto', 1, 2),
    (4, 'Neon na avenida',    'Prédios escuros com janelas acesas em rosa e ciano.', 'seed_neon.jpg',    1280, 720, 'Equipe do projeto', 0, 3),
    (5, 'Silêncio',           'Um círculo laranja sobre fundo cinza claro.',      'seed_silencio.jpg', 1280, 720, 'Equipe do projeto', 0, 4),
    (6, 'Nebulosa roxa',      'Estrelas sobre uma nuvem de gás, versão para celular.', 'seed_nebulosa.jpg', 720, 1280, 'Equipe do projeto', 1, 5);

INSERT INTO tag (id, nome) VALUES
    (1, 'montanha'), (2, 'amanhecer'), (3, 'floresta'), (4, 'azul'),
    (5, 'neon'), (6, 'noite'), (7, 'celular'), (8, 'minimalista');

INSERT INTO wallpaper_tag (wallpaper_id, tag_id) VALUES
    (1, 1), (1, 2),
    (2, 3), (2, 7),
    (3, 4),
    (4, 5), (4, 6),
    (5, 8),
    (6, 6), (6, 7), (6, 4);
