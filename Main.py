import flet as ft

from auth.register import register_view
from auth.login import login_view
from auth.appointments import appointments_view
from auth.presencas import presencas_view
from services.firebase_service import db


def main(page: ft.Page):

    # CONFIGURAÇÃO GERAL
    page.title = "Prontuário Odontológico"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # ESTADO GLOBAL (SESSÃO)
    usuario_logado = {"uid": None}

    # LOGOUT
    def logout():
        usuario_logado["uid"] = None
        page.controls.clear()
        mostrar_inicio()
        page.update()

    # TELA PADRÃO (em construção)
    def ir_para_tela(nome_sessao):
        page.controls.clear()
        page.add(
            ft.Column([
                ft.ElevatedButton(
                    "← Voltar ao Menu Principal",
                    on_click=lambda _: mostrar_menu_principal()
                ),
                ft.Container(height=20),
                ft.Text(nome_sessao, size=30, weight=ft.FontWeight.BOLD),
            ], scroll=ft.ScrollMode.AUTO)
        )
        page.update()

    # CONSULTAS
    def abrir_tela_consultas():
        page.controls.clear()
        page.add(appointments_view(page, mostrar_menu_principal))
        page.update()

    # PRESENÇAS E FALTAS
    def abrir_tela_presencas():
        page.controls.clear()
        page.add(presencas_view(page, mostrar_menu_principal))
        page.update()

    # LOGIN
    def abrir_login():
        page.controls.clear()
        page.add(login_view(page, mostrar_menu_principal, mostrar_inicio, usuario_logado))
        page.update()

    # CADASTRO
    def abrir_cadastro():
        page.controls.clear()
        page.add(register_view(page, mostrar_menu_principal))
        page.update()

    # PERFIL
    def abrir_perfil():
        page.controls.clear()
        uid = usuario_logado["uid"]
        doc = db.collection("usuarios").document(uid).get()
        if not doc.exists:
            page.add(ft.Text("Usuário não encontrado"))
            page.update()
            return
        dados = doc.to_dict()
        page.add(
            ft.Column([
                ft.ElevatedButton(
                    "← Voltar ao Menu Principal",
                    on_click=lambda _: mostrar_menu_principal()
                ),
                ft.Container(height=20),
                ft.Text("Perfil do Usuário", size=30, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                ft.Text(f"Nome: {dados.get('nome', '')}"),
                ft.Text(f"Data de nascimento: {dados.get('nascimento', '')}"),
                ft.Text(f"E-mail: {dados.get('email', '')}"),
                ft.Text(f"Celular: {dados.get('celular', '')}"),
            ])
        )
        page.update()

    # MENU PRINCIPAL
    def mostrar_menu_principal():
        if usuario_logado["uid"] is None:
            mostrar_inicio()
            return

        page.controls.clear()

        titulo = ft.Text(
            "Menu Principal - Sistema Odonto",
            size=28,
            weight=ft.FontWeight.BOLD
        )

        # Mapeamento: nome do botão → função
        sessoes = {
            "Perfil":                          lambda _: abrir_perfil(),
            "Marcar e gerenciar consultas":    lambda _: abrir_tela_consultas(),
            "Registrar faltas e presenças":    lambda _: abrir_tela_presencas(),
            "Histórico de consultas":          lambda e: ir_para_tela("Histórico de consultas"),
            "Registrar procedimentos realizados": lambda e: ir_para_tela("Registrar procedimentos realizados"),
            "Informar esterilização de materiais": lambda e: ir_para_tela("Informar esterilização de materiais"),
            "Editar informações do paciente":  lambda e: ir_para_tela("Editar informações do paciente"),
        }

        lista_botoes = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

        for nome, acao in sessoes.items():
            lista_botoes.controls.append(
                ft.ElevatedButton(nome, width=600, height=50, on_click=acao)
            )

        botao_logout = ft.ElevatedButton(
            "Logout", width=600, height=50,
            on_click=lambda e: logout()
        )

        page.add(
            ft.Column([
                titulo,
                ft.Container(height=10),
                lista_botoes,
                ft.Container(height=20),
                botao_logout,
            ], expand=True)
        )
        page.update()

    # TELA INICIAL
    def mostrar_inicio():
        page.controls.clear()
        page.add(
            ft.Column([
                ft.Text("Sistema Odontológico", size=30, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                ft.ElevatedButton("Login",    width=300, on_click=lambda e: abrir_login()),
                ft.ElevatedButton("Cadastro", width=300, on_click=lambda e: abrir_cadastro()),
            ])
        )
        page.update()

    # INÍCIO DO APP
    mostrar_inicio()


ft.app(target=main)