import os

from flask import Blueprint, current_app, send_from_directory

bp = Blueprint("site", __name__)


@bp.get("/")
@bp.get("/index.html")
def index():
    """index.html fica na raiz do projeto."""
    return send_from_directory(current_app.config["RAIZ"], "index.html")


@bp.get("/<any(pages,css,js,uploads):pasta>/<path:arquivo>")
def arquivos(pasta, arquivo):
    """Serve SÓ as pastas pages/, css/, js/ e uploads/ (send_from_directory bloqueia '../')."""
    return send_from_directory(os.path.join(current_app.config["RAIZ"], pasta), arquivo)
