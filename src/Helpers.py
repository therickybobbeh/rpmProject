import cv2
import numpy as np

class Helpers:
    @staticmethod
    def compare_images(image1, image2) -> bool:
        diff = cv2.absdiff(image1, image2)
        non_zero_count = np.count_nonzero(diff)
        # adjust threashold pixles as needed
        if non_zero_count < 500:
            return True
        return False