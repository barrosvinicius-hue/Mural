from .base import EntidadeBase
from .tag import Tag


class Wallpaper(EntidadeBase):
    """Um papel de parede cadastrado: imagem, resolução, autor, categoria e tags."""

    MAX_TAGS = 8

    def __init__(self, titulo="", descricao="", arquivo="", largura=0, altura=0,
                 autor="", categoria_id=None, favorito=False, tags=None,
                 categoria_nome="", id=None, data_cadastro=None):
        super().__init__(id, data_cadastro)
        self.titulo = titulo
        self.descricao = descricao
        self.arquivo = arquivo
        self.largura = largura
        self.altura = altura
        self.autor = autor
        self.categoria_id = categoria_id
        self.favorito = favorito
        self.tags = tags or []
        self.categoria_nome = categoria_nome

    # --- encapsulamento: textos sempre chegam "limpos" ---------------------
    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, valor):
        self._titulo = (valor or "").strip()

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, valor):
        self._descricao = (valor or "").strip()

    @property
    def autor(self):
        return self._autor

    @autor.setter
    def autor(self, valor):
        self._autor = (valor or "").strip()

    @property
    def largura(self):
        return self._largura

    @largura.setter
    def largura(self, valor):
        self._largura = self._como_inteiro(valor)

    @property
    def altura(self):
        return self._altura

    @altura.setter
    def altura(self, valor):
        self._altura = self._como_inteiro(valor)

    @staticmethod
    def _como_inteiro(valor):
        try:
            return int(valor)
        except (TypeError, ValueError):
            return 0

    # --- atributos calculados ------------------------------------------------
    @property
    def resolucao(self):
        return f"{self._largura}×{self._altura}"

    @property
    def orientacao(self):
        if self._largura > self._altura:
            return "Paisagem"
        if self._largura < self._altura:
            return "Retrato"
        return "Quadrado"

    # --- métodos exigidos pela classe abstrata -----------------------------
    def validar(self):
        erros = []
        if not self._titulo:
            erros.append("Informe o título do wallpaper.")
        elif len(self._titulo) > 80:
            erros.append("O título deve ter no máximo 80 caracteres.")
        if len(self._descricao) > 300:
            erros.append("A descrição deve ter no máximo 300 caracteres.")
        if len(self._autor) > 60:
            erros.append("O nome do autor deve ter no máximo 60 caracteres.")
        if not self.categoria_id:
            erros.append("Escolha uma categoria.")
        if self.arquivo and (self._largura <= 0 or self._altura <= 0):
            erros.append("Não foi possível ler a resolução da imagem.")
        if len(self.tags) > self.MAX_TAGS:
            erros.append(f"Use no máximo {self.MAX_TAGS} tags.")
        for nome in self.tags:
            erros.extend(Tag(nome).validar())
        return erros

    def para_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "arquivo": self.arquivo,
            "url_imagem": f"/uploads/{self.arquivo}",
            "largura": self.largura,
            "altura": self.altura,
            "resolucao": self.resolucao,
            "orientacao": self.orientacao,
            "autor": self.autor,
            "categoria_id": self.categoria_id,
            "categoria": self.categoria_nome,
            "favorito": bool(self.favorito),
            "tags": list(self.tags),
            "data_cadastro": self.data_cadastro,
        }

    def __str__(self):
        return f"{self.titulo} ({self.resolucao})"

    @classmethod
    def de_linha(cls, linha, tags=None):
        """Cria um objeto a partir de uma linha da view vw_wallpaper_completo."""
        return cls(
            titulo=linha["titulo"],
            descricao=linha["descricao"],
            arquivo=linha["arquivo"],
            largura=linha["largura"],
            altura=linha["altura"],
            autor=linha["autor"],
            categoria_id=linha["categoria_id"],
            favorito=bool(linha["favorito"]),
            tags=tags or [],
            categoria_nome=linha["categoria_nome"],
            id=linha["id"],
            data_cadastro=linha["data_cadastro"],
        )
