import flet as ft
import base64


def update_select_view(on_voltar, produtos, on_editar):
    items = []

    # --- A FUNÇÃO item_card PERMANECE EXATAMENTE IGUAL ---
    def item_card(item):
        foto = item.get("foto")
        foto_ctrl = None

        if isinstance(foto, bytes) and foto:
            foto_base64 = base64.b64encode(foto).decode("utf-8")
            foto_ctrl = ft.Image(
                src_base64=foto_base64, width=100, height=100, fit=ft.ImageFit.COVER
            )
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
                                f"Preço: R$ {float(item.get('preco', 0) or 0):.2f}",
                                size=14,
                                color="#000000",
                            ),
                            ft.Text(
                                f"Descrição: {item.get('descricao', '')}",
                                color="#000000",
                                size=14,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=2,
                        expand=True,
                    ),
                    ft.Column(
                        [
                            ft.IconButton(
                                icon=ft.Icons.EDIT_NOTE_ROUNDED,
                                icon_color=ft.Colors.ORANGE_700,
                                icon_size=40,
                                tooltip="Editar este item",
                                on_click=lambda e: on_editar(item),
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=16,
            margin=ft.margin.symmetric(vertical=8),
            bgcolor="#f5f5f5",
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=8, color="#cccccc", offset=ft.Offset(2, 2)),
            width=500,
        )

    # A lista é construída aqui, de forma síncrona
    for produto in produtos:
        items.append(item_card(produto))

    lista = ft.Column(items, scroll=ft.ScrollMode.AUTO, expand=True)

    view = ft.Column(
        [
            ft.Text(
                "Selecione um item para atualizar",
                size=24,
                weight="bold",
                text_align=ft.TextAlign.CENTER,
            ),
            lista,
            ft.ElevatedButton("Voltar", on_click=on_voltar, width=300, height=50),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    container = ft.SafeArea(
        ft.Container(view, alignment=ft.alignment.center, padding=16), expand=True
    )

    # Não há mais on_mount nem função de retorno para atualizar a lista
    return container
