import flet as ft
from views.home import home_view
from views.new_item import new_item_view
from views.remove_item import remove_item_view
from views.consult_item import consult_item_view
from views.sold_item import sold_item_view
from views.sucess import success_view
from views.confirm import confirm_view
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

    def go_to_sale_details(e: ft.ControlEvent):
        item_selecionado = e.control.data

        def handle_sale_confirmation(quantidade_vendida, preco_venda):
            estoque_atual = int(item_selecionado.get("quantidade", 0))
            novo_estoque = estoque_atual - quantidade_vendida

            item_vendido_data = item_selecionado.copy()
            item_vendido_data["quantidade"] = quantidade_vendida
            item_vendido_data["preco_venda"] = preco_venda
            adicionar_item_vendido_controller(item_vendido_data)

            if novo_estoque > 0:
                atualizar_estoque_controller(item_selecionado["id"], novo_estoque)
            else:
                remover_produto_controller(item_selecionado["id"])

            go_to_select_for_sale()

        def handle_sale_cancel(e_cancel=None):
            go_to_select_for_sale()

        page = e.control.page  # Pega a referência da página
        page.controls.clear()
        sale_page = sale_details_view(
            item_data=item_selecionado,
            on_confirm=handle_sale_confirmation,
            on_cancel=handle_sale_cancel,
        )
        page.controls.append(sale_page)
        page.update()

    def go_to_select_for_sale(e=None):
        page = e.page if e else page  # Pega a referência da página
        page.controls.clear()

        def build_sell_button(item_data):
            return ft.IconButton(
                icon=ft.icons.MONETIZATION_ON_OUTLINED,
                icon_color=ft.colors.GREEN_700,
                tooltip="Vender este item",
                data=item_data,
                on_click=go_to_sale_details,
            )

        # Reutilizando a consult_item_view para listar os itens
        view_content = consult_item_view(
            page=page,
            on_voltar=go_to_menu,
            on_listar=listar_produtos_controller,
            item_action_builder=build_sell_button,
        )
        page.controls.append(view_content)
        page.update()

        def go_to_update_form(e: ft.ControlEvent):
            item_selecionado = e.control.data
            page = e.control.page

            print(
                f"Navegando para o formulário de atualização do item: {item_selecionado.get('id')}"
            )
            # AQUI VAI A LÓGICA PARA ABRIR A TELA DE ATUALIZAÇÃO
            # Por enquanto, vamos apenas voltar ao menu como placeholder.
            page.controls.clear()
            # No futuro, aqui chamaremos a update_item_view, passando o item_selecionado
            page.controls.append(
                ft.Text(
                    f"TELA DE ATUALIZAÇÃO PARA O ITEM {item_selecionado.get('id')}",
                    size=30,
                )
            )
            page.controls.append(ft.ElevatedButton("Voltar", on_click=go_to_menu))
            page.update()

    def go_to_update_item(e=None):
        page = e.page if e else page
        page.controls.clear()

        def build_edit_button(item_data):
            return ft.IconButton(
                icon=ft.Icons.EDIT_NOTE_ROUNDED,
                icon_color=ft.Colors.ORANGE_700,
                tooltip="Editar este item",
                data=item_data,
                on_click=go_to_update_form,
            )

        view_content = consult_item_view(
            page=page,
            on_voltar=go_to_menu,
            on_listar=listar_produtos_controller,
            item_action_builder=build_edit_button,
        )
        page.controls.append(view_content)
        page.update()

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
