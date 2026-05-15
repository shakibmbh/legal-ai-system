
from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_angle_cls=True,
    lang='en'
)

def run_ocr(image_path):

    results = ocr.ocr(image_path)

    extracted = []

    for line in results[0]:

        text = line[1][0]
        confidence = float(line[1][1])

        extracted.append({
            "text": text,
            "confidence": confidence
        })

    return extracted
