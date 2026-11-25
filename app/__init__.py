import os

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

from . import db
from .db import RAIZ
from .routes import categorias, site, wallpapers


def create_app(config=None):
    # static_folder=None: os arquivos do site são servidos só pelas pastas
    # liberadas em routes/site.py (assim database/ e app/ nunca ficam expostos)
    app = Flask(__name__, static_folder=None)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "wallpapers.db"),
        RAIZ=RAIZ,
        UPLOAD_FOLDER=os.path.join(RAIZ, "uploads"),
        MAX_CONTENT_LENGTH=5 * 1024 * 1024,  # 5 MB por imagem
    )
    if config:
        app.config.update(config)

    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    app.register_blueprint(site.bp)
    app.register_blueprint(wallpapers.bp)
    app.register_blueprint(categorias.bp)

    @app.errorhandler(HTTPException)
    def erro_http(erro):
        """Nas rotas /api/ os erros também saem em JSON."""
        if request.path.startswith("/api/"):
            mensagens = {
                404: "Não encontrado.",
                405: "Método não permitido nesta rota.",
                413: "A imagem passa de 5 MB. Envie um arquivo menor.",
            }
            return jsonify(erros=[mensagens.get(erro.code, erro.description)]), erro.code
        return erro

    with app.app_context():
        db.garantir_banco()

    return app
