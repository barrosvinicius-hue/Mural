from flask import Blueprint, abort, jsonify, request

from ..models import Categoria
from ..repositorios import CategoriaRepositorio

bp = Blueprint("api_categorias", __name__, url_prefix="/api/categorias")
repo = CategoriaRepositorio()


def _salvar(categoria, status):
    """Lê o JSON, valida e salva. Devolve a categoria em JSON."""
    dados = request.get_json(silent=True)
    dados = dados if isinstance(dados, dict) else {}
    categoria.nome = dados.get("nome")
    categoria.descricao = dados.get("descricao")

    erros = categoria.validar()
    if not erros and repo.nome_existe(categoria.nome, categoria.id):
        erros.append("Já existe uma categoria com esse nome.")
    if erros:
        return jsonify(erros=erros), 400

    repo.salvar(categoria)
    return jsonify(repo.buscar(categoria.id).para_dict()), status


@bp.get("")
def listar():
    return jsonify(categorias=[c.para_dict() for c in repo.listar()])


@bp.get("/<int:id>")
def obter(id):
    categoria = repo.buscar(id) or abort(404)
    return jsonify(categoria.para_dict())


@bp.post("")
def criar():
    return _salvar(Categoria(), 201)


@bp.put("/<int:id>")
def atualizar(id):
    categoria = repo.buscar(id) or abort(404)
    return _salvar(categoria, 200)


@bp.delete("/<int:id>")
def excluir(id):
    categoria = repo.buscar(id) or abort(404)
    if categoria.total_wallpapers:
        return jsonify(erros=[
            f"A categoria “{categoria.nome}” tem wallpapers. Mova ou exclua os wallpapers antes."
        ]), 409
    repo.excluir(id)
    return "", 204
