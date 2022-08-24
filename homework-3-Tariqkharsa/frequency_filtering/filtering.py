# For this part of the assignment, You can use inbuilt functions to compute the fourier transform
# You are welcome to use fft that are available in numpy and opencv

import numpy as np
import math

class Filtering:

    def __init__(self, image):
        """initializes the variables for frequency filtering on an input image
        takes as input:
        image: the input image
        """
        self.image = image
        self.mask = self.get_mask

    def get_mask(self, shape):
        """Computes a user-defined mask
        takes as input:
        shape: the shape of the mask to be generated
        rtype: a 2d numpy array with size of shape
        """
        mk = np.full(shape,1)
        r,c = mk.shape
        for i in range(r):
            for j in range(c):
                if (240 < i < 250) and (230 < j < 240):
                    mk[i][j] = 0
                if (227 < i < 237) and (293 < j < 303):
                    mk[i][j] = 0
                if (274 < i < 284) and (208 < j < 218):
                    mk[i][j] = 0
                if (265 < i < 275) and (275 < j < 285):
                    mk[i][j] = 0
        return mk

    def post_process_image(self, image):
        """Post processing to display DFTs and IDFTs
        takes as input:
        image: the image obtained from the inverse fourier transform
        return an image with full contrast stretch
        -----------------------------------------------------
        You can perform post processing as needed. For example,
        1. You can perfrom log compression
        2. You can perfrom a full contrast stretch (fsimage)
        3. You can take negative (255 - fsimage)
        4. etc.
        """
        # Apply log transformation method
        row,col = image.shape
        a, b = np.min(image), np.max(image)
        contrast_image = np.zeros((row,col), dtype=np.uint8)
        for i in range(row):
            for j in range(col):
                contrast_image[i][j] = (255/(b-a)) * (image[i][j] - a) 
        return contrast_image

    def filter(self):
        """Performs frequency filtering on an input image
        returns a filtered image, magnitude of frequency_filtering, magnitude of filtered frequency_filtering
        ----------------------------------------------------------
        You are allowed to use inbuilt functions to compute fft
        There are packages available in numpy as well as in opencv
        Steps:
        1. Compute the fft of the image
        2. shift the fft to center the low frequencies
        3. get the mask (write your code in functions provided above) the functions can be called by self.filter(shape)
        4. filter the image frequency based on the mask (Convolution theorem)
        5. compute the inverse shift
        6. compute the inverse fourier transform
        7. compute the magnitude
        8. You will need to do post processing on the magnitude and depending on the algorithm (use post_process_image to write this code)
        Note: You do not have to do zero padding as discussed in class, the inbuilt functions takes care of that
        filtered image, magnitude of frequency_filtering, magnitude of filtered frequency_filtering: Make sure all images being returned have grey scale full contrast stretch and dtype=uint8
        """
        input_image = self.image
        fft_img = np.fft.fft2(input_image)
        shift_img = np.fft.fftshift(fft_img)
        mask = self.get_mask(input_image.shape)

        filter = shift_img * mask

        inverse_img = np.fft.ifftshift(filter)
        filter_img = np.fft.ifft2(inverse_img)
        mag_dft = np.absolute(shift_img)
        filter_img = np.uint8(self.post_process_image(np.absolute(filter_img)))
        mag_dft = (np.uint8(np.log(mag_dft)))* 10
        dft_filter_mag = (np.uint8(np.log((1 + np.absolute(filter)))))*10
        return filter_img, mag_dft , dft_filter_mag
