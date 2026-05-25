import flet as ft
import calendar
from datetime import datetime, date
from services.firebase_service import db

# ── Cores ────────────────────────────────────────────────────────────────────
AZUL_FUNDO   = "#1A237E"
AZUL_BORDA   = "#90CAF9"
VERDE_FUNDO  = "#1B5E20"
VERDE_BORDA  = "#66BB6A"
VERDE_TEXTO  = "#C8E6C9"
LIVRE_FUNDO  = "#2A2A2A"
LIVRE_BORDA  = "#555555"
DIM_TEXTO    = "#999999"
CARD_FUNDO   = "#1E3A1E"
CARD_BORDA   = "#388E3C"

CELL  = 52   # tamanho de cada célula do calendário
GAP   = 6    # espaço entre células
DIAS_SEMANA = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]


def _borda(cor):
    s = ft.BorderSide(1, cor)
    return ft.Border(top=s, bottom=s, left=s, right=s)

def _pad(h=0, v=0):
    return ft.Padding(left=h, right=h, top=v, bottom=v)


def appointments_view(page: ft.Page, voltar_menu):

    hoje          = date.today()
    mes_atual     = [hoje.year, hoje.month]
    consultas_mes = {}

    MESES = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
             "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]

    # ── Widgets principais ───────────────────────────────────────────────────
    mes_label     = ft.Text("", size=22, weight=ft.FontWeight.BOLD)
    corpo_cal     = ft.Column([], spacing=GAP)   # aqui ficam as linhas do calendário

    # ── Widgets do dialog ────────────────────────────────────────────────────
    campo_nome = ft.TextField(label="Nome do Paciente *", width=370)
    campo_hora = ft.TextField(label="Horário (ex: 14:30) *", width=370)
    campo_fone = ft.TextField(label="Telefone", width=370, keyboard_type=ft.KeyboardType.PHONE)
    campo_obs  = ft.TextField(label="Observações", width=370, multiline=True, min_lines=2)
    st_texto   = ft.Text("", size=13)
    lista_cons = ft.Column([], spacing=6)
    dia_sel    = [None]

    # ── Firebase ─────────────────────────────────────────────────────────────

    def carregar_mes():
        consultas_mes.clear()
        ano, mes = mes_atual[0], mes_atual[1]
        try:
            for doc in (db.collection("consultas")
                        .where("ano", "==", ano)
                        .where("mes", "==", mes)
                        .stream()):
                d = doc.to_dict()
                dia = d.get("dia")
                if dia:
                    consultas_mes[dia] = consultas_mes.get(dia, 0) + 1
        except Exception as ex:
            print(f"Erro carregar_mes: {ex}")

    def carregar_dia(dia):
        lista_cons.controls.clear()
        ano, mes = mes_atual[0], mes_atual[1]
        try:
            docs = sorted(
                db.collection("consultas")
                  .where("ano", "==", ano)
                  .where("mes", "==", mes)
                  .where("dia", "==", dia)
                  .stream(),
                key=lambda x: x.to_dict().get("hora", "")
            )
            if not docs:
                lista_cons.controls.append(
                    ft.Text("Nenhuma consulta marcada para este dia.",
                            color=DIM_TEXTO, italic=True)
                )
            else:
                for doc in docs:
                    d = doc.to_dict()
                    lista_cons.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Column([
                                    ft.Text(f"🕐 {d.get('hora','--:--')}  —  👤 {d.get('nome','?')}",
                                            weight=ft.FontWeight.BOLD, size=13),
                                    ft.Text(f"📞 {d.get('telefone','—')}   📝 {d.get('observacoes','') or '—'}",
                                            size=11, color=DIM_TEXTO),
                                ], spacing=2, expand=True),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    icon_color=ft.Colors.RED_400,
                                    tooltip="Cancelar consulta",
                                    on_click=lambda e, did=doc.id: deletar(did, dia),
                                ),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            bgcolor=CARD_FUNDO,
                            border=_borda(CARD_BORDA),
                            border_radius=8,
                            padding=_pad(h=10, v=6),
                        )
                    )
        except Exception as ex:
            lista_cons.controls.append(
                ft.Text(f"Erro: {ex}", color=ft.Colors.RED_300))
        page.update()

    def salvar(e):
        if not campo_nome.value or not campo_hora.value:
            st_texto.value = "⚠️  Preencha o nome e o horário!"
            st_texto.color = ft.Colors.ORANGE_400
            page.update()
            return
        dia = dia_sel[0]
        ano, mes = mes_atual[0], mes_atual[1]
        try:
            db.collection("consultas").add({
                "nome": campo_nome.value.strip(),
                "hora": campo_hora.value.strip(),
                "telefone": campo_fone.value.strip(),
                "observacoes": campo_obs.value.strip(),
                "dia": dia, "mes": mes, "ano": ano,
                "criado_em": datetime.now().isoformat(),
            })
            campo_nome.value = campo_hora.value = campo_fone.value = campo_obs.value = ""
            st_texto.value = "✅  Consulta marcada com sucesso!"
            st_texto.color = ft.Colors.GREEN_400
            carregar_dia(dia)
            carregar_mes()
            renderizar()
        except Exception as ex:
            st_texto.value = f"Erro: {ex}"
            st_texto.color = ft.Colors.RED_400
        page.update()

    def deletar(doc_id, dia):
        try:
            db.collection("consultas").document(doc_id).delete()
            st_texto.value = "🗑️  Consulta cancelada."
            st_texto.color = ft.Colors.ORANGE_400
            carregar_dia(dia)
            carregar_mes()
            renderizar()
        except Exception as ex:
            st_texto.value = f"Erro: {ex}"
            st_texto.color = ft.Colors.RED_400
        page.update()

    # ── Dialog ───────────────────────────────────────────────────────────────
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Consultas", weight=ft.FontWeight.BOLD),
        content=ft.Container(
            width=420, height=520,
            content=ft.Column([
                ft.Text("📋 Consultas do dia:", size=14, weight=ft.FontWeight.BOLD),
                lista_cons,
                ft.Divider(height=14),
                ft.Text("➕ Nova Consulta:", size=14, weight=ft.FontWeight.BOLD),
                campo_nome, campo_hora, campo_fone, campo_obs,
                st_texto,
            ], scroll=ft.ScrollMode.AUTO, spacing=8),
        ),
        actions=[
            ft.TextButton("Fechar", on_click=lambda e: fechar()),
            ft.ElevatedButton(
                "Marcar Consulta",
                icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                on_click=salvar,
                bgcolor=ft.Colors.BLUE_700,
                color=ft.Colors.WHITE,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def abrir():
        # Flet 0.85.1 — usar page.overlay
        if dialog not in page.overlay:
            page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def fechar():
        dialog.open = False
        st_texto.value = ""
        page.update()

    # ── Construção do calendário (linhas manuais) ────────────────────────────

    def cel_vazia():
        return ft.Container(width=CELL, height=CELL)

    def cel_header(nome):
        return ft.Container(
            width=CELL, height=36,
            alignment=ft.Alignment(0, 0),
            content=ft.Text(nome, size=11, weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                            color=ft.Colors.BLUE_200),
        )

    def cel_dia(dia, tem, eh_hoje):
        if eh_hoje:
            fundo, borda, cor_n = AZUL_FUNDO, AZUL_BORDA, "#FFFFFF"
        elif tem:
            fundo, borda, cor_n = VERDE_FUNDO, VERDE_BORDA, VERDE_TEXTO
        else:
            fundo, borda, cor_n = LIVRE_FUNDO, LIVRE_BORDA, "#FFFFFF"

        return ft.Container(
            width=CELL, height=CELL,
            bgcolor=fundo,
            border=_borda(borda),
            border_radius=8,
            alignment=ft.Alignment(0, 0),
            on_click=lambda e, d=dia: abrir_dia(d),
            ink=True,
            content=ft.Column([
                ft.Text(str(dia), size=14, color=cor_n,
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.BOLD if eh_hoje else ft.FontWeight.NORMAL),
                ft.Text(f"{consultas_mes[dia]}✓" if tem else "",
                        size=9, color=VERDE_BORDA,
                        text_align=ft.TextAlign.CENTER),
            ], alignment=ft.MainAxisAlignment.CENTER,
               horizontal_alignment=ft.CrossAxisAlignment.CENTER,
               spacing=0),
        )

    def abrir_dia(dia):
        dia_sel[0] = dia
        campo_nome.value = campo_hora.value = campo_fone.value = campo_obs.value = ""
        st_texto.value = ""
        ano, mes = mes_atual[0], mes_atual[1]
        dialog.title = ft.Text(f"📅  {dia:02d}/{mes:02d}/{ano}",
                                weight=ft.FontWeight.BOLD, size=16)
        carregar_dia(dia)
        abrir()

    def renderizar():
        corpo_cal.controls.clear()
        ano, mes = mes_atual[0], mes_atual[1]
        mes_label.value = f"{MESES[mes - 1]}  {ano}"

        # Linha do cabeçalho
        corpo_cal.controls.append(
            ft.Row([cel_header(n) for n in DIAS_SEMANA],
                   spacing=GAP, alignment=ft.MainAxisAlignment.CENTER)
        )

        # Monta todas as células
        primeiro, total = calendar.monthrange(ano, mes)
        deslocamento = (primeiro + 1) % 7   # domingo = 0

        celulas = [cel_vazia() for _ in range(deslocamento)]
        for dia in range(1, total + 1):
            tem     = dia in consultas_mes
            eh_hoje = (dia == hoje.day and mes == hoje.month and ano == hoje.year)
            celulas.append(cel_dia(dia, tem, eh_hoje))

        # Preenche a última semana para fechar em 7
        while len(celulas) % 7 != 0:
            celulas.append(cel_vazia())

        # Cria uma Row por semana
        for i in range(0, len(celulas), 7):
            corpo_cal.controls.append(
                ft.Row(celulas[i:i+7],
                       spacing=GAP,
                       alignment=ft.MainAxisAlignment.CENTER)
            )

        page.update()

    def mes_ant(e):
        if mes_atual[1] == 1:
            mes_atual[1] = 12; mes_atual[0] -= 1
        else:
            mes_atual[1] -= 1
        carregar_mes(); renderizar()

    def mes_prox(e):
        if mes_atual[1] == 12:
            mes_atual[1] = 1; mes_atual[0] += 1
        else:
            mes_atual[1] += 1
        carregar_mes(); renderizar()

    # ── Layout principal ─────────────────────────────────────────────────────
    conteudo = ft.Column([
        ft.ElevatedButton("← Voltar ao Menu Principal",
                          on_click=lambda _: voltar_menu(),
                          icon=ft.Icons.ARROW_BACK),
        ft.Container(height=8),
        ft.Text("🦷 Agenda de Consultas", size=28, weight=ft.FontWeight.BOLD),
        ft.Container(height=6),

        ft.Row([
            ft.IconButton(ft.Icons.CHEVRON_LEFT,  on_click=mes_ant,
                          tooltip="Mês anterior", icon_size=28),
            mes_label,
            ft.IconButton(ft.Icons.CHEVRON_RIGHT, on_click=mes_prox,
                          tooltip="Próximo mês",  icon_size=28),
        ], alignment=ft.MainAxisAlignment.CENTER),

        ft.Container(height=4),

        ft.Row([
            ft.Container(width=14, height=14, bgcolor=AZUL_FUNDO,  border_radius=3),
            ft.Text("Hoje", size=12),
            ft.Container(width=14, height=14, bgcolor=VERDE_FUNDO, border_radius=3),
            ft.Text("Com consulta", size=12),
            ft.Container(width=14, height=14, bgcolor=LIVRE_FUNDO,
                         border=_borda(LIVRE_BORDA), border_radius=3),
            ft.Text("Livre", size=12),
        ], spacing=6, alignment=ft.MainAxisAlignment.CENTER),

        ft.Container(height=8),
        corpo_cal,
        ft.Container(height=10),
        ft.Text("Clique em qualquer dia para ver ou marcar consultas.",
                size=12, italic=True, color=DIM_TEXTO,
                text_align=ft.TextAlign.CENTER),
    ],
    scroll=ft.ScrollMode.AUTO,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    carregar_mes()
    renderizar()
    return conteudo