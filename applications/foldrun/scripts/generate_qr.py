"""Generate QR code SVG for FoldRun demo video.

Usage:
    uv venv /tmp/qr-venv
    source /tmp/qr-venv/bin/activate
    uv pip install "qrcode[pil]"
    python generate_qr.py
"""

import qrcode
import qrcode.image.svg

DEMO_URL = "https://youtu.be/umTLrEF5L7A"
OUTPUT_PATH = "../foldrun-qr.svg"

factory = qrcode.image.svg.SvgPathImage
qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10,
    border=2,
)
qr.add_data(DEMO_URL)
qr.make(fit=True)
img = qr.make_image(image_factory=factory)
img.save(OUTPUT_PATH)
print(f"QR code saved to {OUTPUT_PATH}")
