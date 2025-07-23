import flet as ft
import base64


def select_for_sale_view(on_voltar, on_listar, on_vender):

    # Armazena todos os produtos em uma variável para podermos filtrar
    todos_os_produtos = on_listar()
    item_column = ft.Column(
        [],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    # --- FUNÇÃO QUE CRIA O CARD DE ITEM COM BOTÃO DE VENDER ---
    # --- FUNÇÃO QUE CRIA O CARD DE ITEM COM BOTÃO DE VENDER ABAIXO ---
    def item_card(item):
        foto = item.get("foto")
        foto_ctrl = None

        # Lógica para exibir a imagem (igual à sua)
        if isinstance(foto, bytes) and foto:
            foto_base64 = base64.b64encode(foto).decode("utf-8")
            foto_ctrl = ft.Image(
                src_base64=foto_base64, width=100, height=100, fit=ft.ImageFit.COVER
            )
        else:
            foto_ctrl = ft.Image(
                src=foto or "https://via.placeholder.com/100",
                width=100,
                height=100,
                fit=ft.ImageFit.COVER,
            )

        # 1. A estrutura principal agora é uma Coluna.
        #    Ela centraliza o botão horizontalmente.

        card_content = ft.Column(
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                # 2. A primeira parte é uma Linha apenas com a imagem e os textos.
                ft.Row(
                    [
                        ft.Container(
                            foto_ctrl,
                            width=110,
                            height=110,
                            bgcolor="#f0f0f0",
                            border_radius=8,
                            alignment=ft.alignment.center,
                            margin=ft.margin.only(right=16),
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    f"Código: {item.get('id', '')}",
                                    weight="bold",
                                    size=16,
                                    color="#000000",
                                ),
                                ft.Text(
                                    f"Tipo: {item.get('tipo', '')}",
                                    size=15,
                                    color="#000000",
                                ),
                                ft.Text(
                                    f"Cor: {item.get('cor', '')}",
                                    size=15,
                                    color="#000000",
                                ),
                                ft.Text(
                                    f"Tamanho: {item.get('tamanho', '')}",
                                    size=15,
                                    color="#000000",
                                ),
                                ft.Text(
                                    f"Qtd em Estoque: {item.get('quantidade', '')}",
                                    size=15,
                                    weight="bold",
                                    color="#000000",
                                ),
                                ft.Text(
                                    f"Preço: R$ {float(item.get('preco', 0) or 0):.2f}",
                                    size=14,
                                    color="#000000",
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=5,
                            expand=True,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                # Adiciona uma linha divisória para separar visualmente
                ft.Divider(height=10, color=ft.Colors.GREY_300),
                # 3. A segunda parte é o botão de Venda.
                #    Sugiro trocar o IconButton por um botão com texto, fica mais claro.
                ft.FilledButton(
                    text="Vender Item",
                    icon=ft.Icons.MONETIZATION_ON_OUTLINED,
                    on_click=lambda e, item=item: on_vender(item),
                    width=250,  # Largura do botão
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        bgcolor=ft.Colors.GREEN_700,
                        color=ft.Colors.WHITE,
                    ),
                ),
            ],
        )

        return ft.Container(
            content=card_content,  # Adiciona a nova coluna ao container do card
            padding=20,
            margin=ft.margin.symmetric(vertical=8),
            bgcolor=ft.Colors.WHITE,  # Um branco puro para mais contraste
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=6, color="#cccccc", offset=ft.Offset(2, 2)),
            width=500,
            # O on_click agora pode ser removido do container principal se a única ação for vender.
            # on_click=lambda e: print(f"Você clicou no item de ID: {item.get('id')}"),
        )

    # Lógica de atualização e filtragem, similar à sua
    def update_items():
        termo = search_field.value.lower() if search_field.value else ""

        filtered = [
            item
            for item in todos_os_produtos
            if termo in item.get("id", "").lower()
            or termo in item.get("tipo", "").lower()
            or termo in item.get("cor", "").lower()
            or termo in item.get("tamanho", "").lower()
        ]

        item_column.controls.clear()
        if not filtered:
            item_column.controls.append(
                ft.Text("Nenhum item encontrado.", color=ft.Colors.RED, size=18)
            )
        else:
            for item in filtered:
                item_column.controls.append(item_card(item))
        # item_column.update()  # Remover esta linha!

    # Campos de busca
    search_field = ft.TextField(
        label="Buscar por código, cor, tipo...",
        width=400,
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: update_items(),
    )

    # Preenche a lista inicialmente
    update_items()

    # Centraliza o conteúdo na tela
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Selecione um item para vender",
                    size=24,
                    weight="bold",
                    text_align=ft.TextAlign.CENTER,
                ),
                search_field,
                ft.Divider(),
                item_column,
                ft.ElevatedButton(
                    "Voltar",
                    on_click=on_voltar,
                    width=300,
                    height=50,
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.BLUE_GREY,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            expand=True,
        ),
        alignment=ft.alignment.center,
        expand=True,
        padding=ft.padding.only(
            top=80, left=30, right=30, bottom=30
        ),  # Espaço extra no topo
    )
