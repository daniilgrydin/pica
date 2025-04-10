"""
Resources class for managing target images, tiles, and colors.

This class loads and processes the target image, PETSCII tiles, and Commodore 64 colors
for use in the genetic algorithm.

Author: Daniil Grydin
Date: April 1, 2025
"""

import cv2
import numpy as np
from typing import List

# Constants
TILE_SIZE: int = 8
TARGET_SIZE: int = 128
TILE_IMAGE_PATH: str = "resources/petscii.png"

class Resources:
    """
    A class to manage shared resources for the genetic algorithm.

    This includes the target image, PETSCII tiles, and Commodore 64 colors.
    """

    def __init__(self, target_path: str):
        """
        Initialize the Resources instance.

        Args:
            target_path (str): Path to the target image file.
        """
        # Load and resize the target image
        target_image: np.ndarray = cv2.imread(target_path)
        if target_image is None:
            raise FileNotFoundError(f"Target image not found at {target_path}")
        self.target: np.ndarray = cv2.resize(target_image, (TARGET_SIZE, TARGET_SIZE))

        # Load and process PETSCII tiles
        tile_image: np.ndarray = cv2.imread(TILE_IMAGE_PATH, cv2.IMREAD_GRAYSCALE)
        if tile_image is None:
            raise FileNotFoundError(f"Tile image not found at {TILE_IMAGE_PATH}")
        self.tiles: List[np.ndarray] = self._extract_tiles(tile_image)

        # Define Commodore 64 colors
        self.colours: np.ndarray = self._initialize_colours()

        # Sort colors and tiles by brightness
        self.colours = self._sort_by_brightness(self.colours)
        self.tiles = self._sort_by_brightness(self.tiles)

    def _extract_tiles(self, tile_image: np.ndarray) -> List[np.ndarray]:
        """
        Extract individual tiles from the PETSCII tile image.

        Args:
            tile_image (np.ndarray): The grayscale image containing all tiles.

        Returns:
            List[np.ndarray]: A list of individual tile images.
        """
        return [
            tile_image[i * TILE_SIZE:(i + 1) * TILE_SIZE, j * TILE_SIZE:(j + 1) * TILE_SIZE]
            for i in range(tile_image.shape[0] // TILE_SIZE)
            for j in range(tile_image.shape[1] // TILE_SIZE)
        ]

    def _initialize_colours(self) -> np.ndarray:
        """
        Initialize the Commodore 64 color palette.

        Returns:
            np.ndarray: An array of RGB colors.
        """
        return np.array([
            [0x00, 0x00, 0x00], [0xFF, 0xFF, 0xFF], [0x2B, 0x37, 0x68], [0xB2, 0xA4, 0x70],
            [0x86, 0x3D, 0x6F], [0x43, 0x8D, 0x58], [0x79, 0x28, 0x35], [0x6F, 0xC7, 0xB8],
            [0x25, 0x4F, 0x6F], [0x00, 0x39, 0x43], [0x59, 0x67, 0x9A], [0x44, 0x44, 0x44],
            [0x6C, 0x6C, 0x6C], [0x84, 0xD2, 0x9A], [0xB5, 0x5E, 0x6C], [0x95, 0x95, 0x95]
        ], dtype=np.uint8)

    def _sort_by_brightness(self, array: List[np.ndarray] | np.ndarray) -> List[np.ndarray] | np.ndarray:
        """
        Sort an array of tiles or colors by brightness.

        Args:
            array (List[np.ndarray] | np.ndarray): The array to sort.

        Returns:
            List[np.ndarray] | np.ndarray: The sorted array.
        """
        return sorted(array, key=lambda x: -np.mean(x))