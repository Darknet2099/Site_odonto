import flet as ft

from auth.register import register_view
from auth.login import login_view
from auth.appointments import appointments_view


def main(page: ft.Page):

    page.title = "Prontuário Odontológico"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20


    #Representa um estado global da aplicação
    usuario_logado = {"uid": None}
    page.controls.clear()
    mostrar_inicio()
    page.update()
    

    # LOGOUT
    
    def logout():
        page.controls.clear()
        mostrar_inicio()
        page.update()


    # FUNÇÃO PADRÃO DE TELAS
    
    def ir_para_tela(nome_sessao):

        page.controls.clear()

        botao_voltar = ft.ElevatedButton(
            "← Voltar ao Menu Principal",
            on_click=lambda _: mostrar_menu_principal()
        )

        conteudo_pagina = ft.Column([
            botao_voltar,
            ft.Container(height=20),

            ft.Text(
                nome_sessao,
                size=30,
                weight=ft.FontWeight.BOLD
            ),

        ], scroll=ft.ScrollMode.AUTO)

        page.add(conteudo_pagina)
        page.update()

    
    # CONSULTAS

    def abrir_tela_consultas():
        page.controls.clear()
        page.add(appointments_view(page, mostrar_menu_principal))
        page.update()


    # LOGIN
    
    def abrir_login():

        page.controls.clear()

        page.add(
            login_view(
                page,
                mostrar_menu_principal,
                mostrar_inicio
            )
        )

        page.update()

    
    # CADASTRO

    def abrir_cadastro():

        page.controls.clear()

        page.add(
            register_view(
                page,
                mostrar_menu_principal
            )
        )

        page.update()


    # MENU PRINCIPAL 

    def mostrar_menu_principal():

        page.controls.clear()

        titulo = ft.Text(
            "Menu Principal - Sistema Odonto",
            size=28,
            weight=ft.FontWeight.BOLD
        )

        sessoes = [
            "Perfil",
            "Marcar e gerenciar consultas",
            "Registrar faltas e presenças",
            "Histórico de consultas",
            "Registrar procedimentos realizados",
            "Informar esterilização de materiais",
            "Editar informações do paciente",
        ]

        lista_botoes = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.AUTO
        )

        for sessao in sessoes:

            if sessao == "Marcar e gerenciar consultas":
                acao_clique = lambda _: abrir_tela_consultas()
            else:
                acao_clique = lambda e, s=sessao: ir_para_tela(s)

            lista_botoes.controls.append(
                ft.ElevatedButton(
                    sessao,
                    width=600,
                    height=50,
                    on_click=acao_clique
                )
            )

        # 🔥 LOGOUT (PASSO 6 AQUI)
        botao_logout = ft.ElevatedButton(
            "Logout",
            width=600,
            height=50,
            on_click=lambda e: logout()
        )

        page.add(
            ft.Column([
                titulo,
                ft.Container(height=10),
                lista_botoes,
                ft.Container(height=20),
                botao_logout
            ], expand=True)
        )

        page.update()

    
    # TELA INICIAL
  
    def mostrar_inicio():

        page.controls.clear()

        page.add(
            ft.Column([

                ft.Text(
                    "Sistema Odontológico",
                    size=30,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Container(height=20),

                ft.ElevatedButton(
                    "Login",
                    width=300,
                    on_click=lambda e: abrir_login()
                ),

                ft.ElevatedButton(
                    "Cadastro",
                    width=300,
                    on_click=lambda e: abrir_cadastro()
                )

            ])
        )

        page.update()

    
    # INÍCIO DO Site

    mostrar_inicio()

ft.app(target=main)