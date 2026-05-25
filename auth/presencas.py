import flet as ft
from datetime import date, datetime
from services.firebase_service import db

# ── Cores ────────────────────────────────────────────────────────────────────
PRESENTE_FUNDO  = "#1B5E20"
PRESENTE_BORDA  = "#66BB6A"
FALTA_FUNDO     = "#7F0000"
FALTA_BORDA     = "#EF5350"
PENDENTE_FUNDO  = "#1A237E"
PENDENTE_BORDA  = "#90CAF9"
CARD_FUNDO      = "#1E1E1E"
CARD_BORDA      = "#3A3A3A"
DIM_TEXTO       = "#999999"

MESES = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
         "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]

STATUS_LABEL = {
    "presente": "✅  Presente",
    "falta":    "❌  Falta",
    "pendente": "⏳  Pendente",
}

def _borda(cor):
    s = ft.BorderSide(1, cor)
    return ft.Border(top=s, bottom=s, left=s, right=s)

def _pad(h=0, v=0):
    return ft.Padding(left=h, right=h, top=v, bottom=v)


def presencas_view(page: ft.Page, voltar_menu):

    hoje       = date.today()
    filtro_mes = [hoje.year, hoje.month]

    MESES_NOMES = MESES
    mes_label   = ft.Text("", size=20, weight=ft.FontWeight.BOLD)
    lista_cards = ft.Column([], spacing=10, scroll=ft.ScrollMode.AUTO)
    resumo_text = ft.Text("", size=13, color=DIM_TEXTO)

    # ── Carregar consultas do mês ─────────────────────────────────────────

    def carregar():
        lista_cards.controls.clear()
        ano, mes = filtro_mes[0], filtro_mes[1]
        mes_label.value = f"{MESES_NOMES[mes - 1]}  {ano}"

        try:
            docs = sorted(
                db.collection("consultas")
                  .where("ano", "==", ano)
                  .where("mes", "==", mes)
                  .stream(),
                key=lambda x: (x.to_dict().get("dia", 0),
                               x.to_dict().get("hora", ""))
            )
            docs = list(docs)

            if not docs:
                lista_cards.controls.append(
                    ft.Text("Nenhuma consulta encontrada neste mês.",
                            color=DIM_TEXTO, italic=True)
                )
                resumo_text.value = ""
            else:
                total = len(docs)
                presentes = sum(1 for d in docs if d.to_dict().get("status") == "presente")
                faltas    = sum(1 for d in docs if d.to_dict().get("status") == "falta")
                pendentes = total - presentes - faltas
                resumo_text.value = (
                    f"Total: {total}  |  ✅ {presentes} presente(s)  "
                    f"|  ❌ {faltas} falta(s)  |  ⏳ {pendentes} pendente(s)"
                )

                dia_atual = [None]
                for doc in docs:
                    d       = doc.to_dict()
                    dia     = d.get("dia", 0)
                    hora    = d.get("hora", "--:--")
                    nome    = d.get("nome", "Paciente")
                    fone    = d.get("telefone", "")
                    status  = d.get("status", "pendente")
                    doc_id  = doc.id

                    # Separador de dia
                    if dia != dia_atual[0]:
                        dia_atual[0] = dia
                        eh_hoje = (dia == hoje.day and mes == hoje.month and ano == hoje.year)
                        lista_cards.controls.append(
                            ft.Container(
                                content=ft.Text(
                                    f"{'📌 Hoje — ' if eh_hoje else ''}"
                                    f"{dia:02d}/{mes:02d}/{ano}",
                                    size=13,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLUE_200 if eh_hoje else DIM_TEXTO,
                                ),
                                padding=_pad(v=4),
                            )
                        )

                    lista_cards.controls.append(
                        _card_consulta(doc_id, nome, hora, fone, status, dia)
                    )

        except Exception as ex:
            lista_cards.controls.append(
                ft.Text(f"Erro ao carregar: {ex}", color=ft.Colors.RED_300)
            )

        page.update()

    # ── Card de cada consulta ─────────────────────────────────────────────

    def _card_consulta(doc_id, nome, hora, fone, status, dia):

        if status == "presente":
            cor_fundo, cor_borda = PRESENTE_FUNDO, PRESENTE_BORDA
        elif status == "falta":
            cor_fundo, cor_borda = FALTA_FUNDO, FALTA_BORDA
        else:
            cor_fundo, cor_borda = PENDENTE_FUNDO, PENDENTE_BORDA

        def marcar(novo_status):
            try:
                db.collection("consultas").document(doc_id).update({
                    "status": novo_status,
                    "atualizado_em": datetime.now().isoformat(),
                })
                carregar()
            except Exception as ex:
                print(f"Erro ao atualizar status: {ex}")

        btn_presente = ft.ElevatedButton(
            "✅ Presente",
            bgcolor=PRESENTE_FUNDO if status != "presente" else "#2E7D32",
            color="#FFFFFF",
            on_click=lambda e: marcar("presente"),
            style=ft.ButtonStyle(
                side=ft.BorderSide(2, PRESENTE_BORDA) if status == "presente" else ft.BorderSide(1, "#444444"),
            ),
        )
        btn_falta = ft.ElevatedButton(
            "❌ Falta",
            bgcolor=FALTA_FUNDO if status != "falta" else "#C62828",
            color="#FFFFFF",
            on_click=lambda e: marcar("falta"),
            style=ft.ButtonStyle(
                side=ft.BorderSide(2, FALTA_BORDA) if status == "falta" else ft.BorderSide(1, "#444444"),
            ),
        )
        btn_pendente = ft.ElevatedButton(
            "⏳ Pendente",
            bgcolor=PENDENTE_FUNDO if status != "pendente" else "#283593",
            color="#FFFFFF",
            on_click=lambda e: marcar("pendente"),
            style=ft.ButtonStyle(
                side=ft.BorderSide(2, PENDENTE_BORDA) if status == "pendente" else ft.BorderSide(1, "#444444"),
            ),
        )

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text(f"👤 {nome}",
                                size=15, weight=ft.FontWeight.BOLD),
                        ft.Text(f"🕐 {hora}   📞 {fone or '—'}",
                                size=12, color=DIM_TEXTO),
                    ], spacing=3, expand=True),
                    ft.Container(
                        content=ft.Text(
                            STATUS_LABEL.get(status, "⏳  Pendente"),
                            size=11, weight=ft.FontWeight.BOLD,
                            color=cor_borda,
                        ),
                        bgcolor=cor_fundo,
                        border=_borda(cor_borda),
                        border_radius=6,
                        padding=_pad(h=8, v=4),
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                ft.Row([btn_presente, btn_falta, btn_pendente],
                       spacing=8, wrap=True),
            ], spacing=8),
            bgcolor=CARD_FUNDO,
            border=_borda(cor_borda),
            border_radius=10,
            padding=_pad(h=14, v=10),
        )

    # ── Navegação de meses ────────────────────────────────────────────────

    def mes_ant(e):
        if filtro_mes[1] == 1:
            filtro_mes[1] = 12; filtro_mes[0] -= 1
        else:
            filtro_mes[1] -= 1
        carregar()

    def mes_prox(e):
        if filtro_mes[1] == 12:
            filtro_mes[1] = 1; filtro_mes[0] += 1
        else:
            filtro_mes[1] += 1
        carregar()

    # ── Layout principal ──────────────────────────────────────────────────

    conteudo = ft.Column([
        ft.ElevatedButton(
            "← Voltar ao Menu Principal",
            on_click=lambda _: voltar_menu(),
            icon=ft.Icons.ARROW_BACK,
        ),
        ft.Container(height=8),
        ft.Text("📋 Registrar Presenças e Faltas",
                size=26, weight=ft.FontWeight.BOLD),
        ft.Container(height=4),
        ft.Text("Clique em ✅ Presente ou ❌ Falta para registrar a presença de cada consulta.",
                size=12, italic=True, color=DIM_TEXTO),
        ft.Container(height=8),

        # Navegação de mês
        ft.Row([
            ft.IconButton(ft.Icons.CHEVRON_LEFT,
                          on_click=mes_ant, tooltip="Mês anterior", icon_size=26),
            mes_label,
            ft.IconButton(ft.Icons.CHEVRON_RIGHT,
                          on_click=mes_prox, tooltip="Próximo mês", icon_size=26),
        ], alignment=ft.MainAxisAlignment.CENTER),

        resumo_text,
        ft.Container(height=6),
        lista_cards,
    ],
    scroll=ft.ScrollMode.AUTO,
    expand=True)

    carregar()
    return conteudo