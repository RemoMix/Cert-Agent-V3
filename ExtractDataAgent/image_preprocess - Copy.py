import cv2
import numpy as np
from pathlib import Path

def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    if coords.size == 0:
        return image

    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # ignore very small angles
    if abs(angle) < 0.5:
        return image

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(
        image, M, (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )

def preprocess(image_path: Path) -> None:
    """
    Global, safe preprocessing for full certificate page.
    Designed to improve OCR stability without breaking text.
    """

    img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        return

    # 1️⃣ Upscale slightly (improves digit shapes)
    img = cv2.resize(
        img, None,
        fx=1.25,
        fy=1.25,
        interpolation=cv2.INTER_CUBIC
    )

    # 2️⃣ Mild Gaussian blur (preserve strokes)
    img = cv2.GaussianBlur(img, (3, 3), 0)

    # 3️⃣ Gentle contrast normalization (NOT CLAHE)
    img = cv2.normalize(
        img, None,
        alpha=0,
        beta=255,
        norm_type=cv2.NORM_MINMAX
    )

    # 4️⃣ Adaptive threshold (balanced)
    img = cv2.adaptiveThreshold(
        img,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        23,   # balance between text & digits
        4
    )

    # 5️⃣ Morphology OPEN (remove noise)
    open_kernel = np.ones((2, 2), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, open_kernel)

    # 6️⃣ Very light CLOSE (protect digits)
    close_kernel = np.ones((1, 1), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, close_kernel)

    img = deskew(img)

    img = img[5:-5, 5:-5]


    cv2.imwrite(str(image_path), img)

    
