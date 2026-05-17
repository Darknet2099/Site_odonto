import flet as ft
from auth.register import register_view
# Importa a nova tela que criamos (ajuste o caminho se salvou em alguma pasta)
from auth.appointments import appointments_view 

def main(page: ft.Page):

    page.title = "Prontuário Odontológico"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # ---------------------------
    # FUNÇÃO PARA ABRIR SESSÕES PADRÃO
    # ---------------------------

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

    # ---------------------------
    # FUNÇÃO PARA ABRIR A TELA DE CONSULTAS
    # ---------------------------
    def abrir_tela_consultas():
        page.controls.clear()
        # Adiciona a view externa passando a página e a função de voltar
        page.add(appointments_view(page, mostrar_menu_principal))
        page.update()

    # ---------------------------
    # MENU PRINCIPAL
    # ---------------------------

    def mostrar_menu_principal():

        page.controls.clear()

        titulo = ft.Text(
            "Menu Principal - Sistema Odonto",
            size=28,
            weight=ft.FontWeight.BOLD
        )

        sessoes = [
            "Perfil",
            "Marcar e gerenciar consultas", # Clicar aqui vai redirecionar para a nova tela
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
            # Condição para definir qual função o botão vai chamar ao ser clicado
            if sessao == "Marcar e gerenciar consultas":
                acao_clique = lambda _: abrir_tela_consultas()
            else:
                # Mantém o comportamento genérico para as outras sessões temporariamente
                acao_clique = lambda e, s=sessao: ir_para_tela(s)

            lista_botoes.controls.append(
                ft.ElevatedButton(
                    sessao,
                    width=600,
                    height=50,
                    on_click=acao_clique
                )
            )

        page.add(
            ft.Column([
                titulo,
                ft.Container(height=10),
                lista_botoes
            ], expand=True)
        )

        page.update()
        
    # ---------------------------
    # PRIMEIRA TELA = CADASTRO
    # ---------------------------

    page.add(
        register_view(
            page,
            mostrar_menu_principal
        )
    )

ft.app(target=main)