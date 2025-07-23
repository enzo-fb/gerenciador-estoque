import flet as ft


def sale_details_view(item_data, on_confirm, on_cancel):
    quantidade_disponivel = int(item_data.get("quantidade", 0))

    quantidade_field = ft.TextField(
        value="1",
        width=80,
        text_align=ft.TextAlign.CENTER,
        keyboard_type=ft.KeyboardType.NUMBER,
        border_color=ft.Colors.WHITE,  # Borda branca
        color=ft.Colors.WHITE,  # Texto branco
    )

    preco_field = ft.TextField(
        label="Valor da venda",
        value=str(item_data.get("preco", "")),
        keyboard_type=ft.KeyboardType.NUMBER,
        width=200,
        text_align=ft.TextAlign.CENTER,
        border_color=ft.Colors.WHITE,  # Borda branca
        label_style=ft.TextStyle(color=ft.Colors.WHITE),
        color=ft.Colors.WHITE,  # Texto branco
    )

    def decrementar_quantidade(e):
        try:
            valor_atual = int(quantidade_field.value)
            if valor_atual > 0:
                quantidade_field.value = str(valor_atual - 1)
                e.page.update()
        except ValueError:
            quantidade_field.value = "0"
            e.page.update()

    def incrementar_quantidade(e):
        try:
            valor_atual = int(quantidade_field.value)
            if valor_atual < quantidade_disponivel:
                quantidade_field.value = str(valor_atual + 1)
                e.page.update()
        except ValueError:
            quantidade_field.value = "1"
            e.page.update()

    def confirmar_venda(e):
        try:
            quantidade_vendida = int(quantidade_field.value)
            preco_venda = float(preco_field.value)

            if quantidade_vendida <= 0 or quantidade_vendida > quantidade_disponivel:
                e.page.snack_bar = ft.SnackBar(
                    ft.Text("Quantidade inválida!"), open=True
                )
                e.page.update()
                return

            if preco_venda < 0:
                e.page.snack_bar = ft.SnackBar(
                    ft.Text("Preço não pode ser negativo!"), open=True
                )
                e.page.update()
                return

            on_confirm(quantidade_vendida, preco_venda)
        except ValueError:
            e.page.snack_bar = ft.SnackBar(
                ft.Text("Valores inválidos nos campos!"), open=True
            )
            e.page.update()

    # Layout dos botões de + e -
    quantidade_row = ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.REMOVE,
                on_click=decrementar_quantidade,
                tooltip="Diminuir quantidade",
                icon_color=ft.Colors.WHITE,
            ),
            quantidade_field,
            ft.IconButton(
                icon=ft.Icons.ADD,
                on_click=incrementar_quantidade,
                tooltip="Aumentar quantidade",
                icon_color=ft.Colors.WHITE,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Bloco principal de conteúdo, centralizado na tela
    content_block = ft.Column(
        [
            ft.Text(
                f"Vender: {item_data.get('tipo') +' - '+ item_data.get('id')}",
                size=24,
                color=ft.Colors.WHITE,
                weight="bold",
            ),
            ft.Text(
                f"Qtd. Disponível: {quantidade_disponivel}",
                size=16,
                color=ft.Colors.WHITE,
            ),
            ft.Text(
                f"Descrição: {item_data.get('descricao', 'N/A')}",
                size=14,
                color=ft.Colors.WHITE,
            ),
            ft.Divider(height=20, color=ft.Colors.WHITE24),
            ft.Text("Quantidade vendida:", size=16, color=ft.Colors.WHITE),
            quantidade_row,
            ft.Text("Preço da venda:", size=16, color=ft.Colors.WHITE),
            preco_field,
            ft.Container(height=30),  # Espaço para separar os botões
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Confirmar venda",
                        on_click=confirmar_venda,
                        bgcolor=ft.Colors.GREEN_700,
                        color=ft.Colors.WHITE,
                    ),
                    ft.ElevatedButton(
                        "Cancelar",
                        on_click=on_cancel,
                        bgcolor=ft.Colors.RED_700,
                        color=ft.Colors.WHITE,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,  # Alinha o bloco na vertical
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinha os elementos do bloco na horizontal
        spacing=30,  # Espaçamento entre os elementos do bloco
    )

    # A função retorna apenas o bloco centralizado
    return ft.Container(
        content=content_block,
        alignment=ft.alignment.center,  # Alinha o container na vertical e horizontal
        expand=True,
    )
