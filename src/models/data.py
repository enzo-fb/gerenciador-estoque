import sqlite3
from contextlib import closing
import os
from datetime import datetime
import shutil

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from pytz import timezone as ZoneInfo  # Para Python <3.9, instale pytz

DB_PATH = os.path.join(os.path.dirname(__file__), "estoque.db")


def tabela_existe(nome_tabela):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (nome_tabela,),
        )
        return c.fetchone() is not None


def init_db():
    print("Inicializando banco e criando tabelas se necessário...")
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        if not tabela_existe("produtos"):
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
        if not tabela_existe("produtos_vendidos"):
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
    realizar_backup()


def listar_produtos(filtro=None, vendidos=None):
    """
    Lista produtos do banco de dados com filtros opcionais.

    Args:
        filtro (str, optional): Termo para buscar em várias colunas. Defaults to None.
        vendidos (bool, optional): True para listar apenas vendidos, False para não vendidos,
                                  None para listar todos. Defaults to None.
    """
    # Usar a 'row_factory' é a forma moderna e segura de obter dicionários
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.row_factory = (
            sqlite3.Row
        )  # Transforma cada linha em um objeto tipo dicionário
        c = conn.cursor()

        query = "SELECT id, codigo, tipo, quantidade, cor, tamanho, preco, descricao, foto FROM produtos WHERE 1=1"
        params = []

        # Lógica para o filtro de texto (já estava correta)
        if filtro:
            query += " AND (id LIKE ? OR codigo LIKE ? OR tipo LIKE ? OR cor LIKE ? OR tamanho LIKE ? OR descricao LIKE ?)"
            filtro_val = f"%{filtro}%"
            params.extend([filtro_val] * 6)  # Usar extend é uma boa prática

        # --- LÓGICA IMPLEMENTADA PARA 'vendidos' ---
        # Assumindo que a tabela 'produtos' tem uma coluna 'data_venda'
        # que é NULL se o produto não foi vendido.
        if vendidos is True:
            query += " AND data_venda IS NOT NULL"
        elif vendidos is False:
            query += " AND data_venda IS NULL"

        c.execute(query, params)
        # O retorno já será uma lista de "Rows" que se comportam como dicionários
        return [dict(row) for row in c.fetchall()]


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
        c.execute("""DELETE FROM produtos WHERE codigo=?""", (codigo,))
        conn.commit()
    realizar_backup()


def atualizar_estoque_pos_venda(cursor, produto_id, nova_quantidade):
    if nova_quantidade > 0:
        cursor.execute(
            """UPDATE produtos SET quantidade=? WHERE id=?""",
            (nova_quantidade, produto_id),
        )
    else:
        remover_produto_por_codigo(produto_id)
    realizar_backup()


def marcar_como_vendido_controller(produto, quantidade_vendida, preco_venda):
    import time

    try:
        for tentativa in range(3):
            try:
                with closing(sqlite3.connect(DB_PATH, isolation_level=None)) as conn:
                    c = conn.cursor()
                    quantidade_disponivel = int(produto.get("quantidade", 0))
                    if quantidade_vendida > quantidade_disponivel:
                        print(
                            f"Erro: A quantidade vendida ({quantidade_vendida}) é maior que a disponível ({quantidade_disponivel})."
                        )
                        return False

                    now = datetime.now()
                    data_venda = now.strftime("%d-%m-%Y")
                    hora_venda = now.strftime("%H:%M:%S")
                    c.execute(
                        """
                        INSERT INTO produtos_vendidos (
                            id, codigo, tipo, quantidade, cor, tamanho, preco, descricao, foto, data_venda, hora_venda
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            produto.get("id"),
                            produto.get("codigo"),
                            produto.get("tipo"),
                            quantidade_vendida,
                            produto.get("cor"),
                            produto.get("tamanho"),
                            preco_venda,
                            produto.get("descricao"),
                            produto.get("foto"),
                            data_venda,
                            hora_venda,
                        ),
                    )
                    nova_quantidade = quantidade_disponivel - quantidade_vendida

                    print(f"Nova quantidade após venda: {nova_quantidade}")
                    atualizar_estoque_pos_venda(c, produto.get("id"), nova_quantidade)
                    conn.commit()
                    print(
                        f"Venda do produto ID {produto.get('id')} registrada com sucesso!"
                    )
                    realizar_backup()
                    return True
            except sqlite3.OperationalError as err:
                if "database is locked" in str(err):
                    print("Banco de dados está bloqueado, tentando novamente...")
                    time.sleep(0.2)
                    continue
                else:
                    print(f"Erro inesperado: {err}")
                    return False
        print("Falha ao acessar o banco de dados após múltiplas tentativas.")
        return False
    except Exception as e:
        print(f"Erro inesperado: {e}")
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


def atualizar_item_controller(item):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cursor = conn.cursor()
        foto_path = item.get("foto")
        # Se for um caminho de arquivo, atualiza a foto
        if foto_path and isinstance(foto_path, str) and os.path.exists(foto_path):
            with open(foto_path, "rb") as f:
                foto_blob = f.read()
            cursor.execute(
                """
                UPDATE produtos
                SET id=?, codigo=?, quantidade=?, preco=?, cor=?, tamanho=?, descricao=?, foto=?
                WHERE id=?
                """,
                (
                    item.get("id"),
                    item.get("codigo"),
                    item.get("quantidade"),
                    item.get("preco"),
                    item.get("cor"),
                    item.get("tamanho"),
                    item.get("descricao"),
                    foto_blob,
                    item.get("id"),
                ),
            )
        else:
            # Não atualiza o campo foto
            cursor.execute(
                """
                UPDATE produtos
                SET id=?, codigo=?, quantidade=?, preco=?, cor=?, tamanho=?, descricao=?
                WHERE id=?
                """,
                (
                    item.get("id"),
                    item.get("codigo"),
                    item.get("quantidade"),
                    item.get("preco"),
                    item.get("cor"),
                    item.get("tamanho"),
                    item.get("descricao"),
                    item.get("id"),
                ),
            )
        conn.commit()
    realizar_backup()


BACKUP_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "backup_path.txt")


def _carregar_backup_personalizado():
    if os.path.exists(BACKUP_CONFIG_PATH):
        try:
            with open(BACKUP_CONFIG_PATH, "r", encoding="utf-8") as f:
                caminho = f.read().strip()
                if caminho:
                    return caminho
        except Exception:
            pass
    return None


def _salvar_backup_personalizado(caminho):
    try:
        with open(BACKUP_CONFIG_PATH, "w", encoding="utf-8") as f:
            f.write(caminho)
    except Exception as ex:
        print(f"Erro ao salvar caminho do backup personalizado: {ex}")


# Inicializa o caminho do último backup personalizado
ULTIMO_BACKUP_PERSONALIZADO = [_carregar_backup_personalizado()]


def realizar_backup():
    import gzip

    origem = os.path.join(os.path.dirname(__file__), "../models/estoque.db")
    # Salva apenas no local personalizado, se definido
    if ULTIMO_BACKUP_PERSONALIZADO[0]:
        try:
            with (
                open(origem, "rb") as f_in,
                gzip.open(ULTIMO_BACKUP_PERSONALIZADO[0], "wb") as f_out,
            ):
                shutil.copyfileobj(f_in, f_out)
            return ULTIMO_BACKUP_PERSONALIZADO[0]
        except Exception as ex:
            print(f"Erro ao salvar backup personalizado periódico: {ex}")
            return None
    return None


def realizar_backup_personalizado(destino_gz):
    import gzip

    origem = os.path.join(os.path.dirname(__file__), "../models/estoque.db")
    try:
        with open(origem, "rb") as f_in, gzip.open(destino_gz, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
        ULTIMO_BACKUP_PERSONALIZADO[0] = destino_gz
        _salvar_backup_personalizado(destino_gz)
        return True
    except Exception as ex:
        print(f"Erro ao salvar backup personalizado: {ex}")
        return False


def realizar_backup_semanal():
    import gzip
    from datetime import datetime

    destino_base = ULTIMO_BACKUP_PERSONALIZADO[0]
    if not destino_base:
        print("Destino do backup semanal não definido pelo usuário.")
        return None

    base_dir = os.path.dirname(destino_base)
    semana_str = datetime.now().strftime("%Y-%W")
    destino = os.path.join(base_dir, f"estoque_backup_semanal_{semana_str}.db.gz")

    # Só faz backup se ainda não existe para esta semana
    if os.path.exists(destino):
        print(f"Backup semanal já existe para esta semana: {destino}")
        return destino

    origem = os.path.join(os.path.dirname(__file__), "../models/estoque.db")
    try:
        with open(origem, "rb") as f_in, gzip.open(destino, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
        print(f"Backup semanal criado: {destino}")
        return destino
    except Exception as ex:
        print(f"Erro ao salvar backup semanal: {ex}")
        return None
