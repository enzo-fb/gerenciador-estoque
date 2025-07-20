import flet as ft
from src.views.home import home_view


def main(page: ft.Page):
    page.add(home_view())


ft.app(main)
