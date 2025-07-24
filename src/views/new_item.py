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


def new_item_view(on_voltar=None, on_salvar=None, on_sucesso=None):

    tipo_selector = ft.DropdownM2(
        label="Tipo",
        width=200,  # Um pouco mais de espaço para o ícone
        options=[ft.dropdown.Option(k, text=f"{v} ({k})") for k, v in TIPOS_PRODUTO],
        value="01",
        # --- Estilo Visual Melhorado ---
        bgcolor=ft.Colors.WHITE,
        color=ft.Colors.BLACK,
        border_radius=8,
        border_color="transparent",  # Borda invisível quando não focado
        focused_border_color=ft.Colors.BLUE_600,  # Borda azul ao focar
        icon=ft.Icons.ARROW_DROP_DOWN,
    )
    id_field = ft.TextField(
        label="6 dígitos finais",
        width=100,
        max_length=6,
        color="#000000",
        border_color="#ffffff",  # Adicionando cor de borda
        bgcolor="#ffffff",
        label_style=ft.TextStyle(color="#808080"),  # Cor do rótulo
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    quantidade_field = ft.TextField(
        label="Quantidade",
        width=300,
        keyboard_type=ft.KeyboardType.NUMBER,
        border_color="#ffffff",  # Adicionando cor de borda
        bgcolor="#ffffff",
        color="#000000",  # Cor do texto digitado
        label_style=ft.TextStyle(color="#808080"),  # Cor do rótulo
    )
    cor_field = ft.TextField(
        label="Cor",
        width=300,
        color="#000000",
        border_color="#ffffff",  # Adicionando cor de borda
        bgcolor="#ffffff",
        label_style=ft.TextStyle(color="#808080"),  # Cor do rótulo
    )
    tamanho_field = ft.TextField(
        label="Tamanho",
        width=300,
        color="#000000",
        border_color="#ffffff",  # Adicionando cor de borda
        bgcolor="#ffffff",
        label_style=ft.TextStyle(color="#808080"),  # Cor do rótulo
    )
    preco_field = ft.TextField(
        label="Preço",
        width=300,
        keyboard_type=ft.KeyboardType.NUMBER,
        color="#000000",
        border_color="#ffffff",  # Adicionando cor de borda
        bgcolor="#ffffff",
        label_style=ft.TextStyle(color="#808080"),  # Cor do rótulo
    )
    descricao_field = ft.TextField(
        label="Descrição",
        width=300,
        multiline=True,
        min_lines=2,
        max_lines=2,
        color="#000000",
        border_color="#ffffff",  # Adicionando cor de borda
        bgcolor="#ffffff",
        label_style=ft.TextStyle(color="#808080"),  # Cor do rótulo
    )
    foto_path = ft.Text("", size=14)
    foto_real_path = [None]  # Usado para armazenar o caminho real do arquivo

    instrucoes_camera = ft.Text(
        "Use o aplicativo de câmera do seu dispositivo para tirar a foto e depois clique em 'Adicionar Foto' para selecionar.",
        size=12,
        italic=True,
        text_align=ft.TextAlign.CENTER,
    )

    def on_foto_result(e: ft.FilePickerResultEvent):
        if e.files:
            foto_path.value = f"Foto selecionada: {e.files[0].name}"
            foto_path.color = "#228B22"
            foto_real_path[0] = e.files[0].path  # Salva o caminho real do arquivo
            foto_path.update()
        else:
            foto_path.value = ""
            foto_path.color = "#666666"
            foto_real_path[0] = None
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
        foto_real_path[0] = None
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
            try:
                # Corrige: o campo "quantidade" deve ser convertido para int, "preco" para float
                on_salvar(
                    {
                        "id": gerar_id_completo(),
                        "codigo": gerar_id_completo(),
                        "tipo": next(
                            (v for k, v in TIPOS_PRODUTO if k == tipo_selector.value),
                            "",
                        ),
                        "quantidade": int(quantidade_field.value or "0"),
                        "cor": cor_field.value,
                        "tamanho": tamanho_field.value,
                        "preco": float(preco_field.value or "0"),
                        "descricao": descricao_field.value,
                        "foto": foto_real_path[0],  # Salva o caminho real do arquivo
                    }
                )
            except Exception as ex:
                id_field.error_text = str(ex)
                id_field.update()
                return
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
                    ft.Text("Adicionar Novo Item", size=28, weight="bold"),
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
                    foto_path,
                    adicionar_foto_btn,  # Botão para selecionar arquivo
                    instrucoes_camera,
                    salvar_btn,
                    voltar_btn,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                expand=True,  # Adicionado para expandir a coluna
            ),
            alignment=ft.alignment.center,
            expand=True,  # Adicionado para expandir o container
            padding=20,
        ),
        expand=True,  # Adicionado para expandir o SafeArea
    )
    return ft.Stack(
        [layout, file_picker], expand=True
    )  # Adicionado expand=True no Stack
