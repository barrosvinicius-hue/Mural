from .base import EntidadeBase


class Categoria(EntidadeBase):
    """Agrupa wallpapers por assunto (Natureza, Abstrato, Cidades...)."""

    def __init__(self, nome="", descricao="", id=None, data_cadastro=None, total_wallpapers=0):
        super().__init__(id, data_cadastro)
        self.nome = nome
        self.descricao = descricao
        self.total_wallpapers = total_wallpapers

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        self._nome = (valor or "").strip()

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, valor):
        self._descricao = (valor or "").strip()

    def validar(self):
        erros = []
        if not self._nome:
            erros.append("Informe o nome da categoria.")
        elif len(self._nome) > 40:
            erros.append("O nome da categoria deve ter no máximo 40 caracteres.")
        if len(self._descricao) > 200:
            erros.append("A descrição deve ter no máximo 200 caracteres.")
        return erros

    def para_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "total_wallpapers": self.total_wallpapers,
            "data_cadastro": self.data_cadastro,
        }

    @classmethod
    def de_linha(cls, linha):
        """Cria um objeto a partir de uma linha do banco."""
        chaves = linha.keys()
        return cls(
            nome=linha["nome"],
            descricao=linha["descricao"],
            id=linha["id"],
            data_cadastro=linha["data_cadastro"],
            total_wallpapers=linha["total_wallpapers"] if "total_wallpapers" in chaves else 0,
        )
