import flet as ft
from views.home import home_view
from views.new_item import new_item_view
from views.remove_item import remove_item_view
from views.consult_item import consult_item_view
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
            )
        )
        page.update()

    def go_to_remove_item(e=None):
        page.controls.clear()
        page.controls.append(
            remove_item_view(
                on_voltar=go_to_menu,
                on_remover=remover_produto_controller,
                on_listar=lambda termo=None: listar_produtos_controller(),  # Use o controller para buscar do banco
            )
        )
        page.update()

    def go_to_consult_item(e=None):
        page.controls.clear()
        page.controls.append(
            consult_item_view(
                on_voltar=go_to_menu,
                on_marcar_vendido=marcar_como_vendido_controller,
                on_listar=listar_produtos_controller,
                on_listar_vendidos=listar_produtos_vendidos_controller,
            )
        )
        page.update()

    def go_to_menu(e=None):
        page.controls.clear()
        page.controls.append(
            home_view(
                on_add_item=go_to_new_item,
                on_remove_item=go_to_remove_item,
                on_consult_item=go_to_consult_item,
            )
        )
        page.update()

    # Inicializa na tela de menu
    go_to_menu()


ft.app(target=main)
