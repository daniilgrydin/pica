import cv2
import numpy as np

class Resources:
    def __init__(self, target):
        img = cv2.imread(target)
        self.target = cv2.resize(img, (128, 128))
        image = cv2.imread("resources/petscii.png", cv2.IMREAD_GRAYSCALE)
        self.tiles = [image[i*8:i*8+8, j*8:j*8+8] for i in range(image.shape[0]//8) for j in range(image.shape[1]//8)]
        self.colours = np.array([
            [0x00, 0x00, 0x00], [0xFF, 0xFF, 0xFF], [0x2B, 0x37, 0x68], [0xB2, 0xA4, 0x70],
            [0x86, 0x3D, 0x6F], [0x43, 0x8D, 0x58], [0x79, 0x28, 0x35], [0x6F, 0xC7, 0xB8],
            [0x25, 0x4F, 0x6F], [0x00, 0x39, 0x43], [0x59, 0x67, 0x9A], [0x44, 0x44, 0x44],
            [0x6C, 0x6C, 0x6C], [0x84, 0xD2, 0x9A], [0xB5, 0x5E, 0x6C], [0x95, 0x95, 0x95]
        ], dtype=np.uint8) # Commodore 64 colours
        
        # self.colours = np.concatenate((self.colours, np.array([
        #     [0, 0, 0], [29, 43, 83], [126, 37, 83], [0, 135, 81],
        #     [171, 82, 54], [95, 87, 79], [194, 195, 199], [255, 241, 232],
        #     [255, 0, 77], [255, 163, 0], [255, 236, 39], [0, 228, 54],
        #     [41, 173, 255], [131, 118, 156], [255, 119, 168], [255, 204, 170],
        #     [41, 24, 20], [17, 29, 53], [66, 33, 54], [18, 83, 89],
        #     [116, 47, 41], [73, 51, 59], [162, 136, 121], [243, 239, 125],
        #     [190, 18, 80], [255, 108, 36], [168, 231, 46], [0, 181, 67],
        #     [6, 90, 181], [117, 70, 101], [255, 110, 89], [255, 157, 129]
        # ], dtype=np.uint8))) # PICO-8 colours
        
        # sort colours by brightness
        self.colours = np.array(sorted(self.colours, key=lambda x: -np.mean(x)), dtype=np.uint8)
        
        
        # revert the order of colour channels
        # self.colours = self.colours[:, ::-1]
        
        # sort tiles by brightness
        self.tiles = sorted(self.tiles, key=lambda x: -np.mean(x))