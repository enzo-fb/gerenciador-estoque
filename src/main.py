import flet as ft
from views.home import home_view
from views.new_item import new_item_view
from views.remove_item import remove_item_view
from views.consult_item import consult_item_view
from views.sold_item import sold_item_view
from views.sucess import success_view
from views.confirm import confirm_view
from views.sell_item_view import sale_details_view  # Adicione este import
from views.select_for_sale_view import select_for_sale_view
from views.update_item_view import update_item_view
from views.update_select_view import update_select_view
from views.update_sucess import success_view as update_success_view
from models.data import (
    marcar_como_vendido_controller,
    atualizar_item_controller,
)  # Comentei/removi se não estiver em uso para src_base64
from controllers.controller import (
    inicializar_banco,
    adicionar_produto_controller,
    listar_produtos_controller,
    listar_produtos_vendidos_controller,
    remover_produto_controller,
)
from views.confirm_sale import confirm_sale_view


def main(page: ft.Page):
    page.theme_mode = "system"  # Adapta ao modo do sistema

    # Tema claro
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#6495ED",  # Azul principal
            background="#f5f5f5",  # Fundo geral claro
            surface="#ffffff",  # Cards/branco
            on_primary="#222222",  # Texto sobre botões
            on_background="#222222",  # Texto sobre fundo
            on_surface="#222222",  # Texto sobre cards
        )
    )
    # Tema escuro
    page.dark_theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#6495ED",  # Azul principal
            background="#222222",  # Fundo geral escuro
            surface="#333333",  # Cards/cinza escuro
            on_primary="#ffffff",  # Texto sobre botões
            on_background="#ffffff",  # Texto sobre fundo
            on_surface="#ffffff",  # Texto sobre cards
        )
    )

    inicializar_banco()  # Inicializa/cria o banco ao iniciar o app

    def go_to_new_item(e=None):
        page.controls.clear()
        page.controls.append(
            new_item_view(
                on_voltar=go_to_menu,
                on_salvar=adicionar_produto_controller,
                on_sucesso=show_success_screen,
            )
        )
        page.update()

    def show_success_screen():
        def voltar_para_add(e=None):
            go_to_new_item()

        def voltar_menu(e=None):
            go_to_menu()

        page.controls.clear()
        page.controls.append(
            success_view(
                on_add_another=voltar_para_add,
                on_voltar_menu=voltar_menu,
            )
        )
        page.update()

    def go_to_confirm_remove(e: ft.ControlEvent):

        item_id_to_remove = e.control.data

        def handle_confirm(e_confirm):
            """Função executada ao clicar em 'Confirmar'."""
            remover_produto_controller(item_id_to_remove)
            go_to_remove_item()

        def handle_cancel(e_cancel):
            """Função executada ao clicar em 'Cancelar'."""
            go_to_remove_item()

        page.controls.clear()

        confirmation_page = confirm_view(
            on_confirm=handle_confirm,
            on_cancel=handle_cancel,
            title="Confirmar Exclusão",
            message=f"Tem certeza que deseja remover o item de código '{item_id_to_remove}' do estoque?",
            confirm_text="Sim, Remover",
            cancel_text="Cancelar",
        )

        page.controls.append(confirmation_page)
        page.update()

    def go_to_remove_item(e=None):
        page.controls.clear()

        view_content, update_function = remove_item_view(
            on_voltar=go_to_menu,
            on_request_remove=go_to_confirm_remove,
            on_listar=listar_produtos_controller,
        )

        page.controls.append(view_content)
        page.update()
        update_function()

    def go_to_sold_items(e=None):
        page.controls.clear()
        view_content, update_function = sold_item_view(
            on_voltar=go_to_menu,
            on_listar_vendidos=listar_produtos_vendidos_controller,
        )
        page.controls.append(view_content)
        page.update()
        update_function()

    def go_to_consult_item(e=None):
        page.controls.clear()
        consult_view_content, update_consult_func = consult_item_view(
            on_voltar=go_to_menu,
            on_listar=lambda termo=None: listar_produtos_controller(filtro=termo),
        )
        page.controls.append(consult_view_content)
        page.update()
        update_consult_func()

    def go_to_sale_details(item_selecionado):
        def handle_sale_cancel(e_cancel=None):
            go_to_select_for_sale()

        def handle_sale_confirm(quantidade_vendida, preco_venda):
            def confirmar_venda_final(e=None):
                marcar_como_vendido_controller(
                    item_selecionado, quantidade_vendida, preco_venda
                )
                go_to_select_for_sale()

            def cancelar_venda_final(e=None):
                go_to_select_for_sale()

            page.controls.clear()
            page.controls.append(
                confirm_sale_view(
                    item_data=item_selecionado,
                    quantidade=quantidade_vendida,
                    preco=preco_venda,
                    on_confirm=confirmar_venda_final,
                    on_cancel=cancelar_venda_final,
                )
            )
            page.update()

        page.controls.clear()
        sale_page = sale_details_view(
            item_data=item_selecionado,
            on_confirm=handle_sale_confirm,  # Agora chama a tela de confirmação
            on_cancel=handle_sale_cancel,
        )
        page.controls.append(sale_page)
        page.update()

    def go_to_select_for_sale(e=None):
        # Use sempre a variável 'page' do escopo principal
        page.controls.clear()

        def on_vender(item):
            go_to_sale_details(item)

        view_content = select_for_sale_view(
            on_voltar=go_to_menu,
            on_listar=listar_produtos_controller,
            on_vender=on_vender,
        )
        page.controls.append(view_content)
        page.update()

    def go_to_update_form(item_selecionado):
        def salvar_atualizacao(novo_item):
            atualizar_item_controller(novo_item)
            show_update_success_screen()

        def show_update_success_screen():
            def atualizar_mais(e=None):
                go_to_update_item()

            def voltar_menu(e=None):
                go_to_menu()

            page.controls.clear()
            page.controls.append(
                update_success_view(
                    on_add_another=atualizar_mais,
                    on_voltar_menu=voltar_menu,
                )
            )
            page.update()

        page.controls.clear()
        page.controls.append(
            update_item_view(
                item_data=item_selecionado,
                on_salvar=salvar_atualizacao,
                on_voltar=go_to_update_item,
            )
        )
        page.update()

    def go_to_update_item(e=None):
        page.controls.clear()

        def on_editar(item):
            go_to_update_form(item)

        # 1. Primeiro, busca todos os produtos
        produtos = listar_produtos_controller()

        # 2. Constrói a view passando a lista de produtos já carregada
        view_content = update_select_view(
            on_voltar=go_to_menu,
            produtos=produtos,  # Passa a lista de produtos
            on_editar=on_editar,
        )

        # 3. Adiciona a view à página e atualiza UMA ÚNICA VEZ
        page.controls.append(view_content)
        page.update()

        # A função de atualização agora não existe mais e o problema de timing é eliminado

    def go_to_menu(e=None):
        page.controls.clear()
        page.controls.append(
            home_view(
                on_add_item=go_to_new_item,
                on_remove_item=go_to_remove_item,
                on_consult_item=go_to_consult_item,
                on_sold_items=go_to_sold_items,  # Certifique-se de passar a função aqui
                on_sell_item=go_to_select_for_sale,  # <-- CONECTAR FUNÇÃO
                on_update_item=go_to_update_item,  # <-- CONECTAR FUNÇÃO
            )
        )
        page.update()

    # Inicializa na tela de menu
    go_to_menu()


ft.app(target=main, assets_dir="assets")
