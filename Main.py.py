import flet as ft

def main(page: ft.Page):
    page.title = "Prontuário Odontológico"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Menu Lateral (Sidebar)
    sidebar = ft.Column([
       
        ft.ElevatedButton("Informações da Paciente"),
        ft.ElevatedButton("Histórico Odontológico"),
        ft.ElevatedButton("Consultas Agendadas"),
    ], width=250)

    # Conteúdo Central (Cards)
    cards = ft.Row([
        ft.Container(content=ft.Text("Tratamentos Atuais"), bgcolor="white", padding=20, border_radius=10, expand=True),
        ft.Container(content=ft.Text("Condições Dentárias"), bgcolor="white", padding=20, border_radius=10, expand=True),
    ])

    # Layout Principal
    page.add(
        ft.Row([
            sidebar,
            ft.VerticalDivider(width=1),
            ft.Column([cards], expand=True)
        ], expand=True)
    )

ft.app(target=main)