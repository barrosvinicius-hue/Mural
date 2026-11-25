from abc import ABC, abstractmethod

from .db import get_db
from .models import Categoria, Tag, Wallpaper


class RepositorioBase(ABC):
    """Classe abstrata com o CRUD comum. As subclasses só dizem COMO inserir/atualizar.

    Polimorfismo: salvar() funciona igual para qualquer entidade.
    """

    tabela = ""

    @property
    def db(self):
        return get_db()

    def salvar(self, entidade):
        if entidade.id is None:
            self._inserir(entidade)
        else:
            self._atualizar(entidade)
        self.db.commit()
        return entidade

    def excluir(self, id):
        self.db.execute(f"DELETE FROM {self.tabela} WHERE id = ?", (id,))
        self.db.commit()

    @abstractmethod
    def _inserir(self, entidade): ...

    @abstractmethod
    def _atualizar(self, entidade): ...

    @abstractmethod
    def buscar(self, id): ...

    @abstractmethod
    def listar(self): ...


class CategoriaRepositorio(RepositorioBase):
    tabela = "categoria"

    def listar(self):
        linhas = self.db.execute(
            """SELECT c.*, COUNT(w.id) AS total_wallpapers
               FROM categoria c
               LEFT JOIN wallpaper w ON w.categoria_id = c.id
               GROUP BY c.id
               ORDER BY c.nome COLLATE NOCASE"""
        ).fetchall()
        return [Categoria.de_linha(linha) for linha in linhas]

    def buscar(self, id):
        linha = self.db.execute(
            """SELECT c.*, (SELECT COUNT(*) FROM wallpaper WHERE categoria_id = c.id) AS total_wallpapers
               FROM categoria c WHERE c.id = ?""",
            (id,),
        ).fetchone()
        return Categoria.de_linha(linha) if linha else None

    def nome_existe(self, nome, ignorar_id=None):
        linha = self.db.execute(
            "SELECT 1 FROM categoria WHERE lower(nome) = lower(?) AND id IS NOT ?",
            (nome, ignorar_id),
        ).fetchone()
        return linha is not None

    def _inserir(self, c):
        cursor = self.db.execute(
            "INSERT INTO categoria (nome, descricao) VALUES (?, ?)", (c.nome, c.descricao)
        )
        c.id = cursor.lastrowid

    def _atualizar(self, c):
        self.db.execute(
            "UPDATE categoria SET nome = ?, descricao = ? WHERE id = ?",
            (c.nome, c.descricao, c.id),
        )


class WallpaperRepositorio(RepositorioBase):
    tabela = "wallpaper"

    ORDENS = {
        "recentes": "data_cadastro DESC, id DESC",
        "antigos": "data_cadastro ASC, id ASC",
        "titulo": "titulo COLLATE NOCASE ASC",
        "resolucao": "(largura * altura) DESC, titulo COLLATE NOCASE ASC",
    }

    def listar(self, q="", categoria_id=None, orientacao="", tag="", so_favoritos=False, ordem="recentes"):
        sql = "SELECT * FROM vw_wallpaper_completo WHERE 1 = 1"
        params = []
        if q:
            sql += " AND (titulo LIKE ? OR autor LIKE ? OR descricao LIKE ?)"
            params += [f"%{q}%"] * 3
        if categoria_id:
            sql += " AND categoria_id = ?"
            params.append(categoria_id)
        if orientacao:
            sql += " AND orientacao = ?"
            params.append(orientacao)
        if tag:
            sql += """ AND id IN (SELECT wt.wallpaper_id FROM wallpaper_tag wt
                                  JOIN tag t ON t.id = wt.tag_id WHERE t.nome = ?)"""
            params.append(tag)
        if so_favoritos:
            sql += " AND favorito = 1"
        sql += " ORDER BY " + self.ORDENS.get(ordem, self.ORDENS["recentes"])

        linhas = self.db.execute(sql, params).fetchall()
        tags = self._tags_por_wallpaper([linha["id"] for linha in linhas])
        return [Wallpaper.de_linha(linha, tags.get(linha["id"])) for linha in linhas]

    def buscar(self, id):
        linha = self.db.execute("SELECT * FROM vw_wallpaper_completo WHERE id = ?", (id,)).fetchone()
        if not linha:
            return None
        return Wallpaper.de_linha(linha, self._tags_por_wallpaper([id]).get(id))

    def alternar_favorito(self, id):
        self.db.execute("UPDATE wallpaper SET favorito = 1 - favorito WHERE id = ?", (id,))
        self.db.commit()

    def estatisticas(self):
        linha = self.db.execute(
            "SELECT COUNT(*) AS total, COALESCE(SUM(favorito), 0) AS favoritos FROM wallpaper"
        ).fetchone()
        return {"total": linha["total"], "favoritos": linha["favoritos"]}

    def tags_populares(self, limite=12):
        linhas = self.db.execute(
            """SELECT t.id, t.nome, COUNT(*) AS total
               FROM tag t JOIN wallpaper_tag wt ON wt.tag_id = t.id
               GROUP BY t.id ORDER BY total DESC, t.nome LIMIT ?""",
            (limite,),
        ).fetchall()
        return [Tag(l["nome"], id=l["id"], total=l["total"]) for l in linhas]

    # --- métodos internos ----------------------------------------------------
    def _inserir(self, w):
        cursor = self.db.execute(
            """INSERT INTO wallpaper (titulo, descricao, arquivo, largura, altura, autor, favorito, categoria_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (w.titulo, w.descricao, w.arquivo, w.largura, w.altura, w.autor, int(w.favorito), w.categoria_id),
        )
        w.id = cursor.lastrowid
        self._sincronizar_tags(w.id, w.tags)

    def _atualizar(self, w):
        self.db.execute(
            """UPDATE wallpaper SET titulo = ?, descricao = ?, arquivo = ?, largura = ?,
                                    altura = ?, autor = ?, categoria_id = ? WHERE id = ?""",
            (w.titulo, w.descricao, w.arquivo, w.largura, w.altura, w.autor, w.categoria_id, w.id),
        )
        self._sincronizar_tags(w.id, w.tags)

    def _sincronizar_tags(self, wallpaper_id, nomes):
        """Troca as tags do wallpaper e apaga tags que ninguém mais usa."""
        self.db.execute("DELETE FROM wallpaper_tag WHERE wallpaper_id = ?", (wallpaper_id,))
        for nome in nomes:
            self.db.execute("INSERT OR IGNORE INTO tag (nome) VALUES (?)", (nome,))
            tag_id = self.db.execute("SELECT id FROM tag WHERE nome = ?", (nome,)).fetchone()["id"]
            self.db.execute(
                "INSERT INTO wallpaper_tag (wallpaper_id, tag_id) VALUES (?, ?)", (wallpaper_id, tag_id)
            )
        self.db.execute("DELETE FROM tag WHERE id NOT IN (SELECT tag_id FROM wallpaper_tag)")

    def _tags_por_wallpaper(self, ids):
        if not ids:
            return {}
        marcadores = ",".join("?" * len(ids))
        linhas = self.db.execute(
            f"""SELECT wt.wallpaper_id, t.nome FROM wallpaper_tag wt
                JOIN tag t ON t.id = wt.tag_id
                WHERE wt.wallpaper_id IN ({marcadores}) ORDER BY t.nome""",
            ids,
        ).fetchall()
        mapa = {}
        for linha in linhas:
            mapa.setdefault(linha["wallpaper_id"], []).append(linha["nome"])
        return mapa
