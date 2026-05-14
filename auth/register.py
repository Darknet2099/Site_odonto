import flet as ft

def register_view(page: ft.Page):
   
    titulo = ft.Text("Cadastro de Usuário")
    nome = ft.TextField(label="Nome Completo")
    email = ft.TextField(label="Email")
    senha = ft.TextField(label="Senha", password=True)
    
    def cadastrar(e):
        page.snack_bar = ft.SnackBar(ft.Text("Usuário cadastrado!"))
        page.snack_bar.open = True
        page.update()
    
    return ft.Column([
        titulo,
        nome,
        email,
        senha,
        ft.ElevatedButton("Cadastrar", on_click = cadastrar)   
])
    
    