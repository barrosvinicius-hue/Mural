from .base import EntidadeBase


class Tag(EntidadeBase):
    """Palavra-chave livre usada para achar wallpapers (relação N:N)."""

    LIMITE = 20

    def __init__(self, nome="", id=None, total=0):
        super().__init__(id)
        self.nome = nome
        self.total = total

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        self._nome = (valor or "").strip().lower()

    def validar(self):
        if not self._nome:
            return ["A tag não pode ficar vazia."]
        if len(self._nome) > self.LIMITE:
            return [f"A tag '{self._nome}' passa de {self.LIMITE} caracteres."]
        return []

    def para_dict(self):
        return {"id": self.id, "nome": self.nome, "total": self.total}

    @staticmethod
    def normalizar_lista(texto):
        """'Azul, NEON, azul' -> ['azul', 'neon'] (sem repetidas e sem vazias)."""
        nomes = []
        for parte in (texto or "").split(","):
            nome = Tag(parte).nome
            if nome and nome not in nomes:
                nomes.append(nome)
        return nomes
