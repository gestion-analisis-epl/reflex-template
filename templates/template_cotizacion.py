from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
from reportlab.platypus import Image as RLImage
from datetime import datetime
import os

BLUE_DARK   = colors.HexColor('#1e3a8a')
BLUE_LIGHT  = colors.HexColor('#e0e7ff')
GRAY_BG     = colors.HexColor('#f3f4f6')
GRAY_BORDER = colors.HexColor('#d1d5db')
WHITE       = colors.white
TEXT_DARK   = colors.HexColor('#333333')
TEXT_MUTED  = colors.HexColor('#666666')

MARGIN    = 0.75 * inch
CONTENT_W = letter[0] - (MARGIN * 2)
TOTALES_W = 3.2 * inch
BAR_W     = 4  # ancho de la barra de color izquierda


def _styles():
    base = getSampleStyleSheet()
    normal = ParagraphStyle('INormal', parent=base['Normal'],
                            fontSize=10, textColor=TEXT_DARK, leading=15)
    right  = ParagraphStyle('IRight',  parent=normal, alignment=TA_RIGHT)
    center = ParagraphStyle('ICenter', parent=normal, alignment=TA_CENTER)
    muted_center = ParagraphStyle('IMutedCenter', parent=normal,
                                  fontSize=9, textColor=TEXT_MUTED,
                                  alignment=TA_CENTER)
    invoice_meta_right = ParagraphStyle('IMetaRight', parent=normal,
                                        fontSize=10, alignment=TA_RIGHT,
                                        leading=17)
    total_style = ParagraphStyle('ITotal', parent=normal,
                                 fontSize=12, fontName='Helvetica-Bold',
                                 textColor=BLUE_DARK, alignment=TA_RIGHT)
    return dict(normal=normal, right=right, center=center,
                muted_center=muted_center,
                invoice_meta_right=invoice_meta_right,
                total_style=total_style)


def generar_pdf_cotizacion(cotizacion: dict, ruta_salida: str,
                            logo_path: str = None) -> bool:
    try:
        doc = SimpleDocTemplate(
            ruta_salida, pagesize=letter,
            topMargin=MARGIN, bottomMargin=MARGIN,
            leftMargin=MARGIN, rightMargin=MARGIN,
        )

        st = _styles()
        elementos = []

        # ── Fechas ──────────────────────────────────────────────────────────
        def _fmt(d):
            if not d: return "No especificada"
            if isinstance(d, str): d = datetime.fromisoformat(d.split("T")[0])
            return d.strftime("%d/%m/%Y")

        fecha_cot_str = _fmt(cotizacion.get("fecha_cotizacion", datetime.now()))
        fecha_ven_str = _fmt(cotizacion.get("fecha_vencimiento", ""))

        # ── Totales ─────────────────────────────────────────────────────────
        productos = cotizacion.get("productos", [])
        subtotal  = sum(float(p["precio_unitario"]) * int(p["cantidad"]) for p in productos)
        
        # Verificar si se incluye IVA
        incluir_iva = cotizacion.get("incluir_iva", True)
        tasa_iva  = float(cotizacion.get("impuesto", 0.16)) if incluir_iva else 0.0
        iva       = subtotal * tasa_iva if incluir_iva else 0.0
        total     = subtotal + iva

        # ════════════════════════════════════════════════════════════════════
        # HEADER
        # ════════════════════════════════════════════════════════════════════
        LOGO_W, LOGO_H = 1.6 * inch, 0.7 * inch

        if logo_path and os.path.isfile(logo_path):
            logo_cell = RLImage(logo_path, width=LOGO_W, height=LOGO_H)
        else:
            logo_cell = Paragraph(
                '<font size="26" color="#1e3a8a"><b>KRONOS</b></font>',
                st['normal']
            )

        meta_right = Paragraph(
            f'<font size="16" color="#1e3a8a"><b>Cotización</b></font><br/>'
            f'<font size="10">N° {cotizacion.get("id_kronos", "")}</font><br/>'
            f'<font size="10">Fecha: {fecha_cot_str}</font><br/>'
            f'<font size="10">Válida hasta: {fecha_ven_str}</font>',
            st['invoice_meta_right']
        )

        header_tbl = Table(
            [[logo_cell, meta_right]],
            colWidths=[CONTENT_W * 0.55, CONTENT_W * 0.45]
        )
        header_tbl.setStyle(TableStyle([
            ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
            ('LEFTPADDING',   (0, 0), (0, -1),  0),
            ('RIGHTPADDING',  (1, 0), (1, -1),  0),
        ]))
        elementos.append(header_tbl)
        elementos.append(
            HRFlowable(width="100%", thickness=3, color=BLUE_DARK, spaceAfter=14)
        )

        # ════════════════════════════════════════════════════════════════════
        # CLIENTE — barra azul como columna, no como LINEBEFORE
        # ════════════════════════════════════════════════════════════════════
        empresa  = cotizacion.get("empresa_cliente", "")
        telefono = cotizacion.get("telefono_cliente", "")
        estado   = cotizacion.get("estado_origen", "")

        client_html = (
            f'<b>Facturar a:</b><br/>'
            f'{cotizacion.get("nombre_cliente", "")}'
            + (f'<br/>{empresa}'    if empresa  else '') + '<br/>'
            f'{cotizacion.get("email_cliente", "")}'
            + (f'<br/>{telefono}' if telefono else '')
            + (f'<br/>{estado}'   if estado   else '')
        )

        client_tbl = Table(
            [['', Paragraph(client_html, st['normal'])]],
            colWidths=[BAR_W, CONTENT_W - BAR_W]
        )
        client_tbl.setStyle(TableStyle([
            ('BACKGROUND',    (0, 0), (0, -1),  BLUE_DARK),   # barra izq
            ('BACKGROUND',    (1, 0), (1, -1),  BLUE_LIGHT),  # fondo índigo
            ('LEFTPADDING',   (0, 0), (0, -1),  0),
            ('RIGHTPADDING',  (0, 0), (0, -1),  0),
            ('LEFTPADDING',   (1, 0), (1, -1),  14),
            ('RIGHTPADDING',  (1, 0), (1, -1),  14),
            ('TOPPADDING',    (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elementos.append(client_tbl)
        elementos.append(Spacer(1, 0.25 * inch))

        # ════════════════════════════════════════════════════════════════════
        # EJECUTIVO — barra gris como columna
        # ════════════════════════════════════════════════════════════════════
        if cotizacion.get("nombre_ejecutivo"):
            tel_exec = cotizacion.get("telefono_ejecutivo", "")
            exec_html = (
                f'<b>Ejecutivo de cuenta:</b><br/>'
                f'{cotizacion.get("nombre_ejecutivo", "")}<br/>'
                f'{cotizacion.get("email_ejecutivo", "")}'
                + (f'<br/>{tel_exec}' if tel_exec else '')
            )
            exec_tbl = Table(
                [['', Paragraph(exec_html, st['normal'])]],
                colWidths=[BAR_W, CONTENT_W - BAR_W]
            )
            exec_tbl.setStyle(TableStyle([
                ('BACKGROUND',    (0, 0), (0, -1),  GRAY_BORDER), # barra gris
                ('BACKGROUND',    (1, 0), (1, -1),  GRAY_BG),     # fondo gris claro
                ('LEFTPADDING',   (0, 0), (0, -1),  0),
                ('RIGHTPADDING',  (0, 0), (0, -1),  0),
                ('LEFTPADDING',   (1, 0), (1, -1),  14),
                ('RIGHTPADDING',  (1, 0), (1, -1),  14),
                ('TOPPADDING',    (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))
            elementos.append(exec_tbl)
            elementos.append(Spacer(1, 0.25 * inch))

        # ════════════════════════════════════════════════════════════════════
        # TABLA DE PRODUCTOS — bordes manuales, sin BOX
        # ════════════════════════════════════════════════════════════════════
        COL_W = [CONTENT_W * 0.46, CONTENT_W * 0.12,
                 CONTENT_W * 0.21, CONTENT_W * 0.21]

        def th(text):
            return Paragraph(f'<font color="white"><b>{text}</b></font>', st['center'])

        prod_data = [[th("PRODUCTO / SERVICIO"), th("CANT."),
                      th("PRECIO UNIT."),        th("SUBTOTAL")]]

        for p in productos:
            sub_p = float(p["precio_unitario"]) * int(p["cantidad"])
            prod_data.append([
                Paragraph(p["nombre_producto"], st['normal']),
                Paragraph(str(p["cantidad"]),   st['center']),
                Paragraph(f'${float(p["precio_unitario"]):,.2f}', st['right']),
                Paragraph(f'${sub_p:,.2f}',                       st['right']),
            ])

        prod_tbl = Table(prod_data, colWidths=COL_W, repeatRows=1)

        row_styles = [
            # Header
            ('BACKGROUND',    (0, 0), (-1, 0),  BLUE_DARK),
            ('TEXTCOLOR',     (0, 0), (-1, 0),  WHITE),
            ('TOPPADDING',    (0, 0), (-1, 0),  10),
            ('BOTTOMPADDING', (0, 0), (-1, 0),  10),
            # Cuerpo
            ('FONTNAME',      (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE',      (0, 1), (-1, -1), 10),
            ('TOPPADDING',    (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('LEFTPADDING',   (0, 0), (-1, -1), 8),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
            ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
            # Bordes manuales (sin BOX para que el header no quede "flotando")
            ('LINEABOVE',     (0, 0), (-1, 0),  1, BLUE_DARK),
            ('LINELEFT',      (0, 0), (0, -1),  1, GRAY_BORDER),
            ('LINERIGHT',     (-1, 0), (-1, -1),1, GRAY_BORDER),
            ('LINEBELOW',     (0, -1), (-1, -1),1, GRAY_BORDER),
            ('LINEBELOW',     (0, 0), (-1, 0),  2, BLUE_DARK),
            ('INNERGRID',     (0, 1), (-1, -1), 0.5, GRAY_BORDER),
        ]
        for i in range(1, len(prod_data)):
            if i % 2 == 0:
                row_styles.append(('BACKGROUND', (0, i), (-1, i), GRAY_BG))

        prod_tbl.setStyle(TableStyle(row_styles))
        elementos.append(prod_tbl)
        elementos.append(Spacer(1, 0.25 * inch))

        # ════════════════════════════════════════════════════════════════════
        # TOTALES
        # ════════════════════════════════════════════════════════════════════
        totales_data = [
            [Paragraph('Subtotal',                         st['right']),
             Paragraph(f'${subtotal:,.2f}',                st['right'])],
        ]
        
        # Solo agregar fila de IVA si está incluido
        if incluir_iva and tasa_iva > 0:
            totales_data.append([
                Paragraph(f'Impuestos ({tasa_iva*100:.0f}%)', st['right']),
                Paragraph(f'${iva:,.2f}',                     st['right'])
            ])
        
        # Fila de total
        totales_data.append([
            Paragraph('<b>Total</b>',                     st['total_style']),
            Paragraph(f'<b>${total:,.2f} MXN</b>',        st['total_style'])
        ])
        
        totales_tbl = Table(totales_data, colWidths=[1.6*inch, 1.6*inch])
        
        # Ajustar el índice de la línea superior según si hay IVA o no
        linea_total_idx = 2 if (incluir_iva and tasa_iva > 0) else 1
        
        totales_tbl.setStyle(TableStyle([
            ('TOPPADDING',    (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 0),
            ('LINEABOVE',     (0, linea_total_idx), (-1, linea_total_idx),  2, BLUE_DARK),
            ('TOPPADDING',    (0, linea_total_idx), (-1, linea_total_idx),  10),
            ('BOTTOMPADDING', (0, linea_total_idx), (-1, linea_total_idx),  10),
        ]))

        wrapper = Table([[totales_tbl]], colWidths=[CONTENT_W])
        wrapper.setStyle(TableStyle([
            ('LEFTPADDING',   (0, 0), (-1, -1), CONTENT_W - TOTALES_W),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 0),
            ('TOPPADDING',    (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        elementos.append(wrapper)

        # ════════════════════════════════════════════════════════════════════
        # FOOTER
        # ════════════════════════════════════════════════════════════════════
        elementos.append(Spacer(1, 0.4 * inch))
        elementos.append(
            HRFlowable(width="100%", thickness=1, color=GRAY_BORDER, spaceAfter=10)
        )
        footer_tbl = Table(
            [[Paragraph(
                'Gracias por su preferencia. '
                'Esta cotización es válida por 30 días a partir de la fecha de emisión.',
                st['muted_center']
            )]],
            colWidths=[CONTENT_W]
        )
        footer_tbl.setStyle(TableStyle([
            ('BACKGROUND',    (0, 0), (-1, -1), GRAY_BG),
            ('LEFTPADDING',   (0, 0), (-1, -1), 14),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 14),
            ('TOPPADDING',    (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elementos.append(footer_tbl)

        doc.build(elementos)
        return True

    except Exception as e:
        print(f"Error al generar PDF: {e}")
        import traceback
        traceback.print_exc()
        return False