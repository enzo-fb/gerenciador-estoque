import flet as ft


def home_view(
    on_add_item=None,
    on_remove_item=None,
    on_consult_item=None,
    on_sold_items=None,
    on_sell_item=None,
    on_update_item=None,
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

    # Layout manual para a grade 2x3
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

    return ft.SafeArea(
        ft.Container(
            content=ft.Column(
                [
                    ft.Image(src="splash_android.png", width=160, height=160),
                    ft.Text("Controle de Estoque", size=32, weight="bold"),
                    ft.Container(height=20),
                    button_layout,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            alignment=ft.alignment.center,
            padding=20,
            expand=True,
        )
    )
