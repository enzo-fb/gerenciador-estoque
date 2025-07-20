import flet as ft


def new_item_view(on_voltar=None, on_salvar=None):
    id_field = ft.TextField(label="Código do produto (8 dígitos)", width=300)
    quantidade_field = ft.TextField(
        label="Quantidade", width=300, keyboard_type=ft.KeyboardType.NUMBER
    )
    cor_field = ft.TextField(
        label="Cor",
        width=300,
    )
    tamanho_field = ft.TextField(
        label="Tamanho",
        width=300,
    )
    preco_field = ft.TextField(
        label="Preço", width=300, keyboard_type=ft.KeyboardType.NUMBER
    )
    descricao_field = ft.TextField(
        label="Descrição", width=300, multiline=True, min_lines=2, max_lines=4
    )
    file_picker = ft.FilePicker()
    foto_path = ft.Text("", size=14, color="#666666")

    def on_foto_result(e: ft.FilePickerResultEvent):
        if e.files:
            foto_path.value = e.files[0].name
            foto_path.update()

    file_picker.on_result = on_foto_result

    adicionar_foto_btn = ft.ElevatedButton(
        "Adicionar Foto",
        bgcolor="#808080",
        color="#ffffff",
        width=300,
        height=50,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)),
        on_click=lambda e: file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png"],
        ),
    )
    salvar_btn = ft.ElevatedButton(
        "Salvar",
        bgcolor="#228B22",
        color="#ffffff",
        width=300,
        height=50,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)),
        on_click=lambda e: on_salvar
        and on_salvar(
            {
                "id": id_field.value,
                "quantidade": quantidade_field.value,
                "cor": cor_field.value,
                "tamanho": tamanho_field.value,
                "preco": preco_field.value,
                "descricao": descricao_field.value,
                "foto": foto_path.value if foto_path.value else None,
            }
        ),
    )
    voltar_btn = ft.ElevatedButton(
        "Voltar para menu",
        bgcolor="#6495ED",
        color="#ffffff",
        width=300,
        height=50,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=20)),
        on_click=on_voltar,
    )
    layout = ft.SafeArea(
        ft.Container(
            ft.Column(
                [
                    ft.Text(
                        "Adicionar Novo Item", size=28, weight="bold", color="#000000"
                    ),
                    id_field,
                    quantidade_field,
                    cor_field,
                    tamanho_field,
                    preco_field,
                    descricao_field,
                    adicionar_foto_btn,
                    foto_path,
                    salvar_btn,
                    voltar_btn,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            alignment=ft.alignment.center,
            bgcolor="#feffff",
            expand=True,
            padding=20,
        ),
        expand=True,
    )
    return ft.Stack([layout, file_picker])
