import flet as ft
from services.firebase_service import db


def profile_view(page: ft.Page, user_uid, voltar):

    doc = db.collection("usuarios").document(user_uid).get()

    if doc.exists:
        data = doc.to_dict()
    else:
        data = {}

    return ft.Column([

        ft.ElevatedButton("← Voltar", on_click=lambda e: voltar()),

        ft.Text("Perfil do Usuário", size=30),

        ft.Text(f"Nome: {data.get('nome', '')}"),
        ft.Text(f"Nascimento: {data.get('nascimento', '')}"),
        ft.Text(f"Email: {data.get('email', '')}"),
        ft.Text(f"Celular: {data.get('celular', '')}"),

    ])