import numpy as np
import random
import math
class Coloring:

    def intensity_slicing(self, image, n_slices):
        '''
       Convert greyscale image to color image using color slicing technique.
       takes as input:
       image: the grayscale input image
       n_slices: number of slices
        
       Steps:
 
        1. Split the exising dynamic range (0, k-1) using n slices (creates n+1 intervals)
        2. Randomly assign a color to each interval
        3. Create and output color image
        4. Iterate through the image and assign colors to the color image based on which interval the intensity belongs to
 
       returns colored image
       '''
        random.seed(7)
        r,c = image.shape
        intervals = []
        for i in range(1,n_slices+2):
            intervals.append(i*(255/(n_slices+1)))
        out_image = np.zeros((r,c,3))
        color_interval = np.zeros((n_slices+1,3))
        for i in range(n_slices+1):
            for j in range(3):
                color_interval[i][j] = (random.random()*256)//1
        for i in range(r):
            for j in range(c):
                for x in range(len(intervals)):
                    if image[i][j] < intervals[x]:
                        out_image[i][j][0] = color_interval[x][0]
                        out_image[i][j][1] = color_interval[x][1]
                        out_image[i][j][2] = color_interval[x][2]
                        break
        return out_image

    def color_transformation(self, image, n_slices, theta):
        '''
        Convert greyscale image to color image using color transformation technique.
        takes as input:
        image:  grayscale input image
        colors: color array containing RGB values
        theta: (phase_red, phase,_green, phase_blue) a tuple with phase values for (r, g, b) 
        Steps:
  
         1. Split the exising dynamic range (0, k-1) using n slices (creates n+1 intervals)
         2. create red values for each slice using 255*sin(slice + theta[0])
            similarly create green and blue using 255*sin(slice + theta[1]), 255*sin(slice + theta[2])
         3. Create and output color image
         4. Iterate through the image and assign colors to the color image based on which interval the intensity belongs to
  
        returns colored image
        '''
        r,c = image.shape
        intervals = []
        for i in range(n_slices+2):
            intervals.append(i*(255/(n_slices+1)))
        out_image = np.zeros((r,c,3))
        for i in range(r):
            for j in range(c):
                for x in range(len(intervals)):
                    if image[i][j] < intervals[x]:
                        center = (intervals[x] + intervals[x-1])/2
                        out_image[i][j][0] = abs((255*math.sin(center + theta[0]))//1)
                        out_image[i][j][1] = abs((255*math.sin(center + theta[1]))//1)
                        out_image[i][j][2] = abs((255*math.sin(center + theta[2]))//1)
                        break
        return out_image



        

