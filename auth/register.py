import flet as ft
from services.firebase_service import criar_usuario


def register_view(page: ft.Page, mostrar_menu_principal):

    nome = ft.TextField(label="Nome completo")
    nascimento = ft.TextField(label="Data de nascimento (DD/MM/AAAA)")
    email = ft.TextField(label="Email")
    celular = ft.TextField(label="Número de celular")
    senha = ft.TextField(label="Senha", password=True)


    

    def cadastrar(e):

        uid = criar_usuario(
            nome.value,
            nascimento.value,
            email.value,
            celular.value,
            senha.value
        )

        page.snack_bar = ft.SnackBar(
            ft.Text(f"Usuário criado: {uid}")
        )
        page.snack_bar.open = True
        page.update()

        # Limpa a tela atual para preparar a próxima
        page.controls.clear()

        # Vai para o menu principal
        mostrar_menu_principal()

    return ft.Column([
        ft.Text("Cadastro de Usuário"),
        nome,
        nascimento,
        email,
        celular,
        senha,
        ft.ElevatedButton("Cadastrar", on_click=cadastrar)
    ])