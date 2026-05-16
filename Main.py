import flet as ft

def main(page: ft.Page):
    page.title = "Prontuário Odontológico"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    
    def ir_para_tela(nome_sessao):
        page.controls.clear()
        
        
        botao_voltar = ft.ElevatedButton(
            "← Voltar ao Menu Principal", 
            on_click=lambda _: mostrar_menu_principal()
        )
        
        
        conteudo_pagina = ft.Column([
            botao_voltar,
            ft.Container(height=20),
            ft.Text(nome_sessao, size=30, weight=ft.FontWeight.BOLD),
            
        ], scroll=ft.ScrollMode.AUTO)
        
        page.add(conteudo_pagina)
        page.update()

    
    def mostrar_menu_principal():
        page.controls.clear()
        
        titulo = ft.Text("Menu Principal - Sistema Odonto", size=28, weight=ft.FontWeight.BOLD)
        
        sessoes = [
            "Perfil",
            "Marcar e gerenciar consultas",
            "Registrar faltas e presenças",
            "Histórico de consultas",
            "Registrar procedimentos realizados",
            "Informar esterilização de materiais",
            "Editar informações do paciente",
            
        ]
    
        
        lista_botoes = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)
        
        for sessao in sessoes:
            lista_botoes.controls.append(
                ft.ElevatedButton(
                    sessao, 
                    width=600,
                    height=50,
                    on_click=lambda e, s=sessao: ir_para_tela(s)
                )
            )
            
        # Adiciona tudo à página
        page.add(
            ft.Column([
                titulo,
                ft.Container(height=10), 
                lista_botoes
            ], expand=True)
        )
        page.update()

    # Inicia o aplicativo
    mostrar_menu_principal()

ft.app(target=main)