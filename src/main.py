import flet as ft
from views.home import home_view
from views.new_item import new_item_view
import time


def main(page: ft.Page):

    def go_to_new_item(e):
        page.controls.clear()
        page.controls.append(new_item_view())
        page.update()

    page.controls.clear()
    page.controls.append(home_view(on_add_item=go_to_new_item))
    page.update()


# while True:  # Exibe apenas a tela de novo item e atualiza sempre
#     page.controls.clear()
#     page.controls.append(new_item_view())
#     page.update()
#     time.sleep(10)


ft.app(target=main)
