import numpy as np
import cv2

class Node:
    def __init__(self, image_name = None, image_data = None, parent = None):
        self.image_name = image_name
        self.image_data = image_data
        self.actions = []
        self.parent = parent
        self.children = []
        self.depth = 0

    # compare the nonzero elements of the images
    def __eq__(self, other_node: 'Node'):
        diff = cv2.absdiff(self.image_data, other_node.image_data)
        non_zero_count = np.count_nonzero(diff)
        if non_zero_count < 500:
            return True
        return False
