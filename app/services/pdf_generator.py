import os
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

def gerar_das_pdf(nome_empresa: str, cnpj: str, mes_referencia: str) -> str:
    """
    Gera um PDF simulando um DAS (Documento de Arrecadação do Simples Nacional).
    Salva em storage/boletos e retorna o caminho absoluto.
    """
    # Define diretório de saída
    base_dir = Path(__file__).resolve().parent.parent.parent
    output_dir = base_dir / "storage" / "boletos"
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"DAS_{cnpj}_{mes_referencia.replace('/', '-')}.pdf"
    file_path = output_dir / filename

    c = canvas.Canvas(str(file_path), pagesize=A4)
    width, height = A4

    # Cabeçalho
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2*cm, height - 2*cm, "DOCUMENTO DE ARRECADAÇÃO DO SIMPLES NACIONAL")
    
    c.setFont("Helvetica", 12)
    c.drawString(2*cm, height - 3*cm, "DAS - Documento de Arrecadação")

    # Dados da Empresa
    y_pos = height - 5*cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2*cm, y_pos, "CONTRIBUINTE:")
    c.setFont("Helvetica", 12)
    c.drawString(6*cm, y_pos, nome_empresa)

    y_pos -= 1*cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2*cm, y_pos, "CNPJ:")
    c.setFont("Helvetica", 12)
    c.drawString(6*cm, y_pos, cnpj)

    y_pos -= 1*cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2*cm, y_pos, "PERÍODO DE APURAÇÃO:")
    c.setFont("Helvetica", 12)
    c.drawString(8*cm, y_pos, mes_referencia)

    y_pos -= 2*cm
    c.drawString(2*cm, y_pos, "VALOR A PAGAR: R$ 150,00 (Simulado)")

    # Código de Barras (Simulação visual)
    y_pos -= 4*cm
    c.setFillColorRGB(0, 0, 0)
    c.rect(2*cm, y_pos, 17*cm, 1.5*cm, fill=1)
    
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, y_pos + 0.5*cm, "85800000001-0 50000200240-9 10202400000-0 12345678901-2")

    c.save()
    
    return str(file_path.absolute())
