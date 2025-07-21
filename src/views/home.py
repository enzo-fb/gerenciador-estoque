import flet as ft


def home_view(
    on_add_item=None, on_remove_item=None, on_consult_item=None, on_sold_items=None
):
    # Troque o nome do arquivo da logo conforme sua imagem personalizada
    logo = ft.Image(src="logo1.png", width=300, height=300)
    btn_width = 300
    btn_text_size = 20
    btn1 = ft.ElevatedButton(
        "Adicionar novo item",
        bgcolor="#6495ED",
        color="#ffffff",
        width=btn_width,
        height=50,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=btn_text_size)),
        on_click=on_add_item,
    )
    btn2 = ft.ElevatedButton(
        "Remover item",
        bgcolor="#6495ED",
        color="#ffffff",
        width=btn_width,
        height=50,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=btn_text_size)),
        on_click=on_remove_item,
    )
    btn3 = ft.ElevatedButton(
        "Consultar item",
        bgcolor="#6495ED",
        color="#ffffff",
        width=btn_width,
        height=50,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=btn_text_size)),
        on_click=on_consult_item,
    )
    btn4 = ft.ElevatedButton(
        "Ver Itens Vendidos",
        bgcolor="#808080",
        color="#ffffff",
        width=btn_width,
        height=50,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=btn_text_size)),
        on_click=(on_sold_items if on_sold_items else None),
    )
    return ft.SafeArea(
        ft.Container(
            ft.Column(
                [
                    logo,
                    ft.Container(
                        ft.Text(
                            "Controle de \nEstoque",
                            size=30,
                            weight="bold",
                            color="#000000",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=10, bottom=100),
                    ),
                    btn1,  # Adicionar novo item
                    btn2,  # Remover item
                    btn3,  # Consultar item
                    btn4,  # Ver Itens Vendidos
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            alignment=ft.alignment.center,
            bgcolor="#feffff",
            expand=True,
        ),
        expand=True,
    )
