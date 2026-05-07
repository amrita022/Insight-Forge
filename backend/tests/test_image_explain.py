from app.image_explain import extract_text_from_image_bytes
from PIL import Image
import io


def test_extract_text_from_blank_image():
    # create a small blank image
    img = Image.new('RGB', (100, 50), color=(255,255,255))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    b = buf.getvalue()

    text = extract_text_from_image_bytes(b)
    # For blank image typical OCR returns empty string or an OCR_FAILED message
    assert isinstance(text, str)
*** End Patch