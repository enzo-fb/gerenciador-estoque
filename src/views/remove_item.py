import flet as ft


def remove_item_view(on_voltar=None, on_remover=None, on_listar=None):
    search_field = ft.TextField(
        label="Buscar por código, cor, tamanho...",
        width=300,
        prefix_icon=ft.Icons.SEARCH,
    )

    item_column = ft.Column(
        [],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    def remover_item(e, codigo):
        if on_remover:
            on_remover(codigo)
        # Aguarda a operação e remove visualmente o card imediatamente
        update_items()

    def item_card(item):
        foto = item.get("foto")
        if foto and not foto.startswith("http"):
            foto_src = f"file://{foto}"
        else:
            foto_src = foto or "https://via.placeholder.com/100"
        return ft.Container(
            key=item.get("id", ""),  # chave única para facilitar atualização
            content=ft.Row(
                [
                    ft.Container(
                        ft.Image(
                            src=foto_src,
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
                                f"Código: {item.get('id', '')}",
                                weight="bold",
                                size=16,
                                color="#000000",
                            ),
                            ft.Text(
                                f"Tipo: {item.get('tipo', '')}",
                                size=15,
                                color="#000000",
                            ),
                            ft.Text(
                                f"Cor: {item.get('cor', '')}",
                                size=15,
                                color="#000000",
                            ),
                            ft.Text(
                                f"Tamanho: {item.get('tamanho', '')}",
                                size=15,
                                color="#000000",
                            ),
                            ft.Text(
                                f"Qtd: {item.get('quantidade', '')}",
                                size=15,
                                color="#000000",
                            ),
                            ft.Text(
                                f"Descrição: {item.get('descricao', '')}",
                                size=14,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                color="#000000",
                            ),
                            ft.Text(
                                f"Preço: R$ {float(item.get('preco', 0) or 0):.2f}",
                                size=14,
                                color="#000000",
                            ),
                            ft.ElevatedButton(
                                "Remover",
                                bgcolor="#B22222",
                                color="#ffffff",
                                width=180,
                                height=40,
                                style=ft.ButtonStyle(text_style=ft.TextStyle(size=16)),
                                on_click=lambda e, codigo=item.get(
                                    "codigo", item.get("id", "")
                                ): remover_item(e, codigo),
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
            bgcolor="#f5f5f5",  # Alterado para cinza claro
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=8, color="#cccccc", offset=ft.Offset(2, 2)),
            width=420,
        )

    def update_items():
        termo = search_field.value.lower() if search_field.value else ""
        items = on_listar() if on_listar else []

        # Aplica filtro de texto apenas se houver um termo
        if termo:
            filtered = [
                item
                for item in items
                if termo in str(item.get("id", "")).lower()
                or termo in str(item.get("tipo", "")).lower()
                or termo in str(item.get("cor", "")).lower()
                or termo in str(item.get("tamanho", "")).lower()
                or termo in str(item.get("descricao", "")).lower()
            ]
        else:
            # Se não houver termo, mostra todos os itens
            filtered = items

        item_column.controls.clear()
        if not filtered:
            item_column.controls.append(
                ft.Text("Nenhum item encontrado.", color="red", size=18)
            )
        else:
            for item in filtered:
                item_column.controls.append(item_card(item))
        item_column.update()
        if item_column.page:
            item_column.page.update()

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
            expand=True,  # Adicionado para expandir a coluna
        ),
        alignment=ft.alignment.top_center,
        bgcolor="#feffff",
        expand=True,  # Adicionado para expandir o container
        padding=20,
    )
    container.on_mount = on_mount

    return ft.SafeArea(
        container,
        expand=True,  # Adicionado para expandir o SafeArea
    )
