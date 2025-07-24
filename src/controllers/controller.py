from models import data

TIPOS_PRODUTO = [
    ("01", "BLAZER"),
    ("02", "CALÇA"),
    ("03", "CAMISA"),
    ("04", "CAMISETA"),
    ("05", "SHORT"),
    ("06", "VESTIDO"),
    ("07", "SAIA"),
    ("08", "CASACO"),
    ("09", "COLETE"),
    ("10", "CAMISA COM MANGA"),
    ("11", "JAQUETA"),
    ("12", "ROUPA DE CAMA"),
    ("13", "ROUPA DE BANHO"),
    ("14", "ROUPA ÍNTIMA"),
    ("15", "ROUPA DE FESTA"),
    ("16", "TÊNIS"),
    ("17", "SAPATO"),
    ("18", "BOTA"),
    ("19", "SANDÁLIA"),
    ("20", "CHINELO"),
    ("21", "BOLSA"),
    ("22", "CINTO"),
    ("23", "ACESSÓRIO"),
    ("24", "OUTROS"),
    ("25", "ROUPA INFANTIL"),
    ("26", "ANEL"),
    ("27", "BRINCO"),
    ("28", "COLAR"),
    ("29", "PULSEIRA"),
    ("30", "RELÓGIO"),
    ("31", "ÓCULOS"),
    ("32", "CHAPÉU"),
    ("33", "LUVAS"),
    ("34", "CACHECOL"),
    ("35", "MEIAS"),
    ("36", "ROUPA DE ESPORTE"),
    ("37", "ROUPA DE PRAIA"),
    ("38", "ROUPA DE INVERNO"),
    ("39", "ROUPA DE VERÃO"),
    ("40", "ROUPA DE OUTONO"),
    ("41", "ROUPA DE PRIMAVERA"),
    ("42", "CUECA"),
    ("43", "SUTIÃ"),
    ("44", "PANTALONA"),
    ("45", "CALÇA JEANS"),
    ("46", "CALÇA DE MOLETOM"),
    ("47", "CALÇA DE SARJA"),
    ("48", "CALÇA DE TECIDO"),
    ("49", "CALÇA DE LINHO"),
    ("50", "CALÇA DE ALGODÃO"),
    ("51", "CALÇA DE POLIÉSTER"),
    ("52", "CALÇA DE VISCOS"),
    ("53", "CALÇA DE SEDA"),
    ("54", "CALÇA DE LÃ"),
    ("55", "CALÇA DE MALHA"),
    ("56", "CALÇA DE JEANS ESCURO"),
    ("57", "CALÇA DE JEANS CLARO"),
    ("58", "SOCIAL"),
    ("59", "CASUAL"),
    ("60", "ESPORTIVO"),
    ("61", "FORMAL"),
    ("62", "DESPOJADO"),
    ("63", "CLÁSSICO"),
    ("64", "MODERNO"),
    ("65", "VINTAGE"),
]


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
    produto["codigo"] = produto["id"]

    # Verifica se já existe produto com esse código
    existentes = data.listar_produtos(filtro=produto["codigo"])
    if any(p["codigo"] == produto["codigo"] for p in existentes):
        raise ValueError("Já existe um produto com este código.")

    data.adicionar_produto(produto)


def listar_produtos_controller(filtro=None, vendidos=None):
    return data.listar_produtos(filtro=filtro, vendidos=vendidos)


def listar_produtos_vendidos_controller(filtro=None):
    items = data.listar_produtos_vendidos()
    if filtro:
        filtro = filtro.lower()
        items = [
            item
            for item in items
            if filtro in str(item.get("id", "")).lower()
            or filtro in str(item.get("tipo", "")).lower()
            or filtro in str(item.get("cor", "")).lower()
            or filtro in str(item.get("tamanho", "")).lower()
            or filtro in str(item.get("descricao", "")).lower()
        ]
    return items


def remover_produto_controller(codigo):
    data.remover_produto_por_codigo(codigo)
