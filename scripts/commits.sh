#!/usr/bin/env bash
# Cria um histórico de commits organizado por etapa do projeto.
# Uso (na raiz do projeto):
#   bash scripts/commits.sh
#   git remote add origin https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
#   git push -u origin main
set -e

[ -d .git ] || git init -b main

git add .gitignore requirements.txt README.md
git commit -m "chore: estrutura inicial e documentação do projeto"

git add database/schema.sql
git commit -m "feat(bd): cria tabelas, chaves, índices e view"

git add database/seed.sql database/consultas.sql docs/modelo-er.md
git commit -m "feat(bd): adiciona dados de exemplo, consultas SQL e modelo ER"

git add app/models
git commit -m "feat(poo): cria classes Categoria, Tag e Wallpaper com herança e validação"

git add app/db.py app/repositorios.py app/uploads.py
git commit -m "feat(poo): adiciona repositórios, conexão e upload de imagens"

git add app/__init__.py app/routes
git commit -m "feat(dws): rotas Flask (site e API de wallpapers e categorias)"

git add css uploads
git commit -m "feat(dws): estilos responsivos e imagens de exemplo"

git add index.html js/comum.js js/galeria.js
git commit -m "feat(dws): página inicial com galeria e filtros"

git add pages/wallpaper.html pages/wallpaper-form.html js/wallpaper.js js/wallpaper-form.js
git commit -m "feat(dws): páginas de detalhe e cadastro de wallpapers"

git add pages/categorias.html pages/categoria-form.html js/categorias.js js/categoria-form.js
git commit -m "feat(dws): páginas de categorias"

git add scripts
git commit -m "chore: script de commits"

echo "Pronto. Confira com: git log --oneline"
