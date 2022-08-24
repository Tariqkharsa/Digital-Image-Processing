import numpy as np
import cv2


class Operation:

    def __init__(self):
        pass

    def merge(self, image_left, image_right, column):
        """
        Merge image_left and image_right at column (column)
        
        image_left: the input image 1
        image_right: the input image 2
        column: column at which the images should be merged

        returns the merged image at column
        """
        # add your code here
        
        row,col = image_left.shape
        image_mrg = image_left.copy()
        for i in range(row):
            for j in range(column, col):
                image_mrg[i][j] = image_right[i][j]
        
        # Please do not change the structure
        return image_mrg  # Currently the original image is returned, please replace this with the merged image

    def intensity_scaling(self, input_image, column, alpha, beta):
        """
        Scale your image intensity.

        input_image: the input image
        column: image column at which left section ends
        alpha: left half scaling constant
        beta: right half scaling constant

        return: output_image
        """

        # add your code here
        row, col = input_image.shape
        image_res = input_image.copy()
        for i in range(row):
            for j in range(column):
                image_res[i][j] = alpha*image_res[i][j]
        for i in range(row):
            for j in range(column,col):
                image_res[i][j] = beta*image_res[i][j]
        # Please do not change the structure
        return image_res  # Currently the input image is returned, please replace this with the intensity scaled image

    def centralize_pixel(self, input_image, column):
        """
        Centralize your pixels (do not use np.mean)

        input_image: the input image
        column: image column at which left section ends

        return: output_image
        """

        # add your code here
        sum_left, sum_right, count_l, count_r = 0, 0, 0, 0
        row, col = input_image.shape
        image_cen = input_image.copy()
        
        for i in range(row):
            for j in range(column):
                sum_left = input_image[i][j] + sum_left
                count_l+=1
        
        for i in range(row):
            for j in range(column,col):
                sum_right = input_image[i][j] + sum_right
                count_r+=1
                
        avg_left = sum_left/count_l
        avg_right = sum_right/count_r
        o_l = 128 - avg_left
        o_r = 128 - avg_right
        
        for i in range(row):
            for j in range(column):
                if ((o_l+image_cen[i][j]) > 255):
                    image_cen[i][j] = 255
                elif ((o_l+image_cen[i][j]) < 0):
                    image_cen[i][j] = 0
                else:
                    image_cen[i][j] = image_cen[i][j] + o_l
        for i in range(row):
            for j in range(column,col):
                if ((o_r+image_cen[i][j]) > 255):
                     image_cen[i][j] = 255
                elif ((o_r+image_cen[i][j]) < 0):
                     image_cen[i][j] = 0
                else:
                     image_cen[i][j] = image_cen[i][j] + o_r
        return image_cen  # Currently the input image is returned, please replace this with the centralized image
