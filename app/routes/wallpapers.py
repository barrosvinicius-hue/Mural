from flask import Blueprint, abort, jsonify, request

from .. import uploads
from ..models import Tag, Wallpaper
from ..repositorios import CategoriaRepositorio, WallpaperRepositorio

bp = Blueprint("api_wallpapers", __name__, url_prefix="/api")
repo = WallpaperRepositorio()
repo_categorias = CategoriaRepositorio()


def _montar(formulario, wallpaper=None):
    """Copia os campos do formulário (multipart) para um objeto Wallpaper."""
    w = wallpaper or Wallpaper()
    w.titulo = formulario.get("titulo")
    w.descricao = formulario.get("descricao")
    w.autor = formulario.get("autor")
    w.categoria_id = formulario.get("categoria_id", type=int)
    w.tags = Tag.normalizar_lista(formulario.get("tags"))
    return w


def _validar(w):
    erros = w.validar()
    if w.categoria_id and not repo_categorias.buscar(w.categoria_id):
        erros.append("A categoria escolhida não existe.")
    return erros


def _resposta(w, status=200):
    return jsonify(repo.buscar(w.id).para_dict()), status


@bp.get("/wallpapers")
def listar():
    wallpapers = repo.listar(
        q=request.args.get("q", "").strip(),
        categoria_id=request.args.get("categoria", type=int),
        orientacao=request.args.get("orientacao", ""),
        tag=request.args.get("tag", "").strip().lower(),
        so_favoritos=request.args.get("favoritos") == "1",
        ordem=request.args.get("ordem", "recentes"),
    )
    return jsonify(wallpapers=[w.para_dict() for w in wallpapers])


@bp.get("/resumo")
def resumo():
    """Números do topo da galeria e as tags mais usadas."""
    return jsonify(**repo.estatisticas(), tags=[t.para_dict() for t in repo.tags_populares()])


@bp.get("/wallpapers/<int:id>")
def obter(id):
    w = repo.buscar(id) or abort(404)
    return jsonify(w.para_dict())


@bp.post("/wallpapers")
def criar():
    w = _montar(request.form)
    erros = _validar(w)
    arquivo = request.files.get("imagem")
    if not arquivo or not arquivo.filename:
        erros.append("Escolha a imagem do wallpaper.")
    if not erros:
        try:
            w.arquivo, w.largura, w.altura = uploads.salvar_imagem(arquivo)
        except uploads.ErroUpload as erro:
            erros.append(str(erro))
    if erros:
        return jsonify(erros=erros), 400

    repo.salvar(w)
    return _resposta(w, 201)


@bp.put("/wallpapers/<int:id>")
def atualizar(id):
    w = repo.buscar(id) or abort(404)
    arquivo_antigo = w.arquivo
    _montar(request.form, w)
    erros = _validar(w)
    arquivo = request.files.get("imagem")
    trocou_imagem = bool(arquivo and arquivo.filename)
    if trocou_imagem and not erros:
        try:
            w.arquivo, w.largura, w.altura = uploads.salvar_imagem(arquivo)
        except uploads.ErroUpload as erro:
            erros.append(str(erro))
    if erros:
        return jsonify(erros=erros), 400

    repo.salvar(w)
    if trocou_imagem:
        uploads.remover_imagem(arquivo_antigo)
    return _resposta(w)


@bp.delete("/wallpapers/<int:id>")
def excluir(id):
    w = repo.buscar(id) or abort(404)
    repo.excluir(id)
    uploads.remover_imagem(w.arquivo)
    return "", 204


@bp.post("/wallpapers/<int:id>/favorito")
def favoritar(id):
    repo.buscar(id) or abort(404)
    repo.alternar_favorito(id)
    return jsonify(repo.buscar(id).para_dict())
