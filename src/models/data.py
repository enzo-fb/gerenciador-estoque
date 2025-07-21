import sqlite3
from contextlib import closing
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "estoque.db")


def init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS produtos (
                id TEXT PRIMARY KEY CHECK(length(id) = 8),
                codigo TEXT UNIQUE,
                tipo TEXT,
                quantidade INTEGER,
                cor TEXT,
                tamanho TEXT CHECK(length(tamanho) <= 2),
                preco REAL,
                descricao TEXT,
                foto BLOB,
                vendido INTEGER DEFAULT 0
            )
            """
        )
        # Cria tabela de produtos vendidos com data e hora separadas
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS produtos_vendidos (
                id TEXT PRIMARY KEY CHECK(length(id) = 8),
                codigo TEXT,
                tipo TEXT,
                quantidade INTEGER,
                cor TEXT,
                tamanho TEXT CHECK(length(tamanho) <= 2),
                preco REAL,
                descricao TEXT,
                foto TEXT,
                data_venda TEXT,
                hora_venda TEXT
            )
            """
        )
        conn.commit()


def adicionar_produto(produto):
    tipo = produto["tipo"].upper()
    cor = produto["cor"].upper()
    tamanho = produto["tamanho"].upper()
    foto_blob = None
    foto_path = produto.get("foto")
    if foto_path and os.path.exists(foto_path):
        with open(foto_path, "rb") as f:
            foto_blob = f.read()
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute(
            """
            INSERT INTO produtos (id, codigo, tipo, quantidade, cor, tamanho, preco, descricao, foto, vendido)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                produto["id"],
                produto["codigo"],
                tipo,
                produto["quantidade"],
                cor,
                tamanho,
                produto["preco"],
                produto["descricao"],
                foto_blob,  # Salva como BLOB
                produto.get("vendido", 0),
            ),
        )
        conn.commit()


def listar_produtos(filtro=None, vendidos=None):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        query = "SELECT * FROM produtos WHERE 1=1"
        params = []
        if filtro:
            query += " AND (id LIKE ? OR codigo LIKE ? OR tipo LIKE ? OR cor LIKE ? OR tamanho LIKE ? OR descricao LIKE ?)"
            filtro_val = f"%{filtro}%"
            params += [filtro_val] * 6
        if vendidos is not None:
            query += " AND vendido=?"
            params.append(1 if vendidos else 0)
        c.execute(query, params)
        rows = c.fetchall()
        return [
            dict(
                id=row[0],
                codigo=row[1],
                tipo=row[2],
                quantidade=row[3],
                cor=row[4],
                tamanho=row[5],
                preco=row[6],
                descricao=row[7],
                foto=row[8],  # Isso será um BLOB
                vendido=row[9],
            )
            for row in rows
        ]


def listar_produtos_vendidos():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute(
            "SELECT * FROM produtos_vendidos ORDER BY data_venda DESC, hora_venda DESC"
        )
        rows = c.fetchall()
        return [
            dict(
                id=row[0],
                codigo=row[1],
                tipo=row[2],
                quantidade=row[3],
                cor=row[4],
                tamanho=row[5],
                preco=row[6],
                descricao=row[7],
                foto=row[8],
                data_venda=row[9],
                hora_venda=row[10],
            )
            for row in rows
        ]


def remover_produto_por_codigo(codigo):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM produtos WHERE codigo=?", (codigo,))
        conn.commit()


def marcar_como_vendido(codigo):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        # Busca o produto antes de marcar como vendido
        c.execute("SELECT * FROM produtos WHERE codigo=?", (codigo,))
        row = c.fetchone()
        if row:
            # Verifica se já existe na tabela produtos_vendidos
            c.execute("SELECT 1 FROM produtos_vendidos WHERE id=?", (row[0],))
            if not c.fetchone():
                # Insere na tabela produtos_vendidos com data e hora separadas
                c.execute(
                    """
                    INSERT INTO produtos_vendidos (
                        id, codigo, tipo, quantidade, cor, tamanho, preco, descricao, foto, data_venda, hora_venda
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, date('now'), time('now'))
                    """,
                    (
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5],
                        row[6],
                        row[7],
                        row[8],
                    ),
                )
            # Remove da tabela principal (move o produto)
            c.execute("DELETE FROM produtos WHERE codigo=?", (codigo,))
            conn.commit()
            conn.commit()


# Função utilitária para salvar BLOB em arquivo temporário
def salvar_blob_em_arquivo(blob, ext=".jpg"):
    import tempfile

    if not blob:
        return None
    fd, path = tempfile.mkstemp(suffix=ext)
    with open(path, "wb") as f:
        f.write(blob)
    return path
