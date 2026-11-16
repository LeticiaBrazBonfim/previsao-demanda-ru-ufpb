"""Gera o PDF da Entrega 04 a partir do relatório Markdown revisável."""

from __future__ import annotations

from html import escape
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import LongTable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, TableStyle


RAIZ = Path(__file__).resolve().parents[1]
ENTRADA = RAIZ / "docs" / "relatorio_qualidade_e04.md"
SAIDA = RAIZ / "output" / "pdf" / "E04_equipe02_dados_baseline.pdf"
SAIDA.parent.mkdir(parents=True, exist_ok=True)

FONTE_REGULAR = Path("C:/Windows/Fonts/arial.ttf")
FONTE_NEGRITO = Path("C:/Windows/Fonts/arialbd.ttf")
if FONTE_REGULAR.is_file() and FONTE_NEGRITO.is_file():
    pdfmetrics.registerFont(TTFont("E04Arial", str(FONTE_REGULAR)))
    pdfmetrics.registerFont(TTFont("E04Arial-Bold", str(FONTE_NEGRITO)))
    pdfmetrics.registerFontFamily("E04Arial", normal="E04Arial", bold="E04Arial-Bold")
    REGULAR, NEGRITO = "E04Arial", "E04Arial-Bold"
else:
    REGULAR, NEGRITO = "Helvetica", "Helvetica-Bold"

AZUL = colors.HexColor("#16324F")
AZUL_CLARO = colors.HexColor("#EAF1F7")
CINZA = colors.HexColor("#496071")
LARGURA = landscape(A4)[0] - 76

ESTILOS = {
    "titulo": ParagraphStyle("titulo", fontName=NEGRITO, fontSize=17, leading=21, textColor=AZUL, spaceAfter=14),
    "secao": ParagraphStyle("secao", fontName=NEGRITO, fontSize=12, leading=15, textColor=AZUL, spaceBefore=13, spaceAfter=7),
    "subsecao": ParagraphStyle("subsecao", fontName=NEGRITO, fontSize=10, leading=13, textColor=AZUL, spaceBefore=9, spaceAfter=5),
    "corpo": ParagraphStyle("corpo", fontName=REGULAR, fontSize=8.7, leading=11.8, textColor=colors.black, spaceAfter=5, alignment=TA_LEFT),
    "lista": ParagraphStyle("lista", fontName=REGULAR, fontSize=8.7, leading=11.8, leftIndent=12, firstLineIndent=-9, spaceAfter=4),
    "celula": ParagraphStyle("celula", fontName=REGULAR, fontSize=7.7, leading=10, textColor=colors.black),
    "cabecalho": ParagraphStyle("cabecalho", fontName=NEGRITO, fontSize=8, leading=10.5, textColor=colors.white),
}


def inline(texto: str) -> str:
    texto = escape(texto)
    texto = re.sub(r"\[([^]]+)\]\((https?://[^)]+)\)", r'<link href="\2" color="#1B5E93">\1</link>', texto)
    texto = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", texto)
    texto = re.sub(r"`([^`]+)`", r'<font color="#214B6B">\1</font>', texto)
    return texto


def largura_colunas(n: int) -> list[float]:
    pesos = {3: [0.30, 0.31, 0.39], 4: [0.15, 0.28, 0.28, 0.29], 5: [0.32, 0.17, 0.17, 0.17, 0.17]}.get(n)
    pesos = pesos or [1 / n] * n
    return [LARGURA * peso for peso in pesos]


def tabela(linhas: list[str]) -> LongTable:
    dados = []
    for linha in linhas:
        celulas = [parte.strip() for parte in linha.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", parte) for parte in celulas):
            continue
        estilo = ESTILOS["cabecalho"] if not dados else ESTILOS["celula"]
        dados.append([Paragraph(inline(parte), estilo) for parte in celulas])
    n = len(dados[0])
    if any(len(linha) != n for linha in dados):
        raise ValueError("Tabela Markdown com número irregular de colunas")
    item = LongTable(dados, colWidths=largura_colunas(n), repeatRows=1, hAlign="LEFT")
    comandos = [
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, AZUL),
        ("LINEBELOW", (0, 1), (-1, -1), 0.25, colors.HexColor("#CED9E1")),
    ]
    for indice in range(2, len(dados), 2):
        comandos.append(("BACKGROUND", (0, indice), (-1, indice), AZUL_CLARO))
    item.setStyle(TableStyle(comandos))
    return item


def construir_elementos(texto: str) -> list:
    elementos = []
    paragrafo = []
    linhas = texto.splitlines()
    i = 0

    def descarregar():
        if paragrafo:
            elementos.append(Paragraph(inline(" ".join(paragrafo)), ESTILOS["corpo"]))
            paragrafo.clear()

    while i < len(linhas):
        linha = linhas[i].strip()
        if not linha:
            descarregar()
        elif linha.startswith("|"):
            descarregar()
            bloco = []
            while i < len(linhas) and linhas[i].strip().startswith("|"):
                bloco.append(linhas[i].strip())
                i += 1
            elementos.append(tabela(bloco))
            elementos.append(Spacer(1, 9))
            continue
        elif linha.startswith("# "):
            descarregar()
            elementos.append(Paragraph(inline(linha[2:]), ESTILOS["titulo"]))
        elif linha.startswith("## "):
            descarregar()
            if linha.startswith("## 5. Diagnóstico individual"):
                elementos.append(PageBreak())
            elementos.append(Paragraph(inline(linha[3:]), ESTILOS["secao"]))
        elif linha.startswith("### "):
            descarregar()
            elementos.append(Paragraph(inline(linha[4:]), ESTILOS["subsecao"]))
        elif linha.startswith("- "):
            descarregar()
            elementos.append(Paragraph("&#8226; " + inline(linha[2:]), ESTILOS["lista"]))
        else:
            paragrafo.append(linha)
        i += 1
    descarregar()
    return elementos


def rodape(canvas, documento):
    canvas.saveState()
    canvas.setFont(REGULAR, 8)
    canvas.setFillColor(CINZA)
    canvas.drawString(38, 23, "Equipe 02 | Entrega 04 | piloto inteiramente sintético")
    canvas.drawRightString(landscape(A4)[0] - 38, 23, f"Página {documento.page}")
    canvas.restoreState()


documento = SimpleDocTemplate(
    str(SAIDA), pagesize=landscape(A4), leftMargin=38, rightMargin=38,
    topMargin=42, bottomMargin=43, title="E04 — Dados, qualidade e baseline",
    author="Equipe 02 — RU/UFPB", subject="Relatório de qualidade e baseline do mock sintético",
)
documento.build(construir_elementos(ENTRADA.read_text(encoding="utf-8")), onFirstPage=rodape, onLaterPages=rodape)
print(SAIDA)
