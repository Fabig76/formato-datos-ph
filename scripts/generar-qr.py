#!/usr/bin/env python3
"""
Genera un QR apuntando a la URL del formulario público de una PH.

Uso:
  python generar-qr.py "https://[usuario].github.io/[repo]/"
  python generar-qr.py "https://ejemplo.com/form" --output mi-qr.png
  python generar-qr.py "https://ejemplo.com" --no-decorate

Salida (en el directorio actual):
  - qr-formulario.png       (con texto decorado, listo para imprimir)
  - qr-solo.png             (solo el QR, minimalista)
"""

import argparse
import os
import sys

try:
    import qrcode
    from qrcode.constants import ERROR_CORRECT_H
except ImportError:
    print("ERROR: Falta la librería qrcode.")
    print("Instala con: pip install --break-system-packages qrcode[pil]")
    sys.exit(1)

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("ERROR: Falta la librería Pillow.")
    print("Instala con: pip install --break-system-packages Pillow")
    sys.exit(1)


def generate_qr(url, output_path, decorate=True, ph_name=None, nit=None, address=None):
    # Construir QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=ERROR_CORRECT_H,  # H = alta (permite logo encima)
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img_qr = qr.make_image(fill_color="#0066CC", back_color="white").convert("RGB")

    if not decorate:
        img_qr.save(output_path, "PNG", optimize=True)
        return

    # Generar imagen compuesta con texto + QR
    W, H = 800, 1050
    canvas = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(canvas)

    # Intentar cargar fuentes del sistema
    try:
        font_titulo = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
        font_url = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except OSError:
        font_titulo = font_sub = font_url = ImageFont.load_default()

    # Textos (con defaults)
    title = ph_name or "Tu Propiedad Horizontal"
    nit_text = f"NIT {nit}" if nit else ""
    address_text = address or ""
    header_label = "FORMULARIO DE RESIDENTES"

    # Dibujar textos del header
    draw.text((W/2, 60), title, fill="#004C99", font=font_titulo, anchor="mm")
    if nit_text or address_text:
        sub = "  ·  ".join(filter(None, [nit_text, address_text]))
        draw.text((W/2, 105), sub, fill="#666666", font=font_sub, anchor="mm")
    draw.text((W/2, 145), header_label, fill="#0066CC", font=font_sub, anchor="mm")

    # Centrar QR
    qr_w, qr_h = img_qr.size
    qr_max = 600
    if qr_w > qr_max:
        ratio = qr_max / qr_w
        img_qr = img_qr.resize((qr_max, int(qr_h * ratio)), Image.LANCZOS)
        qr_w, qr_h = img_qr.size
    canvas.paste(img_qr, ((W - qr_w)//2, 230))

    # Textos debajo del QR
    y = 230 + qr_h + 40
    draw.text((W/2, y), "Escanea este codigo con tu celular", fill="#333333", font=font_sub, anchor="mm")
    y += 35
    draw.text((W/2, y), "para acceder al formulario de actualizacion", fill="#333333", font=font_sub, anchor="mm")
    y += 35
    draw.text((W/2, y), "de datos de residentes.", fill="#333333", font=font_sub, anchor="mm")
    y += 50

    draw.text((W/2, y), "O ingresa a:", fill="#666666", font=font_url, anchor="mm")
    y += 28
    # Si la URL es muy larga, partirla
    if len(url) > 50:
        # Buscar un punto de corte natural
        mid = len(url) // 2
        for sep in ["/", ":"]:
            idx = url.find(sep, mid - 10)
            if idx > 0:
                draw.text((W/2, y), url[:idx+1], fill="#0066CC", font=font_url, anchor="mm")
                y += 25
                draw.text((W/2, y), url[idx+1:], fill="#0066CC", font=font_url, anchor="mm")
                break
        else:
            draw.text((W/2, y), url, fill="#0066CC", font=font_url, anchor="mm")
    else:
        draw.text((W/2, y), url, fill="#0066CC", font=font_url, anchor="mm")
    y += 60

    draw.text((W/2, H - 30), "Conforme a la Ley 1581 de 2012 y Decreto 768 de 2025",
              fill="#999999", font=font_url, anchor="mm")

    canvas.save(output_path, "PNG", optimize=True)


def main():
    parser = argparse.ArgumentParser(
        description="Genera un QR para el formulario público de una PH"
    )
    parser.add_argument("url", help="URL pública del formulario")
    parser.add_argument("--output", default="qr-formulario.png",
                        help="Archivo de salida (default: qr-formulario.png)")
    parser.add_argument("--ph-name", help="Nombre de la PH (para el header decorado)")
    parser.add_argument("--nit", help="NIT de la PH")
    parser.add_argument("--address", help="Dirección de la PH")
    parser.add_argument("--no-decorate", action="store_true",
                        help="Solo el QR, sin texto decorado")

    args = parser.parse_args()

    output = args.output
    if not output.endswith(".png"):
        output += ".png"

    decorate = not args.no_decorate

    generate_qr(args.url, output, decorate=decorate,
                ph_name=args.ph_name, nit=args.nit, address=args.address)
    print(f"QR guardado en: {os.path.abspath(output)}")

    if decorate:
        # Generar también el QR solo
        solo_path = output.replace(".png", "-solo.png")
        if solo_path == output:
            solo_path = "qr-solo.png"
        generate_qr(args.url, solo_path, decorate=False,
                    ph_name=args.ph_name, nit=args.nit, address=args.address)
        print(f"QR solo guardado en: {os.path.abspath(solo_path)}")


if __name__ == "__main__":
    main()
