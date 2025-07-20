import flet as ft


def home_view():
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
    )
    btn2 = ft.ElevatedButton(
        "Remover item",
        bgcolor="#6495ED",
        color="#ffffff",
        width=btn_width,
        height=50,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=btn_text_size)),
    )
    btn3 = ft.ElevatedButton(
        "Consultar item",
        bgcolor="#6495ED",
        color="#ffffff",
        width=btn_width,
        height=50,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=btn_text_size)),
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
                    btn1,
                    btn3,
                    btn2,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            bgcolor="#feffff",
            expand=True,
        ),
        expand=True,
    )
