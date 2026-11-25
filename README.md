# Parede — cadastro de papéis de parede

Projeto Integrado (DWS + POO + BD). Site para cadastrar, organizar e consultar papéis de parede: imagem, resolução, autor, categoria e tags.

O front-end é feito em **HTML, CSS e JavaScript puros**. O **Python (Flask)** fornece as rotas da API e o **SQL (SQLite)** guarda os dados.

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask --app app run --debug
```

Abra http://127.0.0.1:5000. O Flask também serve o `index.html` e as páginas, então use sempre esse endereço (abrir o HTML direto no navegador não acessa o banco). Na primeira execução o banco (`instance/wallpapers.db`) é criado sozinho, com dados de exemplo.

Para apagar tudo e recriar o banco: `flask --app app init-db` (use `--sem-seed` para criar só as tabelas).

## Estrutura

```
papeis-de-parede/
├── index.html                 # página inicial: galeria com filtros
├── pages/
│   ├── wallpaper.html         # detalhe de um wallpaper (?id=1)
│   ├── wallpaper-form.html    # cadastrar ou editar wallpaper (?id=1 para editar)
│   ├── categorias.html        # lista de categorias
│   └── categoria-form.html    # cadastrar ou editar categoria
├── css/style.css
├── js/
│   ├── comum.js               # fetch para a API, avisos e funções usadas em todas as páginas
│   ├── galeria.js             # index.html
│   ├── wallpaper.js           # pages/wallpaper.html
│   ├── wallpaper-form.js      # pages/wallpaper-form.html
│   ├── categorias.js          # pages/categorias.html
│   └── categoria-form.js      # pages/categoria-form.html
├── uploads/                   # imagens (as seed_* são de exemplo)
├── database/                  # schema.sql, seed.sql, consultas.sql
├── app/                       # Python / Flask
│   ├── __init__.py            # create_app
│   ├── db.py                  # conexão SQLite e comando init-db
│   ├── repositorios.py        # acesso ao banco (CRUD)
│   ├── uploads.py             # validação e gravação das imagens
│   ├── models/                # classes de POO
│   └── routes/                # site.py (serve as páginas) + wallpapers.py e categorias.py (API)
├── docs/modelo-er.md
├── scripts/commits.sh         # histórico de commits sugerido
└── requirements.txt
```

Não há arquivos Python soltos na raiz: o projeto roda como pacote (`flask --app app`).

## Rotas Flask

| Método | Rota | O que faz |
|---|---|---|
| GET | `/`, `/index.html` | Entrega o `index.html` |
| GET | `/pages/...`, `/css/...`, `/js/...`, `/uploads/...` | Entrega só essas pastas (o resto do projeto não fica exposto) |
| GET | `/api/wallpapers` | Lista com filtros: `q`, `categoria`, `orientacao`, `tag`, `favoritos=1`, `ordem` |
| GET | `/api/resumo` | Total, favoritos e tags mais usadas |
| GET | `/api/wallpapers/<id>` | Um wallpaper |
| POST | `/api/wallpapers` | Cadastra (formulário com upload da imagem) |
| PUT | `/api/wallpapers/<id>` | Edita (a imagem é opcional) |
| DELETE | `/api/wallpapers/<id>` | Exclui o wallpaper e a imagem |
| POST | `/api/wallpapers/<id>/favorito` | Liga ou desliga o favorito |
| GET | `/api/categorias`, `/api/categorias/<id>` | Lista e detalhe |
| POST, PUT | `/api/categorias`, `/api/categorias/<id>` | Cadastra e edita (JSON) |
| DELETE | `/api/categorias/<id>` | Exclui (erro 409 se tiver wallpapers) |

Os erros voltam em JSON, no formato `{"erros": ["mensagem"]}`.

## Onde está cada disciplina

| Disciplina | Onde ver |
|---|---|
| **BD** | `database/schema.sql` (tabelas, chaves, CHECK, índices, view), `seed.sql`, `consultas.sql` (JOIN, GROUP BY, HAVING, subconsulta, N:N) e `docs/modelo-er.md` (diagrama e dicionário de dados) |
| **POO** | `app/models/` (classe abstrata `EntidadeBase` e as subclasses `Categoria`, `Tag` e `Wallpaper`) e `app/repositorios.py` (classe abstrata `RepositorioBase` e os repositórios) |
| **DWS** | `index.html` e `pages/` (HTML), `css/style.css` (layout responsivo), `js/` (fetch, DOM e validações) e `app/routes/` (rotas Flask) |

Conceitos de POO aplicados: abstração, herança, encapsulamento (atributos privados com `property`) e polimorfismo (`validar()`, `para_dict()` e `salvar()` funcionam para qualquer entidade).

## Checklist da recuperação

1. Procurar o professor até **sexta, 27/11/2026, às 12h35** e anotar o que ele apontar.
2. Corrigir no **mesmo repositório do GitHub** e continuar fazendo commits.
3. Em *Settings → Collaborators* do repositório, conferir que `leonardo.stephan@eaportal.org` continua como colaborador.
4. Apresentar o sistema corrigido ao professor dentro do prazo.
