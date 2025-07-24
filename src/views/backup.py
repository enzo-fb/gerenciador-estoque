import flet as ft
import os
import gzip
import shutil
from models.data import ULTIMO_BACKUP_PERSONALIZADO


def backup_view(on_voltar, on_backup, page):
    status_text = ft.Text("", size=16, color="#228B22")
    file_picker = ft.FilePicker()
    file_picker_result = [None]

    restore_picker = ft.FilePicker()
    restore_file_path = [None]

    # Adiciona PermissionHandler ao overlay da página
    permission_handler = ft.PermissionHandler()
    if permission_handler not in page.overlay:
        page.overlay.append(permission_handler)
    if file_picker not in page.overlay:
        page.overlay.append(file_picker)
    if restore_picker not in page.overlay:
        page.overlay.append(restore_picker)

    def check_permission(e):
        # Use STORAGE para multiplataforma, MANAGE_EXTERNAL_STORAGE só para Android 11+
        result = permission_handler.check_permission(ft.PermissionType.STORAGE)
        status_text.value = f"Permissão STORAGE: {result}"
        status_text.color = "#228B22" if result else "#FF0000"
        status_text.update()

    def request_permission(e):
        # Use STORAGE para multiplataforma, MANAGE_EXTERNAL_STORAGE só para Android 11+
        result = permission_handler.request_permission(ft.PermissionType.STORAGE)
        status_text.value = f"Solicitação de permissão STORAGE: {result}"
        status_text.color = "#228B22" if result else "#FF0000"
        status_text.update()

    def selecionar_destino(e):
        # Solicita permissão antes de abrir o FilePicker
        permission_handler.request_permission(ft.PermissionType.STORAGE)
        file_picker.save_file(
            allowed_extensions=["gz"],
            dialog_title="Escolha onde salvar o backup",
            file_name="estoque_backup.db.gz",
        )

    def on_picker_result(e: ft.FilePickerResultEvent):
        if e.path:
            file_picker_result[0] = e.path
            status_text.value = f"Destino selecionado: {e.path}"
            status_text.color = "#228B22"
            status_text.update()
        else:
            status_text.value = "Nenhum destino selecionado."
            status_text.color = "#FF0000"
            status_text.update()

    file_picker.on_result = on_picker_result

    def executar_backup(e):
        destino = file_picker_result[0]
        if destino:
            try:
                if not os.access(os.path.dirname(destino), os.W_OK):
                    status_text.value = "Sem permissão para salvar neste local. Escolha uma pasta como 'Downloads'."
                    status_text.color = "#FF0000"
                    status_text.update()
                    return
                ok = on_backup(destino)
                if ok:
                    status_text.value = "Backup realizado com sucesso!"
                    status_text.color = "#228B22"
                else:
                    status_text.value = "Falha ao realizar backup."
                    status_text.color = "#FF0000"
            except Exception as ex:
                status_text.value = f"Erro ao salvar backup: {ex}"
                status_text.color = "#FF0000"
            status_text.update()
        else:
            status_text.value = "Selecione um destino antes de salvar."
            status_text.color = "#FF0000"
            status_text.update()

    def selecionar_backup_para_restaurar(e):
        restore_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["gz"],
            dialog_title="Selecione o arquivo de backup para restaurar",
        )

    def on_restore_picker_result(e: ft.FilePickerResultEvent):
        if e.files and e.files[0].path:
            restore_file_path[0] = e.files[0].path
            status_text.value = f"Backup selecionado para restaurar: {e.files[0].name}"
            status_text.color = "#228B22"
            status_text.update()
        else:
            restore_file_path[0] = None
            status_text.value = "Nenhum arquivo de backup selecionado."
            status_text.color = "#FF0000"
            status_text.update()

    restore_picker.on_result = on_restore_picker_result

    def executar_restauracao(e):
        caminho_backup = restore_file_path[0]
        if not caminho_backup or not os.path.exists(caminho_backup):
            status_text.value = "Selecione um arquivo de backup válido."
            status_text.color = "#FF0000"
            status_text.update()
            return

        db_path_real = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../models/estoque.db")
        )

        try:
            with (
                gzip.open(caminho_backup, "rb") as f_in,
                open(db_path_real, "wb") as f_out,
            ):
                shutil.copyfileobj(f_in, f_out)
            status_text.value = "Backup restaurado com sucesso!"
            status_text.color = "#228B22"
            status_text.update()
        except Exception as ex:
            status_text.value = f"Erro ao restaurar backup: {ex}"
            status_text.color = "#FF0000"
            status_text.update()

    destino_atual_label = ft.Text(
        "Destino atual do backup:",
        size=15,
        color="#444444",
        text_align=ft.TextAlign.CENTER,
        weight="bold",
    )
    destino_atual_path = ft.Text(
        ULTIMO_BACKUP_PERSONALIZADO[0] or "Nenhum definido",
        size=15,
        color="#228B22" if ULTIMO_BACKUP_PERSONALIZADO[0] else "#FF0000",
        selectable=True,
        text_align=ft.TextAlign.CENTER,
        weight="bold",
    )

    instrucoes = ft.Text(
        "Escolha um local seguro para salvar o backup do banco de dados.\n"
        "Você pode restaurar um backup antigo a qualquer momento.",
        size=13,
        color="#444444",
        text_align=ft.TextAlign.CENTER,
        italic=True,
    )

    return ft.Stack(
        [
            ft.SafeArea(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Backup do Banco de Dados",
                                size=32,
                                weight="bold",
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Divider(),
                            destino_atual_label,
                            destino_atual_path,
                            instrucoes,
                            status_text,
                            ft.Container(height=10),
                            ft.Row(
                                [
                                    ft.ElevatedButton(
                                        "Escolher destino...",
                                        on_click=selecionar_destino,
                                        bgcolor="#808080",
                                        width=150,
                                        height=45,
                                        color="#ffffff",
                                    ),
                                    ft.ElevatedButton(
                                        "Salvar Backup",
                                        on_click=executar_backup,
                                        width=150,
                                        height=45,
                                        bgcolor="#228B22",
                                        color="#ffffff",
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                expand=True,
                            ),
                            ft.Row(
                                [
                                    ft.OutlinedButton(
                                        "Verificar permissão",
                                        data=ft.PermissionType.STORAGE,
                                        on_click=check_permission,
                                        width=120,
                                        height=36,
                                        style=ft.ButtonStyle(
                                            padding=ft.Padding(0, 0, 0, 0),
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                        ),
                                    ),
                                    ft.OutlinedButton(
                                        "Solicitar permissão",
                                        data=ft.PermissionType.STORAGE,
                                        on_click=request_permission,
                                        width=120,
                                        height=36,
                                        style=ft.ButtonStyle(
                                            padding=ft.Padding(0, 0, 0, 0),
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                        ),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=10,
                            ),
                            ft.Divider(),
                            ft.Text(
                                "Recuperar dados de um backup salvo",
                                size=18,
                                weight="bold",
                                text_align=ft.TextAlign.CENTER,
                                color="#3FA355",
                            ),
                            ft.Row(
                                [
                                    ft.ElevatedButton(
                                        "Selecionar arquivo...",
                                        on_click=selecionar_backup_para_restaurar,
                                        width=150,
                                        height=45,
                                        bgcolor="#808080",
                                        color="#ffffff",
                                    ),
                                    ft.ElevatedButton(
                                        "Recuperar Backup",
                                        on_click=executar_restauracao,
                                        width=150,
                                        height=45,
                                        bgcolor="#3FA355",
                                        color="#ffffff",
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                expand=True,
                            ),
                            ft.Container(height=20),
                            ft.ElevatedButton(
                                "Voltar para menu",
                                on_click=on_voltar,
                                width=300,
                                height=45,
                                bgcolor="#6495ED",
                                color="#ffffff",
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=18,
                        expand=True,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                    padding=40,
                ),
                expand=True,
            ),
            file_picker,
            restore_picker,
        ],
        expand=True,
        alignment=ft.alignment.center,
    )
        alignment=ft.alignment.center,
    )
