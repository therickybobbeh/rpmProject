import cv2
import numpy as np

class Actions:
    def __init__(self):
        pass

    @staticmethod
    def flip_vertical(img: np.ndarray):
        return cv2.flip(img, 1)

    @staticmethod
    def flip_horizontal(img: np.ndarray):
        return cv2.flip(img, 0)

    @staticmethod
    def rotate_90(img_flipping: np.ndarray):
        # rotate 90 degrees, it goes counterclockwise
        # from https://www.geeksforgeeks.org/image-transformations-using-opencv-in-python/
        rows, cols = img_flipping.shape[:2]
        # M = np.float32([[1, 0, 0], [0, -1, rows], [0, 0, 1]])
        img_rotation = cv2.warpAffine(img_flipping,
                                      cv2.getRotationMatrix2D((cols / 2, rows / 2),
                                                              270, 1),
                                      (cols, rows))
        ##end credit block
        return img_rotation

    @staticmethod
    def rotate_180(img: np.ndarray):
        return cv2.flip(img, -1)

    @staticmethod
    def  rotate_270(img_flipping: np.ndarray):
        # rotate 270 degrees
        # from https://www.geeksforgeeks.org/image-transformations-using-opencv-in-python/
        rows, cols = img_flipping.shape[:2]
        # M = np.float32([[1, 0, 0], [0, -1, rows], [0, 0, 1]])
        img_rotation = cv2.warpAffine(img_flipping,
                                      cv2.getRotationMatrix2D((cols / 2, rows / 2),
                                                              90, 1),
                                      (cols, rows))
        ##end credit block
        return img_rotation

    ## filters
    @staticmethod
    def filter_xor(img1: np.ndarray, img2: np.ndarray):
        return cv2.bitwise_xor(img1, img2)

    @staticmethod
    def filter_and(img1: np.ndarray, img2: np.ndarray):
        return cv2.bitwise_and(img1, img2)

    @staticmethod
    def filter_or(img1: np.ndarray, img2: np.ndarray):
        return cv2.bitwise_or(img1, img2)

    @staticmethod
    def filter_not(img1: np.ndarray, img2: np.ndarray):
        return cv2.bitwise_not(img1, img2)

