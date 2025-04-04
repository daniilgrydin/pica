import cv2
import numpy as np
from typing import List

class Resources:
    def __init__(self, target: str):
        img: np.ndarray = cv2.imread(target)
        self.target: np.ndarray = cv2.resize(img, (128, 128))
        
        image: np.ndarray = cv2.imread("resources/petscii.png", cv2.IMREAD_GRAYSCALE)
        self.tiles: List[np.ndarray] = [
            image[i * 8:i * 8 + 8, j * 8:j * 8 + 8] 
            for i in range(image.shape[0] // 8) 
            for j in range(image.shape[1] // 8)
        ]
        
        self.colours: np.ndarray = np.array([
            [0x00, 0x00, 0x00], [0xFF, 0xFF, 0xFF], [0x2B, 0x37, 0x68], [0xB2, 0xA4, 0x70],
            [0x86, 0x3D, 0x6F], [0x43, 0x8D, 0x58], [0x79, 0x28, 0x35], [0x6F, 0xC7, 0xB8],
            [0x25, 0x4F, 0x6F], [0x00, 0x39, 0x43], [0x59, 0x67, 0x9A], [0x44, 0x44, 0x44],
            [0x6C, 0x6C, 0x6C], [0x84, 0xD2, 0x9A], [0xB5, 0x5E, 0x6C], [0x95, 0x95, 0x95]
        ], dtype=np.uint8)  # Commodore 64 colours
        
        # Sort colours by brightness
        self.colours = np.array(sorted(self.colours, key=lambda x: -np.mean(x)), dtype=np.uint8)
        
        # Sort tiles by brightness
        self.tiles = sorted(self.tiles, key=lambda x: -np.mean(x))