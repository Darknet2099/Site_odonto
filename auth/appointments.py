import flet as ft
# Importa o módulo de cores corretamente para evitar o erro de atributo
from flet import Colors

def appointments_view(page: ft.Page, voltar_menu):
    # Campos do formulário do paciente
    nome_input = ft.TextField(label="Nome Completo", width=400)
    endereco_input = ft.TextField(label="Endereço", width=400)
    telefone_input = ft.TextField(label="Telefone", width=400, keyboard_type=ft.KeyboardType.PHONE)
    data_nasc_input = ft.TextField(label="Data de Nascimento (DD/MM/AAAA)", width=400)
    historico_input = ft.TextField(label="Histórico Básico do Paciente", width=400, multiline=True, min_lines=3)
    
    # Campo para a data da consulta
    data_consulta_input = ft.TextField(label="Data e Hora da Consulta", width=400)

    # Área de status/agenda simulada usando a nova referência de cores
    status_text = ft.Text("", color=Colors.GREEN, weight=ft.FontWeight.BOLD)
    
    # Funções dos botões de ação
    def agendar_consulta(e):
        if not nome_input.value or not data_consulta_input.value:
            status_text.value = "Por favor, preencha pelo menos o Nome e a Data da Consulta."
            status_text.color = Colors.RED
        else:
            status_text.value = f"Consulta agendada com sucesso para {nome_input.value}!"
            status_text.color = Colors.GREEN
        page.update()

    def remarcar_consulta(e):
        if not nome_input.value or not data_consulta_input.value:
            status_text.value = "Informe o nome e a nova data para remarcar."
            status_text.color = Colors.ORANGE
        else:
            status_text.value = f"Consulta de {nome_input.value} remarcada!"
            status_text.color = Colors.ORANGE
        page.update()

    def cancelar_consulta(e):
        if not nome_input.value:
            status_text.value = "Informe o nome do paciente para cancelar."
            status_text.color = Colors.RED
        else:
            status_text.value = f"Consulta de {nome_input.value} cancelada."
            status_text.color = Colors.RED
        page.update()

    def visualizar_agenda(e):
        status_text.value = "Exibindo agenda: [Simulação] Próxima consulta: João Silva às 14:00."
        status_text.color = Colors.BLUE
        page.update()

    # Layout da página
    conteudo = ft.Column([
        ft.ElevatedButton("← Voltar ao Menu Principal", on_click=lambda _: voltar_menu()),
        ft.Container(height=10),
        
        ft.Text("Gerenciamento de Consultas e Pacientes", size=28, weight=ft.FontWeight.BOLD),
        ft.Container(height=10),
        
        # Seção de Dados do Paciente
        ft.Text("Dados do Paciente", size=18, weight=ft.FontWeight.W_600),
        nome_input,
        endereco_input,
        telefone_input,
        data_nasc_input,
        historico_input,
        
        ft.Divider(),
        
        # Seção de Agendamento
        ft.Text("Agendamento", size=18, weight=ft.FontWeight.W_600),
        data_consulta_input,
        ft.Container(height=10),
        
        # Botões de Ação com as propriedades de cores corrigidas
        ft.Row([
            ft.ElevatedButton("Marcar Consulta", on_click=agendar_consulta, bgcolor=Colors.BLUE, color=Colors.WHITE),
            ft.ElevatedButton("Remarcar", on_click=remarcar_consulta),
            ft.ElevatedButton("Cancelar Consulta", on_click=cancelar_consulta, bgcolor=Colors.RED_ACCENT, color=Colors.WHITE),
        ], wrap=True, spacing=10),
        
        ft.Container(height=5),
        ft.ElevatedButton("Visualizar Agenda", on_click=visualizar_agenda, width=200),
        
        ft.Container(height=10),
        status_text
        
    ], scroll=ft.ScrollMode.AUTO)
    
    return conteudo