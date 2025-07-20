import flet as ft


def new_item_view(on_voltar=None, on_salvar=None, on_sucesso=None):
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

    tipo_selector = ft.Dropdown(
        label="Tipo",
        width=150,
        options=[ft.dropdown.Option(k, text=f"{v} ({k})") for k, v in TIPOS_PRODUTO],
        value="01",
    )
    id_field = ft.TextField(
        label="6 dígitos finais", width=150, max_length=6  # 'required' removido
    )
    quantidade_field = ft.TextField(
        label="Quantidade", width=300, keyboard_type=ft.KeyboardType.NUMBER
    )
    cor_field = ft.TextField(
        label="Cor",
        width=300,
        # 'required' removido
    )
    tamanho_field = ft.TextField(
        label="Tamanho",
        width=300,
        # 'required' removido
    )
    preco_field = ft.TextField(
        label="Preço",
        width=300,
        keyboard_type=ft.KeyboardType.NUMBER,  # 'required' removido
    )
    descricao_field = ft.TextField(
        label="Descrição", width=300, multiline=True, min_lines=2, max_lines=2
    )
    foto_path = ft.Text("", size=14, color="#666666")

    def on_foto_result(e: ft.FilePickerResultEvent):
        if e.files:
            foto_path.value = f"Foto selecionada: {e.files[0].name}"
            foto_path.color = "#228B22"
            foto_path.update()
        else:
            foto_path.value = ""
            foto_path.color = "#666666"
            foto_path.update()

    file_picker = ft.FilePicker()
    file_picker.on_result = on_foto_result

    adicionar_foto_btn = ft.ElevatedButton(
        "Adicionar Foto",
        bgcolor="#808080",
        color="#ffffff",
        width=250,
        height=50,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)),
        on_click=lambda e: file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png"],
        ),
    )

    def limpar_campos():
        tipo_selector.value = "01"
        id_field.value = ""
        quantidade_field.value = ""
        cor_field.value = ""
        tamanho_field.value = ""
        preco_field.value = ""
        descricao_field.value = ""
        foto_path.value = ""
        tipo_selector.update()
        id_field.update()
        quantidade_field.update()
        cor_field.update()
        tamanho_field.update()
        preco_field.update()
        descricao_field.update()
        foto_path.update()

    def salvar_item(e):
        # Validação obrigatória dos campos
        campos_obrigatorios = [
            (id_field, "ID"),
            (cor_field, "Cor"),
            (tamanho_field, "Tamanho"),
            (preco_field, "Preço"),
        ]
        erro = False

        # Validação especial para o campo ID: deve ter exatamente 6 dígitos
        if not id_field.value or not id_field.value.strip():
            id_field.error_text = "Campo obrigatório"
            id_field.update()
            erro = True
        elif len(id_field.value.strip()) != 6 or not id_field.value.strip().isdigit():
            id_field.error_text = "Digite exatamente 6 \ndígitos numéricos"
            id_field.update()
            erro = True
        else:
            id_field.error_text = None
            id_field.update()

        # Validação dos outros campos obrigatórios
        for campo, nome in campos_obrigatorios[1:]:
            if not campo.value or not campo.value.strip():
                campo.error_text = f"Campo obrigatório"
                campo.update()
                erro = True
            else:
                campo.error_text = None
                campo.update()
        if erro:
            return

        if on_salvar:
            on_salvar(
                {
                    "id": gerar_id_completo(),
                    "quantidade": quantidade_field.value,
                    "cor": cor_field.value,
                    "tamanho": tamanho_field.value,
                    "preco": preco_field.value,
                    "descricao": descricao_field.value,
                    "foto": foto_path.value if foto_path.value else None,
                }
            )
            limpar_campos()
            if on_sucesso:
                on_sucesso()

    salvar_btn = ft.ElevatedButton(
        "Salvar",
        bgcolor="#228B22",
        color="#ffffff",
        width=300,
        height=50,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)),
        on_click=salvar_item,
    )
    voltar_btn = ft.ElevatedButton(
        "Voltar para menu",
        bgcolor="#6495ED",
        color="#ffffff",
        width=300,
        height=50,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)),
        on_click=on_voltar,
    )

    def gerar_id_completo():
        return (tipo_selector.value or "") + (id_field.value or "")

    layout = ft.SafeArea(
        ft.Container(
            ft.Column(
                [
                    ft.Text(
                        "Adicionar Novo Item", size=28, weight="bold", color="#000000"
                    ),
                    ft.Row(
                        [
                            tipo_selector,
                            id_field,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    quantidade_field,
                    cor_field,
                    tamanho_field,
                    preco_field,
                    descricao_field,
                    foto_path,  # Mostra info da foto selecionada acima do botão
                    adicionar_foto_btn,
                    salvar_btn,
                    voltar_btn,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                expand=True,
            ),
            alignment=ft.alignment.center,
            bgcolor="#feffff",
            expand=True,
            padding=20,
        ),
        expand=True,
    )
    return ft.Stack([layout, file_picker])
