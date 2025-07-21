import flet as ft
from views.home import home_view
from views.new_item import new_item_view
from views.remove_item import remove_item_view
from views.consult_item import consult_item_view
from views.sold_item import sold_item_view
from views.sucess import success_view
from controllers.controller import (
    inicializar_banco,
    adicionar_produto_controller,
    listar_produtos_controller,
    listar_produtos_vendidos_controller,
    remover_produto_controller,
    marcar_como_vendido_controller,
)


def main(page: ft.Page):
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

    def go_to_remove_item(e=None):
        page.controls.clear()

        # Desempacota a view e a função, exatamente como no seu exemplo
        view_content, update_function = remove_item_view(
            on_voltar=go_to_menu,
            on_remover=remover_produto_controller,
            on_listar=lambda termo=None: listar_produtos_controller(filtro=termo),
        )

        page.controls.append(view_content)
        page.update()

        # Chama a função de atualização após a página ser renderizada
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
            on_marcar_vendido=marcar_como_vendido_controller,
            on_listar=lambda termo=None: listar_produtos_controller(filtro=termo),
        )
        page.controls.append(consult_view_content)
        page.update()
        update_consult_func()

    def go_to_menu(e=None):
        page.controls.clear()
        page.controls.append(
            home_view(
                on_add_item=go_to_new_item,
                on_remove_item=go_to_remove_item,
                on_consult_item=go_to_consult_item,
                on_sold_items=go_to_sold_items,  # Certifique-se de passar a função aqui
            )
        )
        page.update()

    # Inicializa na tela de menu
    go_to_menu()


ft.app(target=main, assets_dir="assets")
