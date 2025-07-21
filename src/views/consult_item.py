import flet as ft
from models.data import salvar_blob_em_arquivo


def consult_item_view(
    on_voltar=None,
    on_listar=None,
    on_marcar_vendido=None,
):
    search_field = ft.TextField(
        label="Buscar por código, cor, tamanho...",
        width=300,
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: update_items(),
    )
    min_value_field = ft.TextField(
        label="Valor mínimo",
        width=145,
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=lambda e: update_items(),
    )
    max_value_field = ft.TextField(
        label="Valor máximo",
        width=145,
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=lambda e: update_items(),
    )

    item_column = ft.Column(
        [],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    def marcar_vendido(e, codigo):
        if on_marcar_vendido:
            on_marcar_vendido(codigo)
        update_items()  # Atualiza a lista após marcar como vendido

    detalhes_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Detalhes do Produto", weight="bold"),
        content=ft.Column([], tight=True, spacing=10),
        actions=[
            ft.TextButton(
                "Fechar",
                on_click=lambda e: fechar_dialog(e),
            )
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def fechar_dialog(e):
        page = e.page
        detalhes_dialog.open = False
        page.update()

    def mostrar_detalhes(item):
        # Use item_column.page para obter a página
        page = item_column.page if hasattr(item_column, "page") else None
        foto = item.get("foto")
        foto_src = None
        if isinstance(foto, bytes):
            temp_path = salvar_blob_em_arquivo(foto)
            foto_src = (
                f"file://{temp_path}"
                if temp_path
                else "https://via.placeholder.com/200"
            )
        elif foto and not str(foto).startswith("http"):
            foto_src = f"file://{foto}"
        else:
            foto_src = foto or "https://via.placeholder.com/200"
        detalhes_dialog.title = ft.Text(
            f"Detalhes do Produto {item.get('id', '')}", weight="bold"
        )
        detalhes_dialog.content.controls = [
            ft.Image(
                src=foto_src,
                width=200,
                height=200,
                fit=ft.ImageFit.CONTAIN,
            ),
            ft.Text(f"Código: {item.get('id', '')}", weight="bold"),
            ft.Text(f"Tipo: {item.get('tipo', '')}"),
            ft.Text(f"Cor: {item.get('cor', '')}"),
            ft.Text(f"Tamanho: {item.get('tamanho', '')}"),
            ft.Text(f"Quantidade: {item.get('quantidade', '')}"),
            ft.Text(f"Preço: R$ {item.get('preco', 0):.2f}"),
            ft.Text(f"Descrição: {item.get('descricao', '')}"),
        ]
        detalhes_dialog.open = True
        if page:
            page.dialog = detalhes_dialog
            page.update()

    def item_card(item):
        foto = item.get("foto")
        foto_src = None
        if isinstance(foto, bytes):
            temp_path = salvar_blob_em_arquivo(foto)
            foto_src = (
                f"file://{temp_path}"
                if temp_path
                else "https://via.placeholder.com/100"
            )
        elif foto and not str(foto).startswith("http"):
            foto_src = f"file://{foto}"
        else:
            foto_src = foto or "https://via.placeholder.com/100"
        return ft.Container(
            content=ft.Row(
                [
                    # Foto do produto (imagem ou placeholder)
                    ft.Container(
                        ft.Image(
                            src=foto_src,
                            width=100,
                            height=100,
                            fit=ft.ImageFit.COVER,
                        ),
                        width=110,
                        height=110,
                        bgcolor="#f0f0f0",
                        border_radius=8,
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(right=16),
                    ),
                    # Informações do produto
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
                            ),  # Garante exibição do tipo
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
                                f"Qtd: {item.get('quantidade', '')}",
                                size=15,
                                color="#000000",
                            ),
                            ft.Text(
                                f"Descrição: {item.get('descricao', '')}",
                                color="#000000",
                                size=14,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.ElevatedButton(
                                "Marcar como vendido",
                                bgcolor="#228B22",
                                color="#ffffff",
                                width=180,
                                height=40,
                                style=ft.ButtonStyle(text_style=ft.TextStyle(size=16)),
                                on_click=lambda e, codigo=item.get(
                                    "id", ""
                                ): marcar_vendido(e, codigo),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=2,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=16,
            margin=ft.margin.symmetric(vertical=8),
            bgcolor="#f5f5f5",  # Alterado para cinza claro
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=8, color="#cccccc", offset=ft.Offset(2, 2)),
            width=400,
            on_click=lambda e: mostrar_detalhes(item),
        )

    def update_items():
        termo = search_field.value.lower() if search_field.value else ""
        min_val = min_value_field.value
        max_val = max_value_field.value
        try:
            min_val = float(min_val) if min_val else None
        except ValueError:
            min_val = None
        try:
            max_val = float(max_val) if max_val else None
        except ValueError:
            max_val = None

        # Busca todos os itens primeiro
        items = on_listar(termo) if on_listar else []

        # Aplica filtro de preço
        filtered = []
        for item in items:
            preco = item.get("preco", 0)
            if (min_val is None or preco >= min_val) and (
                max_val is None or preco <= max_val
            ):
                filtered.append(item)

        item_column.controls.clear()
        if not filtered:
            item_column.controls.append(
                ft.Text("Nenhum item encontrado.", color="red", size=18)
            )
        else:
            for item in filtered:
                item_column.controls.append(item_card(item))
        item_column.update()
        if item_column.page:
            item_column.page.update()

    voltar_btn = ft.ElevatedButton(
        "Voltar para menu",
        bgcolor="#6495ED",
        color="#ffffff",
        width=300,
        height=40,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=16)),
        on_click=on_voltar,
    )

    # Inicializa a lista filtrada ao abrir a tela
    def on_page_load(e):
        update_items()

    view = ft.SafeArea(
        ft.Container(
            ft.Column(
                [
                    ft.Text(
                        "Consultar Estoque", size=28, weight="bold", color="#000000"
                    ),
                    search_field,
                    ft.Row(
                        [min_value_field, max_value_field],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    item_column,
                    ft.Row(
                        [voltar_btn],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                expand=True,  # Adicionado para expandir a coluna
            ),
            alignment=ft.alignment.top_center,
            bgcolor="#feffff",
            expand=True,  # Adicionado para expandir o container
            padding=20,
        ),
        expand=True,  # Adicionado para expandir o SafeArea
    )

    # Atualiza a lista ao carregar a página
    view.on_mount = on_page_load

    # Adiciona o dialog de detalhes à página
    def on_view_mount(e):
        page = e.page
        page.dialog = detalhes_dialog
        update_items()

    view.on_mount = on_view_mount

    return view
    # Atualiza a lista ao carregar a página
    view.on_mount = on_page_load

    # Adiciona o dialog de detalhes à página
    def on_view_mount(e):
        page = e.page
        page.dialog = detalhes_dialog
        update_items()

    view.on_mount = on_view_mount

    return view
