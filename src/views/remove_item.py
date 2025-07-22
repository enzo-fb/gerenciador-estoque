import flet as ft
import base64

import flet as ft
import base64


def remove_item_view(on_voltar=None, on_remover=None, on_listar=None):
    search_field = ft.TextField(
        label="Buscar por código, cor, tamanho...",
        width=420,  # Largura ajustada
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
        update_items()

    # --- ALTERAÇÃO DE LAYOUT AQUI ---
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

        return ft.Container(
            key=item_id,
            content=ft.Row(
                [
                    # Elemento 1: Imagem (sem alterações)
                    ft.Container(
                        foto_ctrl,
                        width=110,
                        height=110,
                        bgcolor="#f0f0f0",
                        border_radius=8,
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(
                            right=16
                        ),  # Mantém a distância da imagem para o texto
                    ),
                    # Elemento 2: Coluna de Textos (MODIFICADO)
                    ft.Column(
                        [
                            ft.Text(
                                f"Código: {item_id}",
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
                        ],
                        spacing=2,
                        alignment=ft.MainAxisAlignment.CENTER,
                        # A propriedade expand=True faz esta coluna crescer e ocupar todo o espaço
                        # disponível no meio, empurrando o ícone para a direita.
                        expand=True,
                    ),
                    # Elemento 3: Botão de Lixeira (MOVIDO)
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color=ft.Colors.RED_700,
                        tooltip="Remover item",
                        on_click=lambda e, codigo=item_id: remover_item(e, codigo),
                    ),
                ],
                # Alinha verticalmente a imagem, o bloco de texto e o ícone no centro.
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                # Garante que a largura do card seja consistente
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

    # --- FIM DA ALTERAÇÃO ---

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
            item_column.controls.append(
                ft.Text("Nenhum item encontrado.", color="red", size=18)
            )
        else:
            for item in filtered:
                item_column.controls.append(item_card(item))
        item_column.update()

    search_field.on_change = lambda e: update_items()

    voltar_btn = ft.ElevatedButton(
        "Voltar para menu",
        bgcolor="#6495ED",
        color="#ffffff",
        width=420,  # Largura ajustada
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
        ),
        expand=True,
    )

    def on_view_mount(e):
        update_items()

    view_content.on_mount = on_view_mount

    return view_content, update_items
