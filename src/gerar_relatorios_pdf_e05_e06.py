"""Gera os PDFs coletivos das Entregas 05 e 06 a partir de Markdown."""

from html import escape
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    LongTable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    TableStyle,
)


RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "output" / "pdf"
SAIDA.mkdir(parents=True, exist_ok=True)

ARIAL = Path("C:/Windows/Fonts/arial.ttf")
ARIAL_NEGRITO = Path("C:/Windows/Fonts/arialbd.ttf")
if ARIAL.is_file() and ARIAL_NEGRITO.is_file():
    pdfmetrics.registerFont(TTFont("EquipeArial", str(ARIAL)))
    pdfmetrics.registerFont(TTFont("EquipeArial-Bold", str(ARIAL_NEGRITO)))
    REGULAR = "EquipeArial"
    NEGRITO = "EquipeArial-Bold"
else:
    REGULAR = "Helvetica"
    NEGRITO = "Helvetica-Bold"

AZUL = colors.HexColor("#173B57")
AZUL_CLARO = colors.HexColor("#EAF2F7")
CINZA = colors.HexColor("#506577")
LARGURA = landscape(A4)[0] - 64

ESTILOS = {
    "titulo": ParagraphStyle(
        "titulo",
        fontName=NEGRITO,
        fontSize=16,
        leading=19,
        textColor=AZUL,
        spaceAfter=10,
    ),
    "secao": ParagraphStyle(
        "secao",
        fontName=NEGRITO,
        fontSize=10.8,
        leading=13,
        textColor=AZUL,
        spaceBefore=8,
        spaceAfter=4,
    ),
    "corpo": ParagraphStyle(
        "corpo", fontName=REGULAR, fontSize=7.9, leading=10.2, spaceAfter=4
    ),
    "lista": ParagraphStyle(
        "lista",
        fontName=REGULAR,
        fontSize=7.9,
        leading=10.2,
        leftIndent=10,
        firstLineIndent=-8,
        spaceAfter=3,
    ),
    "celula": ParagraphStyle("celula", fontName=REGULAR, fontSize=6.9, leading=8.5),
    "cabecalho": ParagraphStyle(
        "cabecalho", fontName=NEGRITO, fontSize=7, leading=8.5, textColor=colors.white
    ),
}


def inline(texto: str) -> str:
    """Converte a pequena parte de Markdown usada nos relatórios."""
    texto = escape(texto)
    texto = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", texto)
    texto = re.sub(r"`([^`]+)`", r'<font color="#214B6B">\1</font>', texto)
    return texto


def tabela(linhas: list[str]) -> LongTable:
    """Converte uma tabela Markdown em tabela paginável."""
    dados = []
    for linha in linhas:
        celulas = [parte.strip() for parte in linha.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", parte) for parte in celulas):
            continue
        estilo = ESTILOS["cabecalho"] if not dados else ESTILOS["celula"]
        dados.append([Paragraph(inline(parte), estilo) for parte in celulas])

    quantidade = len(dados[0])
    if any(len(linha) != quantidade for linha in dados):
        raise ValueError("Tabela Markdown com número irregular de colunas.")
    larguras = [LARGURA / quantidade] * quantidade
    item = LongTable(dados, colWidths=larguras, repeatRows=1, hAlign="LEFT")
    comandos = [
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LINEBELOW", (0, 1), (-1, -1), 0.2, colors.HexColor("#CED9E1")),
    ]
    for indice in range(2, len(dados), 2):
        comandos.append(("BACKGROUND", (0, indice), (-1, indice), AZUL_CLARO))
    item.setStyle(TableStyle(comandos))
    return item


def elementos(texto: str) -> list:
    """Monta os elementos visuais a partir do Markdown."""
    itens = []
    paragrafo = []
    linhas = texto.splitlines()
    indice = 0

    def descarregar() -> None:
        if paragrafo:
            itens.append(Paragraph(inline(" ".join(paragrafo)), ESTILOS["corpo"]))
            paragrafo.clear()

    while indice < len(linhas):
        linha = linhas[indice].strip()
        if not linha:
            descarregar()
        elif linha.startswith("|"):
            descarregar()
            bloco = []
            while indice < len(linhas) and linhas[indice].strip().startswith("|"):
                bloco.append(linhas[indice].strip())
                indice += 1
            itens.extend([tabela(bloco), Spacer(1, 6)])
            continue
        elif linha.startswith("# "):
            descarregar()
            itens.append(Paragraph(inline(linha[2:]), ESTILOS["titulo"]))
        elif linha.startswith("## "):
            descarregar()
            itens.append(Paragraph(inline(linha[3:]), ESTILOS["secao"]))
        elif linha.startswith("- "):
            descarregar()
            itens.append(Paragraph("&#8226; " + inline(linha[2:]), ESTILOS["lista"]))
        else:
            paragrafo.append(linha)
        indice += 1
    descarregar()
    return itens


def gerar(entrada: Path, nome: str, rotulo: str) -> None:
    """Gera um relatório com rodapé e paginação."""
    destino = SAIDA / nome

    def rodape(canvas, documento) -> None:
        canvas.saveState()
        canvas.setFont(REGULAR, 7.2)
        canvas.setFillColor(CINZA)
        canvas.drawString(32, 20, f"Equipe 02 | {rotulo} | dados sintéticos")
        canvas.drawRightString(landscape(A4)[0] - 32, 20, f"Página {documento.page}")
        canvas.restoreState()

    documento = SimpleDocTemplate(
        str(destino),
        pagesize=landscape(A4),
        leftMargin=32,
        rightMargin=32,
        topMargin=32,
        bottomMargin=34,
        title=rotulo,
        author="Equipe 02 — RU/UFPB",
    )
    documento.build(
        elementos(entrada.read_text(encoding="utf-8")),
        onFirstPage=rodape,
        onLaterPages=rodape,
    )
    print(destino)


if __name__ == "__main__":
    gerar(
        RAIZ / "docs/relatorio_e05.md",
        "E05_equipe02_pacote_a1.pdf",
        "Entrega 05 — Pacote A1",
    )
    gerar(
        RAIZ / "docs/relatorio_e06.md",
        "E06_equipe02_relatorio_preliminar.pdf",
        "Entrega 06 — Relatório preliminar",
    )
