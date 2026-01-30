import cv2
import numpy as np
from pathlib import Path


def preprocess(image_path: Path) -> None:
    img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)

    if img is None:
        return
    
    # زيادة بسيطة في الـ DPI قبل أي حاجة
    img = cv2.resize(
        img,
        None,
        fx=1.3,
        fy=1.3,
        interpolation=cv2.INTER_CUBIC
    )

    # 1️⃣ اختار واحد بسمش الاتنين مع بعض
    # Gaussian blur خفيف (يحافظ على tails)
    #img = cv2.GaussianBlur(img, (3, 3), 0)
    # Median blur بدل Gaussian
    img = cv2.medianBlur(img, 3)

    # 2️⃣ Adaptive threshold (أهدى)
    img = cv2.adaptiveThreshold(
        img, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        21,   # أصغر من 31
        3     # أقل من 5
    )

    # 3️⃣ Opening لإزالة noise الصغيرة
    open_kernel = np.ones((2, 2), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, open_kernel)

    # 4️⃣ Closing خفيف جدًا (اختياري بس مفيد)
    close_kernel = np.ones((1, 1), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, close_kernel)

    cv2.imwrite(str(image_path), img)
