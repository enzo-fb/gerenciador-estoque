import flet as ft


def confirm_view(
    on_confirm,
    on_cancel,
    title: str = "Confirmar Ação",
    message: str = "Você tem certeza que deseja prosseguir?",
    confirm_text: str = "Confirmar",
    cancel_text: str = "Cancelar",
):

    icon = ft.Icon(
        name=ft.Icons.WARNING_AMBER_ROUNDED, size=60, color=ft.Colors.AMBER_600
    )

    # Título da tela
    title_text = ft.Text(title, size=24, weight="bold", text_align=ft.TextAlign.CENTER)

    # Mensagem detalhada
    message_text = ft.Text(message, size=16, text_align=ft.TextAlign.CENTER)

    # Botões de ação
    confirm_button = ft.ElevatedButton(
        text=confirm_text,
        on_click=on_confirm,  # Associa a função de callback recebida
        bgcolor=ft.Colors.RED_700,
        color="white",
    )

    cancel_button = ft.OutlinedButton(
        text=cancel_text, on_click=on_cancel  # Associa a função de callback recebida
    )

    # Layout principal da caixa de diálogo
    dialog_content = ft.Column(
        [
            icon,
            ft.Container(height=10),  # Espaçador
            title_text,
            message_text,
            ft.Container(height=20),  # Espaçador
            ft.Row(
                [cancel_button, confirm_button],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Container para dar a aparência de um "card" ou "modal"
    card_container = ft.Container(
        content=dialog_content,
        width=450,
        padding=30,
        border_radius=12,
        shadow=ft.BoxShadow(blur_radius=20, color="#00000040"),
    )

    # Container raiz que preenche a tela e centraliza o card.
    # O fundo semi-transparente dá o efeito de "modal".
    root_container = ft.Container(
        content=card_container,
        expand=True,
        alignment=ft.alignment.center,
        bgcolor="#00000030",  # Fundo preto com 30% de opacidade
        # Adiciona um efeito de clique para fechar (opcional)
        on_click=on_cancel,
    )

    return root_container
