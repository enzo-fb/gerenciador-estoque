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
    "10": "CAMISA COM MANGA",
    "11": "JAQUETA",
    "12": "ROUPA DE CAMA",
    "13": "ROUPA DE BANHO",
    "14": "ROUPA ÍNTIMA",
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


def marcar_como_vendido_controller(codigo):
    data.marcar_como_vendido(codigo)
    # Não coloque prints, chamadas duplicadas, ou comentários de debug aqui!
    # Remova qualquer chamada duplicada ou print!
    # Nenhum print ou chamada extra aqui.
    data.marcar_como_vendido(codigo)

    vendidos = data.listar_produtos_vendidos()
    print(f"Agora temos {len(vendidos)} itens vendidos no banco")
