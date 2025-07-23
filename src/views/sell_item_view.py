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
            e.page.update()  # Garante atualização da tela após confirmar venda
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
        spacing=15,  # Espaçamento geral entre os cards
        alignment=ft.MainAxisAlignment.CENTER,  # Centraliza o conteúdo
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza horizontalmente
        controls=[
            # --- CARD 1: Informações do Produto ---
            ft.Card(
                elevation=4,
                content=ft.Container(
                    padding=20,
                    border_radius=ft.border_radius.all(10),
                    content=ft.Column(
                        spacing=10,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                f"{item_data.get('tipo', '')}",
                                size=16,
                                color=ft.Colors.WHITE70,
                                weight="w400",
                            ),
                            ft.Text(
                                f"ID: {item_data.get('id', '')}",
                                size=22,
                                color=ft.Colors.WHITE,
                                weight="bold",
                            ),
                            ft.Divider(height=5, color=ft.Colors.WHITE24),
                            ft.Text(
                                f"Disponível: {quantidade_disponivel} unidade(s)",
                                size=14,
                                color=ft.Colors.WHITE,
                            ),
                            ft.Text(
                                f"Descrição: {item_data.get('descricao', 'N/A')}",
                                size=14,
                                italic=True,
                                color=ft.Colors.WHITE70,  # Cor mais suave para detalhes
                            ),
                        ],
                    ),
                ),
            ),
            # --- CARD 2: Ação de Venda ---
            ft.Card(
                elevation=4,
                content=ft.Container(
                    padding=20,
                    border_radius=ft.border_radius.all(10),
                    content=ft.Column(
                        spacing=15,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            # Usando a propriedade 'label' dos campos, fica mais limpo
                            quantidade_row,  # Assumindo que já tem um label
                            preco_field,  # Assumindo que já tem um label
                        ],
                    ),
                ),
            ),
            # --- Botões de Ação ---
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    # Botão secundário (Cancelar) com estilo diferente
                    ft.OutlinedButton(
                        text="Cancelar",
                        icon=ft.Icons.CANCEL_OUTLINED,
                        on_click=on_cancel,
                        width=150,
                        height=50,
                    ),
                    # Botão principal (Confirmar) com mais destaque
                    ft.ElevatedButton(
                        text="Confirmar Venda",
                        icon=ft.Icons.SHOPPING_CART_CHECKOUT,
                        on_click=confirmar_venda,
                        bgcolor=ft.Colors.GREEN_700,
                        color=ft.Colors.WHITE,
                        width=180,  # Um pouco maior para dar mais importância
                        height=50,
                    ),
                ],
            ),
        ],
        expand=True,  # Garante que a coluna ocupe todo o espaço disponível
        width=350,
    )

    # Centraliza toda a tela verticalmente e horizontalmente
    return ft.Container(
        content=content_block,
        alignment=ft.alignment.center,  # Centraliza o container na tela
        expand=True,
    )
