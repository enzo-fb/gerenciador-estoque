import flet as ft

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
]


def update_item_view(item_data, on_salvar, on_voltar):
    tipo_valor = item_data.get("id", "")[:2] if item_data.get("id", "") else "01"
    codigo_valor = item_data.get("id", "")[2:] if item_data.get("id", "") else ""

    tipo_selector = ft.DropdownM2(
        label="Tipo",
        width=200,
        options=[ft.dropdown.Option(k, text=f"{v} ({k})") for k, v in TIPOS_PRODUTO],
        value=tipo_valor,
        bgcolor=ft.Colors.WHITE,
        color=ft.Colors.BLACK,
        border_radius=8,
        border_color="transparent",
        focused_border_color=ft.Colors.BLUE_600,
        icon=ft.Icons.ARROW_DROP_DOWN,
    )
    id_field = ft.TextField(
        label="6 dígitos finais",
        value=codigo_valor,
        width=100,
        max_length=6,
        color="#000000",
        border_color="#ffffff",
        bgcolor="#ffffff",
        label_style=ft.TextStyle(color="#808080"),
    )
    quantidade_field = ft.TextField(
        label="Quantidade",
        value=str(item_data.get("quantidade", "")),
        width=300,
        keyboard_type=ft.KeyboardType.NUMBER,
        border_color="#ffffff",
        bgcolor="#ffffff",
        color="#000000",
        label_style=ft.TextStyle(color="#808080"),
    )
    cor_field = ft.TextField(
        label="Cor",
        value=str(item_data.get("cor", "")),
        width=300,
        color="#000000",
        border_color="#ffffff",
        bgcolor="#ffffff",
        label_style=ft.TextStyle(color="#808080"),
    )
    tamanho_field = ft.TextField(
        label="Tamanho",
        value=str(item_data.get("tamanho", "")),
        width=300,
        color="#000000",
        border_color="#ffffff",
        bgcolor="#ffffff",
        label_style=ft.TextStyle(color="#808080"),
    )
    preco_field = ft.TextField(
        label="Preço",
        value=str(item_data.get("preco", "")),
        width=300,
        keyboard_type=ft.KeyboardType.NUMBER,
        color="#000000",
        border_color="#ffffff",
        bgcolor="#ffffff",
        label_style=ft.TextStyle(color="#808080"),
    )
    descricao_field = ft.TextField(
        label="Descrição",
        value=str(item_data.get("descricao", "")),
        width=300,
        multiline=True,
        min_lines=2,
        max_lines=2,
        color="#000000",
        border_color="#ffffff",
        bgcolor="#ffffff",
        label_style=ft.TextStyle(color="#808080"),
    )
    foto_path = ft.Text(
        f"Foto atual: {'definida' if item_data.get('foto') else 'Nenhuma'}",
        size=14,
        color="#666666",
    )
    foto_nova_path = [None]  # Sempre começa como None

    def on_foto_result(e: ft.FilePickerResultEvent):
        # Aja apenas se um arquivo foi realmente selecionado
        if e.files:
            foto_path.value = f"Nova foto selecionada: {e.files[0].name}"
            foto_path.color = "#228B22"
            foto_nova_path[0] = e.files[0].path
            foto_path.update()

    file_picker = ft.FilePicker()
    file_picker.on_result = on_foto_result

    adicionar_foto_btn = ft.ElevatedButton(
        "Selecionar nova foto",
        bgcolor="#808080",
        color="#ffffff",
        width=200,
        height=40,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=16)),
        on_click=lambda e: file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png"],
        ),
    )

    def salvar_atualizacao(e):
        tipo_selector.error_text = ""
        id_field.error_text = ""
        quantidade_field.error_text = ""
        preco_field.error_text = ""
        cor_field.error_text = ""
        tamanho_field.error_text = ""
        descricao_field.error_text = ""
        tipo_selector.update()
        id_field.update()
        quantidade_field.update()
        preco_field.update()
        cor_field.update()
        tamanho_field.update()
        descricao_field.update()
        erro = False

        # Validação do código: 6 dígitos
        if not id_field.value or not id_field.value.strip():
            id_field.error_text = "Campo obrigatório"
            id_field.update()
            erro = True
        elif len(id_field.value.strip()) != 6 or not id_field.value.strip().isdigit():
            id_field.error_text = "Digite exatamente 6 dígitos numéricos"
            id_field.update()
            erro = True
        else:
            id_field.error_text = None
            id_field.update()

        if erro:
            return

        try:
            novo_item = item_data.copy()
            novo_item["id"] = (tipo_selector.value or "") + (id_field.value or "")
            novo_item["codigo"] = novo_item["id"]
            novo_item["quantidade"] = int(quantidade_field.value)
            novo_item["preco"] = float(preco_field.value)
            novo_item["cor"] = cor_field.value
            novo_item["tamanho"] = tamanho_field.value
            novo_item["descricao"] = descricao_field.value
            # Se o usuário selecionou uma nova foto (caminho de arquivo), atualiza; senão, mantém o BLOB original
            if foto_nova_path[0]:
                novo_item["foto"] = foto_nova_path[
                    0
                ]  # Caminho do arquivo para ser lido e salvo como BLOB
            else:
                novo_item["foto"] = item_data.get(
                    "foto", None
                )  # Mantém o BLOB original
            novo_item["tipo"] = next(
                (v for k, v in TIPOS_PRODUTO if k == tipo_selector.value), ""
            )
            on_salvar(novo_item)
        except ValueError:
            quantidade_field.error_text = "Verifique os valores"
            quantidade_field.update()

    return ft.Stack(
        [
            ft.Column(
                [
                    ft.Text(
                        f"Atualizar item: {item_data.get('nome', item_data.get('id', ''))}",
                        size=24,
                    ),
                    ft.Row(
                        [
                            tipo_selector,
                            id_field,
                        ],
                        alignment="center",
                        spacing=10,
                    ),
                    quantidade_field,
                    preco_field,
                    cor_field,
                    tamanho_field,
                    descricao_field,
                    foto_path,
                    adicionar_foto_btn,
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Salvar",
                                on_click=salvar_atualizacao,
                                width=150,
                                height=50,
                            ),
                            ft.TextButton(
                                "Voltar", on_click=on_voltar, width=150, height=50
                            ),
                        ],
                        alignment="center",
                    ),
                ],
                alignment="center",
                horizontal_alignment="center",
            ),
            file_picker,
        ],
        expand=True,
    )
