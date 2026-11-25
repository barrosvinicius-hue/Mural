from abc import ABC, abstractmethod


class EntidadeBase(ABC):
    """Classe abstrata: toda entidade salva no banco tem id e data de cadastro.

    Conceitos de POO usados no projeto:
    - Abstração:    esta classe define o que toda entidade precisa ter.
    - Herança:      Categoria, Tag e Wallpaper herdam daqui.
    - Encapsulamento: atributos "privados" (_nome) acessados por properties.
    - Polimorfismo: cada subclasse implementa validar() e para_dict() do seu jeito.
    """

    def __init__(self, id=None, data_cadastro=None):
        self._id = id
        self._data_cadastro = data_cadastro

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        self._id = valor

    @property
    def data_cadastro(self):
        return self._data_cadastro

    @abstractmethod
    def validar(self):
        """Retorna uma lista de mensagens de erro (lista vazia = tudo certo)."""

    @abstractmethod
    def para_dict(self):
        """Representação da entidade em dicionário."""

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self._id}>"
