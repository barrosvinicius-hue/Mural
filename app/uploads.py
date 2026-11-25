import os
import uuid

from flask import current_app
from PIL import Image, UnidentifiedImageError

EXTENSOES = {"png", "jpg", "jpeg", "webp"}


class ErroUpload(ValueError):
    """Problema com o arquivo enviado (extensão, conteúdo inválido...)."""


def salvar_imagem(arquivo):
    """Valida a imagem, salva com nome único e devolve (nome, largura, altura)."""
    nome_original = arquivo.filename or ""
    extensao = nome_original.rsplit(".", 1)[-1].lower() if "." in nome_original else ""
    if extensao not in EXTENSOES:
        raise ErroUpload("Envie uma imagem PNG, JPG ou WEBP.")

    try:
        Image.open(arquivo.stream).verify()      # confere se é imagem de verdade
        arquivo.stream.seek(0)
        largura, altura = Image.open(arquivo.stream).size
    except (UnidentifiedImageError, OSError):
        raise ErroUpload("O arquivo enviado não é uma imagem válida.")

    arquivo.stream.seek(0)
    novo_nome = f"{uuid.uuid4().hex}.{extensao}"
    arquivo.save(os.path.join(current_app.config["UPLOAD_FOLDER"], novo_nome))
    return novo_nome, largura, altura


def remover_imagem(nome):
    """Apaga a imagem do disco (as de exemplo 'seed_*' são mantidas)."""
    if not nome or nome.startswith("seed_"):
        return
    caminho = os.path.join(current_app.config["UPLOAD_FOLDER"], nome)
    if os.path.exists(caminho):
        os.remove(caminho)
