import flet as ft
from services.firebase_service import db


def login_view(page: ft.Page, mostrar_menu_principal, voltar_para_login):

    email = ft.TextField(label="Email")
    senha = ft.TextField(label="Senha", password=True)

    def fazer_login(e):

        usuarios = db.collection("usuarios").stream()

        for u in usuarios:
            dados = u.to_dict()

            if dados["email"] == email.value and dados["senha"] == senha.value:

                page.controls.clear()
                mostrar_menu_principal()
                page.update()
                return

        page.snack_bar = ft.SnackBar(ft.Text("Login inválido"))
        page.snack_bar.open = True
        page.update()

    return ft.Column([
        ft.Text("Login", size=30),
        email,
        senha,

        ft.ElevatedButton("Entrar", on_click=fazer_login),

        ft.TextButton(
            "Voltar",
            on_click=lambda e: voltar_para_login()
        )
    ])