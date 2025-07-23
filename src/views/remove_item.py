import flet as ft
import base64


# O parâmetro 'on_remover' foi trocado por 'on_request_remove' para maior clareza.
def remove_item_view(on_voltar=None, on_request_remove=None, on_listar=None):
    search_field = ft.TextField(
        label="Buscar por código, cor, tamanho...",
        width=420,
        prefix_icon=ft.Icons.SEARCH,
        border_color="#ffffff",  # Adicionando cor de borda
        bgcolor="#ffffff",
        color="#000000",  # Cor do texto digitado
        label_style=ft.TextStyle(color="#808080"),  # Cor do rótulo
    )

    item_column = ft.Column(
        [],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    # A função 'remover_item' foi REMOVIDA daqui.
    # A responsabilidade de remover será do arquivo principal que controla a navegação.

    def item_card(item):
        foto = item.get("foto")
        foto_ctrl = ft.Image(
            src="https://via.placeholder.com/110",
            width=110,
            height=110,
            fit=ft.ImageFit.COVER,
            border_radius=8,
        )
        if isinstance(foto, bytes) and foto:
            foto_ctrl.src_base64 = base64.b64encode(foto).decode("utf-8")

        item_id = item.get("id", "")

        text_color = "#000000"  # cor preta

        return ft.Container(
            key=item_id,
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
                                f"Código: {item_id}",
                                weight="bold",
                                size=16,
                                color=text_color,
                            ),
                            ft.Text(
                                f"Tipo: {item.get('tipo', '')}",
                                size=15,
                                color=text_color,
                            ),
                            ft.Text(
                                f"Cor: {item.get('cor', '')}", size=15, color=text_color
                            ),
                            ft.Text(
                                f"Tamanho: {item.get('tamanho', '')}",
                                size=15,
                                color=text_color,
                            ),
                            ft.Text(
                                f"Qtd: {item.get('quantidade', '')}",
                                size=15,
                                color=text_color,
                            ),
                            ft.Text(
                                f"Descrição: {item.get('descricao', '')}",
                                size=14,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                color=text_color,
                            ),
                            ft.Text(
                                f"Preço: R$ {float(item.get('preco', 0) or 0):.2f}",
                                size=14,
                                color=text_color,
                            ),
                        ],
                        spacing=2,
                        alignment=ft.MainAxisAlignment.CENTER,
                        expand=True,
                    ),
                    # --- ALTERAÇÃO NO BOTÃO ---
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color=ft.Colors.RED_700,
                        tooltip="Remover item",
                        # 1. Guarda o ID do item no próprio botão
                        data=item_id,
                        # 2. Chama a função de callback externa
                        on_click=on_request_remove,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                width=420,
            ),
            padding=16,
            margin=ft.margin.symmetric(vertical=8),
            bgcolor="#f5f5f5",
            border_radius=12,
            shadow=ft.BoxShadow(
                blur_radius=5, color="#00000020", offset=ft.Offset(1, 1)
            ),
        )

    # Nenhuma alteração daqui para baixo no restante do arquivo.
    def update_items():
        termo = search_field.value.lower() if search_field.value else ""
        items = on_listar(termo) if on_listar else []
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
        item_column.controls.clear()
        if not filtered:
            item_column.controls.append(ft.Text("Nenhum item encontrado.", size=18))
        else:
            for item in filtered:
                item_column.controls.append(item_card(item))
        item_column.update()

    search_field.on_change = lambda e: update_items()

    voltar_btn = ft.ElevatedButton(
        "Voltar para menu",
        bgcolor="#6495ED",
        color="#ffffff",
        width=420,
        height=50,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)),
        on_click=on_voltar,
    )

    view_content = ft.SafeArea(
        ft.Container(
            ft.Column(
                [
                    ft.Text(
                        "Remover Item do Estoque",
                        size=28,
                        weight="bold",
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
            expand=True,
            padding=20,
        ),
        expand=True,
    )

    # Este código está usando o padrão on_mount, o que é ótimo.
    # Vou mantê-lo, pois é mais limpo.
    def on_view_mount(e):
        update_items()

    view_content.on_mount = on_view_mount

    # O retorno da função é alterado para se adequar ao on_mount.
    # Se você preferir o outro padrão, me avise.
    return view_content, update_items
