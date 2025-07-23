import sqlite3
from contextlib import closing
import os
from datetime import datetime

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from pytz import timezone as ZoneInfo  # Para Python <3.9, instale pytz

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
                foto BLOB
            )
            """
        )
        # Corrigir: Remover CHECK(length(id_venda) = 8)
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS produtos_vendidos (
                id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
                id TEXT,
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
            INSERT INTO produtos (id, codigo, tipo, quantidade, cor, tamanho, preco, descricao, foto)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                id_venda=str(row[0]).zfill(5),  # Exibe sempre com 5 dígitos
                id=row[1],
                codigo=row[2],
                tipo=row[3],
                quantidade=row[4],
                cor=row[5],
                tamanho=row[6],
                preco=row[7],
                descricao=row[8],
                foto=row[9],
                data_venda=row[10],
                hora_venda=row[11],
            )
            for row in rows
        ]


def remover_produto_por_codigo(codigo):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM produtos WHERE codigo=?", (codigo,))
        conn.commit()


def marcar_como_vendido_controller(produto_id, quantidade_vendida, preco_venda):
    """
    Controla a lógica de venda de um produto, atualizando ou movendo-o.

    Args:
        produto_id (int): O ID único do produto a ser vendido.
        quantidade_vendida (int): A quantidade de itens vendidos.
        preco_venda (float): O preço total da venda.
    """
    try:
        with closing(sqlite3.connect(DB_PATH)) as conn:
            c = conn.cursor()

            # 1. Busca todas as colunas do produto
            c.execute("SELECT * FROM produtos WHERE id=?", (produto_id,))
            resultado = c.fetchone()

            if not resultado:
                print(f"Erro: Produto com ID {produto_id} não encontrado.")
                return False

            # Ajuste dos índices conforme a ordem da tabela produtos:
            # id, codigo, tipo, quantidade, cor, tamanho, preco, descricao, foto, vendido
            quantidade_disponivel = resultado[3]

            if quantidade_vendida > quantidade_disponivel:
                print(
                    f"Erro: A quantidade vendida ({quantidade_vendida}) é maior que a disponível ({quantidade_disponivel})."
                )
                return False

            # 2. Insere o registro na tabela de vendas
            # Obter data/hora de Brasília
            try:
                tz = ZoneInfo("America/Sao_Paulo")
            except Exception:
                import pytz

                tz = pytz.timezone("America/Sao_Paulo")
            now = datetime.now(tz)
            data_venda = now.strftime("%d-%m-%Y")
            hora_venda = now.strftime("%H:%M:%S")

            c.execute(
                """
                INSERT INTO produtos_vendidos (
                    id, codigo, tipo, quantidade, cor, tamanho, preco, descricao, foto, data_venda, hora_venda
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    resultado[0],  # id
                    resultado[1],  # codigo
                    resultado[2],  # tipo
                    quantidade_vendida,  # quantidade vendida
                    resultado[4],  # cor
                    resultado[5],  # tamanho
                    preco_venda,  # preco da venda
                    resultado[7],  # descricao
                    resultado[8],  # foto
                    data_venda,
                    hora_venda,
                ),
            )

            # 3. Atualiza a quantidade do produto na tabela principal
            nova_quantidade = quantidade_disponivel - quantidade_vendida
            if nova_quantidade > 0:
                # Se ainda houver estoque, apenas atualiza a quantidade
                c.execute(
                    "UPDATE produtos SET quantidade=? WHERE id=?",
                    (nova_quantidade, produto_id),
                )
            else:
                # Se o estoque chegar a zero, remove o produto
                c.execute("DELETE FROM produtos WHERE id=?", (produto_id,))

            conn.commit()
            print(f"Venda do produto ID {produto_id} registrada com sucesso!")
            return True

    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}")
        return False


# Função utilitária para salvar BLOB em arquivo temporário
def salvar_blob_em_arquivo(blob, ext=".jpg"):
    import tempfile

    if not blob:
        return None
    fd, path = tempfile.mkstemp(suffix=ext)
    with open(path, "wb") as f:
        f.write(blob)
    return path
