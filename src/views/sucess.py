import flet as ft


def success_view(on_add_another=None, on_voltar_menu=None):
    return ft.Container(
        ft.Column(
            [
                ft.Icon(name=ft.Icons.CHECK_CIRCLE, color="#228B22", size=80),
                ft.Text(
                    "Item adicionado com sucesso!",
                    size=24,
                    weight="bold",
                    color="#228B22",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.ElevatedButton(
                    "Adicionar outro item",
                    bgcolor="#6495ED",
                    color="#ffffff",
                    width=250,
                    height=50,
                    style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)),
                    on_click=on_add_another,
                ),
                ft.ElevatedButton(
                    "Voltar para menu",
                    bgcolor="#808080",
                    color="#ffffff",
                    width=250,
                    height=50,
                    style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)),
                    on_click=on_voltar_menu,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
        ),
        alignment=ft.alignment.center,
        expand=True,
        bgcolor="#feffff",
        padding=40,
    )
