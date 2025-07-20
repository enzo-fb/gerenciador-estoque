import flet as ft


def consult_item_view(on_voltar=None, on_ver_vendidos=None):
    search_field = ft.TextField(
        label="Buscar por código, cor, tamanho...",
        width=300,
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: update_items(),
    )
    min_value_field = ft.TextField(
        label="Valor mínimo",
        width=145,
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=lambda e: update_items(),
    )
    max_value_field = ft.TextField(
        label="Valor máximo",
        width=145,
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=lambda e: update_items(),
    )

    # Exemplo de dados estáticos (adicione o campo 'foto' se desejar)
    items = [
        {
            "codigo": "001",
            "nome": "Produto A",
            "quantidade": 10,
            "cor": "Azul",
            "tamanho": "M",
            "descricao": "Produto de alta qualidade.",
            "preco": 100,
            "foto": None,  # Substitua por caminho da imagem se houver
        },
        {
            "codigo": "002",
            "nome": "Produto B",
            "quantidade": 5,
            "cor": "Vermelho",
            "tamanho": "G",
            "descricao": "Produto resistente e durável.",
            "preco": 200,
            "foto": None,
        },
    ]

    item_column = ft.Column(
        [],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    def marcar_vendido(e, codigo):
        print(f"Produto {codigo} marcado como vendido!")
        # Aqui você pode implementar a lógica real

    detalhes_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Detalhes do Produto", weight="bold"),
        content=ft.Column([], tight=True, spacing=10),
        actions=[
            ft.TextButton(
                "Fechar",
                on_click=lambda e: fechar_dialog(e),
            )
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def fechar_dialog(e):
        page = e.page
        detalhes_dialog.open = False
        page.update()

    def mostrar_detalhes(item):
        # Garante que o dialog está na página antes de abrir
        page = item_column.page
        if not hasattr(page, "dialog") or page.dialog != detalhes_dialog:
            page.dialog = detalhes_dialog
        detalhes_dialog.title = ft.Text(
            f"Detalhes do Produto {item['codigo']}", weight="bold"
        )
        detalhes_dialog.content.controls = [
            ft.Image(
                src=item["foto"] if item["foto"] else "https://via.placeholder.com/200",
                width=200,
                height=200,
                fit=ft.ImageFit.CONTAIN,
            ),
            ft.Text(f"Código: {item['codigo']}", weight="bold"),
            ft.Text(f"Nome: {item['nome']}"),
            ft.Text(f"Cor: {item['cor']}"),
            ft.Text(f"Tamanho: {item['tamanho']}"),
            ft.Text(f"Quantidade: {item['quantidade']}"),
            ft.Text(f"Preço: R$ {item.get('preco', 0):.2f}"),
            ft.Text(f"Descrição: {item['descricao']}"),
        ]
        detalhes_dialog.open = True
        page.update()

    def item_card(item):
        return ft.Container(
            content=ft.Row(
                [
                    # Foto do produto (imagem ou placeholder)
                    ft.Container(
                        ft.Image(
                            src=(
                                item["foto"]
                                if item["foto"]
                                else "https://via.placeholder.com/100"
                            ),
                            width=100,
                            height=100,
                            fit=ft.ImageFit.COVER,
                        ),
                        width=110,
                        height=110,
                        bgcolor="#f0f0f0",
                        border_radius=8,
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(right=16),
                    ),
                    # Informações do produto
                    ft.Column(
                        [
                            ft.Text(
                                f"Código: {item['codigo']}", weight="bold", size=16
                            ),
                            ft.Text(f"Nome: {item['nome']}", size=15),
                            ft.Text(f"Cor: {item['cor']}", size=15),
                            ft.Text(f"Tamanho: {item['tamanho']}", size=15),
                            ft.Text(f"Qtd: {item['quantidade']}", size=15),
                            ft.Text(
                                f"Descrição: {item['descricao']}",
                                size=14,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.ElevatedButton(
                                "Marcar como vendido",
                                bgcolor="#228B22",
                                color="#ffffff",
                                width=180,
                                height=40,
                                style=ft.ButtonStyle(text_style=ft.TextStyle(size=16)),
                                on_click=lambda e, codigo=item[
                                    "codigo"
                                ]: marcar_vendido(e, codigo),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=2,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=16,
            margin=ft.margin.symmetric(vertical=8),
            bgcolor="#ffffff",
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=8, color="#cccccc", offset=ft.Offset(2, 2)),
            width=400,
            on_click=lambda e: mostrar_detalhes(item),
        )

    def update_items():
        termo = search_field.value.lower()
        min_val = min_value_field.value
        max_val = max_value_field.value
        try:
            min_val = float(min_val) if min_val else None
        except ValueError:
            min_val = None
        try:
            max_val = float(max_val) if max_val else None
        except ValueError:
            max_val = None

        filtered = []
        for item in items:
            if (
                termo in item["codigo"].lower()
                or termo in item["nome"].lower()
                or termo in item["cor"].lower()
                or termo in item["tamanho"].lower()
                or termo in item["descricao"].lower()
            ):
                preco = item.get("preco", 0)
                if (min_val is None or preco >= min_val) and (
                    max_val is None or preco <= max_val
                ):
                    filtered.append(item)
        item_column.controls.clear()
        for item in filtered:
            item_column.controls.append(item_card(item))
        item_column.update()

    voltar_btn = ft.ElevatedButton(
        "Voltar para menu",
        bgcolor="#6495ED",
        color="#ffffff",
        width=180,
        height=40,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=16)),
        on_click=on_voltar,
    )
    ver_vendidos_btn = ft.ElevatedButton(
        "Ver itens vendidos",
        bgcolor="#808080",
        color="#ffffff",
        width=180,
        height=40,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=16)),
        on_click=on_ver_vendidos,
    )

    # Inicializa a lista filtrada ao abrir a tela
    def on_page_load(e):
        update_items()

    view = ft.SafeArea(
        ft.Container(
            ft.Column(
                [
                    ft.Text(
                        "Consultar Estoque", size=28, weight="bold", color="#000000"
                    ),
                    search_field,
                    ft.Row(
                        [min_value_field, max_value_field],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    item_column,
                    ft.Row(
                        [voltar_btn, ver_vendidos_btn],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                expand=True,
            ),
            alignment=ft.alignment.top_center,
            bgcolor="#feffff",
            expand=True,
            padding=20,
        ),
        expand=True,
    )

    # Atualiza a lista ao carregar a página
    view.on_mount = on_page_load

    # Adiciona o dialog de detalhes à página
    def on_view_mount(e):
        page = e.page
        page.dialog = detalhes_dialog
        update_items()

    view.on_mount = on_view_mount

    return view
