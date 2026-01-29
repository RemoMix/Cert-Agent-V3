import cv2
import numpy as np
from pathlib import Path

def preprocess(image_path: Path) -> None:
    img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)

    img = cv2.adaptiveThreshold(
        img, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 5
    )

    kernel = np.ones((1, 1), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    cv2.imwrite(str(image_path), img)
