import flet as ft


def confirm_sale_view(item_data, quantidade, preco, on_confirm, on_cancel):
    total = quantidade * preco
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Confirmar Venda",
                    size=24,
                    weight="bold",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    f"Produto: {item_data.get('tipo', '')} - {item_data.get('cor', '')}",
                    size=18,
                ),
                ft.Text(f"Código: {item_data.get('id', '')}", size=18),
                ft.Text(f"Quantidade: {quantidade}", size=18),
                ft.Text(f"Preço unitário: R$ {preco:.2f}", size=18),
                ft.Text(f"Total: R$ {total:.2f}", weight="bold", size=20),
                ft.Row(
                    [
                        ft.OutlinedButton("Cancelar", on_click=on_cancel),
                        ft.ElevatedButton(
                            "Confirmar venda",
                            bgcolor=ft.Colors.GREEN_700,
                            color="white",
                            on_click=on_confirm,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        padding=30,
        border_radius=12,
        shadow=ft.BoxShadow(blur_radius=20, color="#00000040"),
        alignment=ft.alignment.center,
        expand=True,
    )
