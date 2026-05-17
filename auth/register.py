import flet as ft

def register_view(page: ft.Page, abrir_menu):

    titulo = ft.Text(
        "Cadastro de Usuário",
        size=30,
        weight=ft.FontWeight.BOLD
    )

    nome = ft.TextField(label="Nome")
    email = ft.TextField(label="Email")
    senha = ft.TextField(label="Senha", password=True)

    mensagem = ft.Text("")

    def cadastrar(e):

        if not nome.value or not email.value or not senha.value:
            mensagem.value = "Preencha todos os campos!"
            mensagem.color = "red"
            page.update()
            return

        mensagem.value = "Cadastro realizado!"
        mensagem.color = "green"

        page.update()

        # entra no sistema
        abrir_menu()

    return ft.Column([
        titulo,
        nome,
        email,
        senha,

        ft.ElevatedButton(
            "Cadastrar",
            on_click=cadastrar
        ),

        mensagem
    ])