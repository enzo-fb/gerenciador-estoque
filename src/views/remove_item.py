import flet as ft


def remove_item_view(on_voltar=None):
    search_field = ft.TextField(
        label="Buscar por código, nome, cor...",
        width=300,
        prefix_icon=ft.Icons.SEARCH,
    )

    # Exemplo de dados estáticos (substitua depois por dados reais)
    items = [
        {
            "codigo": "001",
            "nome": "Produto A",
            "cor": "Azul",
            "tamanho": "M",
            "descricao": "Produto de alta qualidade.",
            "foto": None,  # Adicione o campo foto
        },
        {
            "codigo": "002",
            "nome": "Produto B",
            "cor": "Vermelho",
            "tamanho": "G",
            "descricao": "Produto resistente e durável.",
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

    def remover_item(e, codigo):
        print(f"Remover produto {codigo}")
        # Aqui você pode implementar a lógica real

    def item_card(item):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        ft.Image(
                            src=(
                                item["foto"]
                                if item.get("foto")
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
                    ft.Column(
                        [
                            ft.Text(
                                f"Código: {item['codigo']}", weight="bold", size=16
                            ),
                            ft.Text(f"Nome: {item['nome']}", size=15),
                            ft.Text(f"Cor: {item['cor']}", size=15),
                            ft.Text(f"Tamanho: {item['tamanho']}", size=15),
                            ft.Text(
                                f"Descrição: {item['descricao']}",
                                size=14,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.ElevatedButton(
                                "Remover",
                                bgcolor="#B22222",
                                color="#ffffff",
                                width=180,
                                height=40,
                                style=ft.ButtonStyle(text_style=ft.TextStyle(size=16)),
                                on_click=lambda e, codigo=item["codigo"]: remover_item(
                                    e, codigo
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=6,
                        width=230,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=16,
            margin=ft.margin.symmetric(vertical=10),
            bgcolor="#ffffff",
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=8, color="#cccccc", offset=ft.Offset(2, 2)),
            width=420,
        )

    def update_items():
        termo = search_field.value.lower()
        filtered = []
        for item in items:
            if (
                termo in item["codigo"].lower()
                or termo in item["nome"].lower()
                or termo in item["cor"].lower()
                or termo in item["tamanho"].lower()
                or termo in item["descricao"].lower()
            ):
                filtered.append(item)
        item_column.controls.clear()
        for item in filtered:
            item_column.controls.append(item_card(item))
        item_column.update()

    search_field.on_change = lambda e: update_items()

    voltar_btn = ft.ElevatedButton(
        "Voltar para menu",
        bgcolor="#6495ED",
        color="#ffffff",
        width=300,
        height=50,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)),
        on_click=on_voltar,
    )

    def on_mount(e):
        update_items()

    container = ft.Container(
        ft.Column(
            [
                ft.Text(
                    "Remover Item do Estoque",
                    size=28,
                    weight="bold",
                    color="#000000",
                ),
                search_field,
                item_column,
                voltar_btn,
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
    )
    container.on_mount = on_mount

    return ft.SafeArea(
        container,
        expand=True,
    )
