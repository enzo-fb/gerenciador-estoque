import flet as ft
import base64


def sold_item_view(on_voltar=None, on_listar_vendidos=None):
    search_field = ft.TextField(
        label="Buscar por código, cor, tipo...",
        width=300,
        prefix_icon=ft.Icons.SEARCH,
    )

    contador = ft.Text("Total de itens vendidos: 0", size=16)
    items_column = ft.Column(
        [],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    def item_card(item):
        foto = item.get("foto")
        if isinstance(foto, bytes) and foto:
            foto_base64 = base64.b64encode(foto).decode("utf-8")
            foto_ctrl = ft.Image(
                src_base64=foto_base64, width=100, height=100, fit=ft.ImageFit.COVER
            )
        elif foto and not str(foto).startswith("http"):
            foto_ctrl = ft.Image(
                src=f"file://{foto}", width=100, height=100, fit=ft.ImageFit.COVER
            )
        else:
            foto_ctrl = ft.Image(
                src=foto or "https://via.placeholder.com/100", width=100, height=100, fit=ft.ImageFit.COVER
            )
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        foto_ctrl,
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
                                f"Cor: {item.get('cor', '')}", size=15, color="#000000"
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
                                f"Preço: R$ {float(item.get('preco', 0) or 0):.2f}",
                                size=14,
                                color="#000000",
                            ),
                            ft.Text(
                                f"Data: {item.get('data_venda', '')}",
                                size=14,
                                color="#000000",
                            ),
                            ft.Text(
                                f"Hora: {item.get('hora_venda', '')}",
                                size=14,
                                color="#000000",
                            ),
                            ft.Text(
                                f"Descrição: {item.get('descricao', '')}",
                                size=14,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                color="#000000",
                            ),
                        ],
                        spacing=5,
                        alignment=ft.MainAxisAlignment.START,
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
        items = on_listar_vendidos(termo) if on_listar_vendidos else []
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
            filtered = items

        contador.value = f"Total de itens vendidos: {len(filtered)}"
        items_column.controls.clear()
        if filtered:
            for item in filtered:
                items_column.controls.append(item_card(item))
        else:
            items_column.controls.append(
                ft.Text("Nenhum item vendido encontrado.", color="red", size=18)
            )
        contador.update()
        items_column.update()

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

    container = ft.Container(
        ft.Column(
            [
                ft.Text(
                    "Itens Vendidos",
                    size=28,
                    weight="bold",
                    text_align=ft.TextAlign.CENTER,
                ),
                search_field,
                contador,
                items_column,
                voltar_btn,
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,  # Adicionado para expandir a coluna
        ),
        padding=20,
        expand=True,  # Adicionado para expandir o container
        alignment=ft.alignment.center,
    )

    def on_mount(e):
        update_items()

    container.on_mount = on_mount

    return ft.SafeArea(container, expand=True)  # Adicionado expand=True no SafeArea
