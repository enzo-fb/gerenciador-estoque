import flet as ft


def home_view(
    on_add_item=None, on_remove_item=None, on_consult_item=None, on_sold_items=None
):

    # Os dados e a função para criar os cards continuam os mesmos,
    # pois é uma ótima prática de organização.
    button_data = [
        {
            "icon": ft.Icons.ADD_SHOPPING_CART_ROUNDED,
            "text": "Adicionar Item",
            "on_click": on_add_item,
        },
        {
            "icon": ft.Icons.REMOVE_SHOPPING_CART_OUTLINED,
            "text": "Remover Item",
            "on_click": on_remove_item,
        },
        {
            "icon": ft.Icons.SEARCH_ROUNDED,
            "text": "Consultar Item",
            "on_click": on_consult_item,
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
                        color=ft.Colors.WHITE,
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

    button_layout = ft.Column(
        controls=[
            # Primeira linha de cards
            ft.Row(
                controls=[
                    create_menu_card(button_data[0]),
                    create_menu_card(button_data[1]),
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza os 2 cards na linha
                spacing=20,  # Espaço horizontal entre os cards
            ),
            # Segunda linha de cards
            ft.Row(
                controls=[
                    create_menu_card(button_data[2]),
                    create_menu_card(button_data[3]),
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza os 2 cards na linha
                spacing=20,  # Espaço horizontal entre os cards
            ),
        ],
        spacing=20,  # Espaço vertical entre as linhas
    )

    return ft.SafeArea(
        ft.Container(
            content=ft.Column(
                [
                    # Seção do Cabeçalho
                    ft.Image(src="splash_android.png", width=180, height=180),
                    ft.Text(
                        "Controle de Estoque", size=32, weight="bold", color="#ffffff"
                    ),
                    # Espaçador entre o título e o bloco de botões
                    ft.Container(height=30),
                    # O layout dos botões que acabamos de criar
                    button_layout,
                ],
                # Centraliza todos os elementos da coluna (cabeçalho e botões)
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,  # Garante que a coluna ocupe todo o espaço vertical
            ),
            # Centraliza o conteúdo do container na página
            alignment=ft.alignment.center,
            padding=20,
            expand=True,
        )
    )
