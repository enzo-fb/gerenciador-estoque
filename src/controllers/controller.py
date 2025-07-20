from models import data

TIPOS_PRODUTO = {
    "01": "BLAZER",
    "02": "CALÇA",
    "03": "CAMISA",
    "04": "CAMISETA",
    "05": "SHORT",
    "06": "VESTIDO",
    "07": "SAIA",
    "08": "CASACO",
    "09": "COLETE",
    # Adicione outros códigos e tipos conforme necessário
}


def inicializar_banco():
    data.init_db()


def identificar_tipo_por_id(id_str):
    prefixo = id_str[:2]
    return TIPOS_PRODUTO.get(prefixo, "DESCONHECIDO")


def adicionar_produto_controller(produto):
    # Validações
    if len(produto.get("id", "")) != 8:
        raise ValueError("O ID deve ter exatamente 8 dígitos.")
    if len(produto.get("tamanho", "")) > 2:
        raise ValueError("O tamanho deve ter no máximo 2 caracteres.")
    # Identifica o tipo automaticamente pelo id
    produto["tipo"] = identificar_tipo_por_id(produto["id"])
    # Garante que 'codigo' existe e é igual ao 'id'
    produto["codigo"] = produto["id"]
    data.adicionar_produto(produto)


def listar_produtos_controller(filtro=None, vendidos=None):
    return data.listar_produtos(filtro=filtro, vendidos=vendidos)


def listar_produtos_vendidos_controller(filtro=None):
    with data.closing(data.sqlite3.connect(data.DB_PATH)) as conn:
        c = conn.cursor()
        query = "SELECT * FROM produtos_vendidos WHERE 1=1"
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
                foto=row[8],
                data_venda=row[9],
                hora_venda=row[10],
            )
            for row in rows
        ]


def remover_produto_controller(codigo):
    data.remover_produto_por_codigo(codigo)


def marcar_como_vendido_controller(codigo):
    data.marcar_como_vendido(codigo)
