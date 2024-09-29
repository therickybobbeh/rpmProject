
# To activate image processing, uncomment the following imports:
# from PIL import Image
import numpy as np
import cv2
from src import Helpers
from src.Node import Node
from copy import deepcopy
from src.Actions import Actions
from collections import deque



#TODO: REOMVE THIS
import matplotlib.pyplot as plt




class Agent:
    def __init__(self):
        """
        The default constructor for your Agent. Make sure to execute any processing necessary before your Agent starts
        solving problems here. Do not add any variables to this signature; they will not be used by main().
        
        This init method is only called once when the Agent is instantiated 
        while the Solve method will be called multiple times.
        """

        self.actions = []
        # self.problems_converted = None
        self.images_data = {}
        self.helpers = Helpers.Helpers()
        self.problem = None

        self.actions = [
            ("flip_vertical", Actions.flip_vertical),
            ("flip_horizontal", Actions.flip_horizontal),
            ("rotate_90", Actions.rotate_90),
            ("rotate_180", Actions.rotate_180),
            ("rotate_270", Actions.rotate_270)
        ]

        self.filters = [
            ("filter_xor", Actions.filter_xor),
            ("filter_and", Actions.filter_and),
            ("filter_or", Actions.filter_or),
            ("filter_not", Actions.filter_not)
        ]

    def Solve(self, problem):
        """
        Primary method for solving incoming Raven's Progressive Matrices.

        Args:
            problem: The RavensProblem instance.

        Returns:
            int: The answer (1-6 for 2x2 OR 1-8 for 3x3) : Remember that the Autograder will have up to 2 additional images for answers.
            Return a negative number to skip a problem.
            Remember to return the answer [Key], not the name, as the ANSWERS ARE SHUFFLED in Gradescope.
        """

        '''
        DO NOT use absolute file pathing to open files.
        
        Example: Read the 'A' figure from the problem using Pillow
            image_a = Image.open(problem.figures["A"].visualFilename)
            
        Example: Read the '1' figure from the problem using OpenCv
            image_1 = cv2.imread(problem.figures["1"].visualFilename)
            
        Don't forget to uncomment the imports as needed!
        '''

        #TODO: later we can add a driver for the type of problem
        self.problem = problem
        self.build(problem)
        # self.find_match_a_and_b()
        # self.preform_actions_on_c()
        # self.find_match()


        # if shape a = b

        if self.helpers.compare_images(self.images_data.get("A"), self.images_data.get("B")):
            return self.find_matching_number_for_image(self.images_data.get("C"))

        # if shape a != b

        # check the tree to see if any transofrmations match
        node_a = Node(image_name="A", image_data=self.images_data.get("A"))
        A_to_B = self.find_match_1_and_2(node_a, self.images_data.get("B"), self.images_data.get("C"))
        if A_to_B is not None:
            return A_to_B
        else:
            #TODO: clean up for memeory

            return -1




        # check the shapes are contained in both with contours
            # run the find match a and b

        # if a != b, a = c
            # check what it takes to transform b into c,
            # transform c using the same transformations

        return -1


        # return 2



    def build (self, problem):
        """
        Used to turn the initial passed in problem into an object storing all of the images in opencv greyscale
        Then will initialize A and B and run the find_match def which returns a list of the actions preformed to find a
        match, for now if it cant find one it will return a random number
        """
        for figure_name, figure in problem.figures.items():
            image = cv2.imread(figure.visualFilename, cv2.IMREAD_GRAYSCALE)
            self.images_data[figure_name] = image





    #TODO: may not want to pass image since it uses more memory than reff the global
    def find_match_1_and_2(self, node1: Node, image_being_compared, image_to_preform_transformations_on):
        '''
        this will return a list of actions to preform
        '''
        # Base case
        if node1 is None:
            return
        if node1.depth == 0:
            # Apply all actions and generate children at depth 1
            for action_name, action_fn in self.actions:
                orientation_action = action_fn(node1.image_data)
                child_node = deepcopy(node1)
                child_node.parent = node1
                child_node.image_data = orientation_action
                child_node.actions.append(action_name)
                child_node.depth += 1
                node1.children.append(child_node)
            # generate layer 2
            # self.apply_filters_to_children(node1.children, image)


            # find first sucessful state
            matching_nodes_actions = self.find_matching_node(node1, image_being_compared)
            if matching_nodes_actions is not None:
                #issue here
                answer_img = self.preform_action_list(matching_nodes_actions, image_to_preform_transformations_on)
                for current_img_name in self.images_data:
                    if current_img_name.isdigit():
                        if self.helpers.compare_images(answer_img, self.images_data[current_img_name]):
                            return int(current_img_name)

            else:
                return None




    def find_matching_node(self, node: Node, image_being_compared):
        # The BFS algorithm used here is an adaptation of the example used on this page and in previous assignments
        # https://codereview.stackexchange.com/questions/135156/bfs-implementation-in-python-3

        queue = deque([(node)])
        # Perform BFS
        while queue:
            # Dequeue the next node and its depth from the front of the queue
            current_node = queue.popleft()
            # Check if this node is solved
            if self.helpers.compare_images(current_node.image_data, image_being_compared):
                return current_node.actions
            for child in current_node.children:
                queue.append(child)
        return None


    def apply_filters_to_children(self, children_nodes, image):
        """
        This function applies filters to each child node.
        For every child created from an action, it applies all filters and adds those filtered nodes as children.
        """
        for child_node in children_nodes:
            for filter_name, filter_fn in self.filters:
                filter_action = filter_fn(child_node.image_data, image)
                if filter_action is not None:
                    filter_child_node = deepcopy(child_node)
                    filter_child_node.parent = child_node
                    filter_child_node.image_data = filter_action
                    filter_child_node.actions.append(filter_name)
                    filter_child_node.depth += 1
                    child_node.children.append(filter_child_node)

    def preform_action_list(self, action_list_to_preform, image_to_preform_transformations_on):
        for action_name in action_list_to_preform:
            for available_action_name, action_fn in self.actions:
                if np.array_equal(action_name, available_action_name):  # Use np.array_equal for array comparison
                    image = action_fn(image_to_preform_transformations_on)
                    #todo: we need the final result before we can do xor operations on it
        # for filter_name in action_list_to_preform:
        #     for available_filter_name, filter_fn in self.filters:
        #         if np.array_equal(filter_name, available_filter_name):  # Use np.array_equal for array comparison
        #             image = filter_fn(image, )
        return image



    def find_matching_number_for_image(self, image):
        for key in self.images_data:
            if key.isdigit():
                if self.helpers.compare_images(image, self.images_data.get(key)):
                    return int(key)