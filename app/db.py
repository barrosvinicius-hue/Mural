import os
import sqlite3

import click
from flask import current_app, g

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_SQL = os.path.join(RAIZ, "database")


def get_db():
    """Uma conexão por requisição, com chaves estrangeiras ligadas."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(erro=None):
    conexao = g.pop("db", None)
    if conexao is not None:
        conexao.close()


def _executar_script(nome):
    with open(os.path.join(PASTA_SQL, nome), encoding="utf-8") as arquivo:
        get_db().executescript(arquivo.read())


def init_db(com_seed=True):
    """Recria todas as tabelas (apaga os dados!) e, se quiser, carrega o seed."""
    _executar_script("schema.sql")
    if com_seed:
        _executar_script("seed.sql")


def garantir_banco():
    """Na primeira execução, cria o banco sozinho."""
    if not os.path.exists(current_app.config["DATABASE"]):
        init_db()


@click.command("init-db")
@click.option("--sem-seed", is_flag=True, help="Cria só as tabelas, sem dados de exemplo.")
def init_db_command(sem_seed):
    """flask --app app init-db  ->  recria o banco."""
    init_db(com_seed=not sem_seed)
    click.echo("Banco recriado.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
