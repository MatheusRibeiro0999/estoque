from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle,
    Paragraph, Spacer, Image
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from datetime import datetime
import os


def gerar_pdf_pedido(pedido_id, cliente_nome, itens):
    nome_arquivo = f"pedido_{pedido_id}.pdf"

    doc = SimpleDocTemplate(
        nome_arquivo,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()
    
    style_esquerda = ParagraphStyle(
        'Esquerda',
        parent=styles['Normal'],
        alignment=0  # 0=esquerda, 1=centralizado, 2=direita, 4=justificado
    )
    
    style_titulo_esquerda = ParagraphStyle(
        'TituloEsquerda',
        parent=styles['Title'],
        alignment=0  # 0=esquerda, 1=centralizado, 2=direita, 4=justificado
    )
    
    elementos = []

    if os.path.exists("assets/logo.png"):
        logo = Image("assets/logo.png", width=4*cm, height=2*cm)
        logo_table = Table([[logo]], colWidths=[doc.width])
        logo_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ]))
        elementos.append(logo_table)

    elementos.append(Spacer(1, 10))

    titulo = Paragraph(f"<b>PEDIDO #{pedido_id}</b>", style_titulo_esquerda)
    elementos.append(titulo)

    elementos.append(Spacer(1, 10))

    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    dados_cliente = [
        [Paragraph(f"<b>Cliente:</b> {cliente_nome}", style_esquerda)],
        [Paragraph(f"<b>Data:</b> {data}", style_esquerda)]
    ]
    
    tabela_cliente = Table(dados_cliente, colWidths=[doc.width])
    tabela_cliente.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elementos.append(tabela_cliente)

    elementos.append(Spacer(1, 20))

    dados = [["Produto", "Quantidade"]]

    for item in itens:
        dados.append([
            item["nome"],
            str(item["quantidade"])
        ])

    tabela = Table(dados, colWidths=[10*cm, 4*cm])
    
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, 0), "LEFT"),  # Cabeçalho 
        ("ALIGN", (0, 1), (-1, -1), "LEFT"),  # Dados       
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
    ]))

    elementos.append(tabela)

    elementos.append(Spacer(1, 30))
    
    rodape = Paragraph("__________________________________", style_esquerda)
    elementos.append(rodape)
    
    assinatura = Paragraph("Assinatura", style_esquerda)
    elementos.append(assinatura)

    doc.build(elementos)

    print(f"PDF gerado: {nome_arquivo}")