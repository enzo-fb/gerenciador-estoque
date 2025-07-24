import flet as ft


def home_view(
    on_add_item=None,
    on_remove_item=None,
    on_consult_item=None,
    on_sold_items=None,
    on_sell_item=None,
    on_update_item=None,
    on_backup=None,
    on_tema=None,  # Novo parâmetro para callback do tema
):
    """Cria a view da tela inicial com um layout de grade 2x3 manual e centralizado."""

    button_data = [
        {
            "icon": ft.Icons.POINT_OF_SALE_ROUNDED,
            "text": "Vender Item",
            "on_click": on_sell_item,
        },
        {
            "icon": ft.Icons.ADD_SHOPPING_CART_ROUNDED,
            "text": "Adicionar Item",
            "on_click": on_add_item,
        },
        {
            "icon": ft.Icons.EDIT_NOTE_ROUNDED,
            "text": "Atualizar Item",
            "on_click": on_update_item,
        },
        {
            "icon": ft.Icons.SEARCH_ROUNDED,
            "text": "Consultar Item",
            "on_click": on_consult_item,
        },
        {
            "icon": ft.Icons.REMOVE_SHOPPING_CART_OUTLINED,
            "text": "Remover Item",
            "on_click": on_remove_item,
        },
        {
            "icon": ft.Icons.PRICE_CHECK_ROUNDED,
            "text": "Itens Vendidos",
            "on_click": on_sold_items,
        },
        # Remova o botão de backup da lista principal
        # {
        #     "icon": ft.Icons.BACKUP_OUTLINED,
        #     "text": "Backup",
        #     "on_click": on_backup,
        # },
    ]

    def create_menu_card(button_info: dict):
        """Cria um card de menu clicável com ícone e texto."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(name=button_info["icon"], size=40, color=ft.Colors.WHITE),
                    ft.Container(height=10),
                    ft.Text(
                        value=button_info["text"],
                        size=16,
                        weight="bold",
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=150,
            height=150,
            bgcolor=ft.Colors.BLUE_GREY_700,
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.BLACK26,
                offset=ft.Offset(2, 2),
            ),
            on_click=button_info["on_click"],
            ink=True,
        )

    # Layout manual para a grade 2x3 (sem backup)
    button_layout = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    create_menu_card(button_data[0]),
                    create_menu_card(button_data[1]),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            ft.Row(
                controls=[
                    create_menu_card(button_data[2]),
                    create_menu_card(button_data[3]),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            ft.Row(
                controls=[
                    create_menu_card(button_data[4]),
                    create_menu_card(button_data[5]),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
        ],
        spacing=20,
    )

    # Botão de backup apenas ícone, posicionado no canto inferior direito
    backup_icon_btn = ft.IconButton(
        icon=ft.Icons.BACKUP_OUTLINED,
        icon_color=ft.Colors.BLUE_GREY_700,
        tooltip="Backup",
        on_click=on_backup,
        width=56,
        height=56,
        style=ft.ButtonStyle(shape=ft.CircleBorder()),
    )

    tema_icon_btn = ft.IconButton(
        icon=ft.Icons.DARK_MODE_OUTLINED,
        icon_color=ft.Colors.BLUE_GREY_700,
        tooltip="Alternar tema",
        on_click=on_tema,
        width=56,
        height=56,
        style=ft.ButtonStyle(shape=ft.CircleBorder()),
    )

    # Coloque os botões de tema e backup na parte superior usando uma Row antes do conteúdo principal.
    return ft.SafeArea(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            backup_icon_btn,
                            alignment=ft.alignment.top_left,
                            padding=ft.Padding(
                                20, 10, 0, 0
                            ),  # padding: left, top, right, bottom
                        ),
                        ft.Container(
                            tema_icon_btn,
                            alignment=ft.alignment.top_right,
                            padding=ft.Padding(
                                0, 10, 20, 0
                            ),  # padding: left, top, right, bottom
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Image(src="splash_android.png", width=160, height=160),
                            ft.Text("Controle de Estoque", size=32, weight="bold"),
                            ft.Container(height=5),  # diminui o espaço
                            button_layout,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True,
                    ),
                    alignment=ft.alignment.top_center,  # sobe o menu
                    padding=ft.Padding(
                        20, -45, 20, 40
                    ),  # padding: left, top, right, bottom
                    expand=True,
                ),
            ],
            expand=True,
        )
    )
