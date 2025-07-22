import flet as ft
import base64

# from models.data import salvar_blob_em_arquivo # Comentei/removi se não estiver em uso para src_base64


# O parâmetro on_marcar_vendido foi removido
def consult_item_view(
    on_voltar=None,
    on_listar=None,
):
    # Diálogo de detalhes (declarado aqui para ser acessível)
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

    search_field = ft.TextField(
        label="Buscar por código, cor, tamanho...",
        width=300,
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: update_items(),
        border_color="#ffffff",
        bgcolor="#ffffff",
        color="#000000",
        label_style=ft.TextStyle(color="#808080"),
    )
    min_value_field = ft.TextField(
        label="Valor mínimo",
        width=145,
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=lambda e: update_items(),
        border_color="#ffffff",
        bgcolor="#ffffff",
        color="#000000",
        label_style=ft.TextStyle(color="#808080"),
    )
    max_value_field = ft.TextField(
        label="Valor máximo",
        width=145,
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=lambda e: update_items(),
        border_color="#ffffff",
        bgcolor="#ffffff",
        color="#000000",
        label_style=ft.TextStyle(color="#808080"),
    )

    item_column = ft.Column(
        [],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    # A função marcar_vendido foi REMOVIDA
    # def marcar_vendido(e, codigo): ...

    def fechar_dialog(e):
        page_instance = e.page
        detalhes_dialog.open = False
        page_instance.update()

    def mostrar_detalhes(e, item):
        page_instance = e.page
        foto = item.get("foto")
        foto_ctrl = None
        if isinstance(foto, bytes) and foto:
            foto_base64 = base64.b64encode(foto).decode("utf-8")
            foto_ctrl = ft.Image(
                src_base64=foto_base64, width=300, height=300, fit=ft.ImageFit.CONTAIN
            )
        elif foto and not str(foto).startswith("http"):
            foto_ctrl = ft.Image(
                src=foto, width=300, height=300, fit=ft.ImageFit.CONTAIN
            )
        else:
            foto_ctrl = ft.Image(
                src=foto or "https://via.placeholder.com/200",
                width=300,
                height=300,
                fit=ft.ImageFit.CONTAIN,
            )

        detalhes_dialog.title = ft.Text(
            f"Detalhes do Produto {item.get('id', '')}", weight="bold"
        )
        detalhes_dialog.content.controls = [
            foto_ctrl,
            ft.Text(f"Código: {item.get('id', '')}", weight="bold"),
            ft.Text(f"Tipo: {item.get('tipo', '')}"),
            ft.Text(f"Cor: {item.get('cor', '')}"),
            ft.Text(f"Tamanho: {item.get('tamanho', '')}"),
            ft.Text(f"Quantidade: {item.get('quantidade', '')}"),
            ft.Text(f"Preço: R$ {item.get('preco', 0):.2f}"),
            ft.Text(f"Descrição: {item.get('descricao', '')}"),
        ]
        detalhes_dialog.open = True
        page_instance.dialog = detalhes_dialog
        page_instance.update()

    def item_card(item):
        foto = item.get("foto")
        foto_ctrl = None
        if isinstance(foto, bytes) and foto:
            foto_base64 = base64.b64encode(foto).decode("utf-8")
            foto_ctrl = ft.Image(
                src_base64=foto_base64, width=100, height=100, fit=ft.ImageFit.COVER
            )
        elif foto and not str(foto).startswith("http"):
            foto_ctrl = ft.Image(src=foto, width=100, height=100, fit=ft.ImageFit.COVER)
        else:
            foto_ctrl = ft.Image(
                src=foto or "https://via.placeholder.com/100",
                width=100,
                height=100,
                fit=ft.ImageFit.COVER,
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
                                f"Descrição: {item.get('descricao', '')}",
                                color="#000000",
                                size=14,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.Text(
                                f"Preço: R$ {float(item.get('preco', 0) or 0):.2f}",
                                size=14,
                                color="#000000",
                            ),
                            # --- O BOTÃO "Marcar como vendido" FOI REMOVIDO DAQUI ---
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=2,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=16,
            margin=ft.margin.symmetric(vertical=8),
            bgcolor="#f5f5f5",
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=8, color="#cccccc", offset=ft.Offset(2, 2)),
            width=400,
            on_click=lambda e_click: mostrar_detalhes(e_click, item),
        )

    # O resto do arquivo permanece exatamente como você enviou.
    def update_items():
        termo = search_field.value.lower() if search_field.value else ""
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
        items = on_listar(termo) if on_listar else []
        filtered = []
        for item in items:
            preco = item.get("preco", 0)
            if (min_val is None or preco >= min_val) and (
                max_val is None or preco <= max_val
            ):
                filtered.append(item)
        item_column.controls.clear()
        if not filtered:
            item_column.controls.append(
                ft.Text("Nenhum item encontrado.", color="red", size=18)
            )
        else:
            for item in filtered:
                item_column.controls.append(item_card(item))
        item_column.update()

    voltar_btn = ft.ElevatedButton(
        "Voltar para menu",
        bgcolor="#6495ED",
        color="#ffffff",
        width=300,
        height=40,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=16)),
        on_click=on_voltar,
    )

    view_content = ft.SafeArea(
        ft.Container(
            ft.Column(
                [
                    ft.Text(
                        "Consultar Estoque", size=28, weight="bold", color="#ffffff"
                    ),
                    search_field,
                    ft.Row(
                        [min_value_field, max_value_field],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    item_column,
                    ft.Row(
                        [voltar_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=20
                    ),
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

    def on_view_mount(e):
        page = e.page
        page.dialog = detalhes_dialog
        update_items()

    view_content.on_mount = on_view_mount

    return view_content, update_items
