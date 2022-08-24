import numpy as np
class Filtering:

    def __init__(self, image, filter_name, filter_size, var = None):
        """initializes the variables of spatial filtering on an input image
        takes as input:
        image: the noisy input image
        filter_name: the name of the filter to use
        filter_size: integer value of the size of the fitler
        global_var: noise variance to be used in the Local noise reduction filter
        S_max: Maximum allowed size of the window that is used in adaptive median filter
        """

        self.image = image

        if filter_name == 'arithmetic_mean':
            self.filter = self.get_arithmetic_mean
        elif filter_name == 'geometric_mean':
            self.filter = self.get_geometric_mean
        if filter_name == 'local_noise':
            self.filter = self.get_local_noise
        elif filter_name == 'median':
            self.filter = self.get_median
        elif filter_name == 'adaptive_median':
            self.filter = self.get_adaptive_median

        self.filter_size = filter_size
        self.global_var = var
        self.S_max = 15

    def get_arithmetic_mean(self, roi):
        """Computes the arithmetic mean of the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the arithmetic mean value of the roi"""
        ari_mean = 0
        for i in range(len(roi)):
            ari_mean = ari_mean + roi[i]
        ari_mean = ari_mean/len(roi)
        return ari_mean

    def get_geometric_mean(self, roi):
        """Computes the geometric mean for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the geometric mean value of the roi"""
        geo_mean = 1
        for i in range(len(roi)):
            geo_mean = geo_mean * roi[i]
        geo_mean = geo_mean**(1/len(roi))
        return geo_mean

    def get_local_noise(self, roi):
        """Computes the local noise reduction value
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the local noise reduction value of the roi"""
        local_mean = 0
        local_var = 0
        global_var = self.global_var
        var_sum = 0
        for i in range(len(roi)):
            local_mean = local_mean + roi[i]
        local_mean = local_mean/len(roi)
        for i in range(len(roi)):
            var_sum = var_sum + (roi[i] - local_mean) ** 2
        local_var = var_sum/len(roi)
        g_xy = roi[len(roi)//2]
        f_xy = g_xy - (global_var/local_var)*(g_xy-local_mean)
        return f_xy

    def get_median(self, roi):
        """Computes the median for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the median value of the roi"""
        sorted_roi = roi
        sorted_roi.sort()
        roi_size = len(roi)
        median = 0
        if roi_size % 2 == 0:
            median1 = sorted_roi[roi_size//2]
            median2 = sorted_roi[roi_size//2 - 1]
            median = (median1 + median2)/2
        else:
            median = sorted_roi[roi_size//2]
        return median


    def get_adaptive_median(self, pad_image, fz, i, j):
        """Use this function to implment the adaptive median.
        It is left up to the student to define the input to this function and call it as needed. Feel free to create
        additional functions as needed.
        """   
        offset = self.S_max -fz
        roi = []
        for y in range(fz):
            for x in range(fz):
                roi.append(pad_image[y+i+offset][x+j+offset])
        min_val = min(roi)
        max_val = max(roi)
        med_val = self.get_median(roi)
        g_xy = roi[len(roi)//2]
        S_max = self.S_max
        a1 = med_val - min_val
        a2 = med_val - max_val
        b1 = g_xy - min_val
        b2 = g_xy - max_val
        if a1 > 0  and a2 < 0:
            if b1 > 0  and b2 < 0:
                return g_xy
            else:
                return med_val
        else:
            if fz > S_max:
                return med_val
            else:
                fz = fz + 2
                return self.get_adaptive_median(pad_image, fz, i, j)


    def filtering(self):
        """performs filtering on an image containing gaussian or salt & pepper noise
        returns the denoised image
        ----------------------------------------------------------
        Note: Here when we perform filtering we are not doing convolution.
        For every pixel in the image, we select a neighborhood of values defined by the kernal and apply a mathematical
        operation for all the elements with in the kernel. For example, mean, median and etc.

        Steps:
        1. add the necesssary zero padding to the noisy image, that way we have sufficient values to perform the operati
        ons on the pixels at the image corners. The number of rows and columns of zero padding is defined by the kernel size
        2. Iterate through the image and every pixel (i,j) gather the neighbors defined by the kernel into a list (or any data structure)
        3. Pass these values to one of the filters that will compute the necessary mathematical operations (mean, median, etc.)
        4. Save the results at (i,j) in the ouput image.
        5. return the output image

        Note: You can create extra functions as needed. For example if you feel that it is easier to create a new function for
        the adaptive median filter as it has two stages, you are welcome to do that.
        For the adaptive median filter assume that S_max (maximum allowed size of the window) is 15
        """
        r,c = self.image.shape
        fz = self.filter_size
        s_max = self.S_max
        if self.filter == self.get_adaptive_median:
            pad_image = np.zeros((r+2*s_max//2,c+2*s_max//2))
            for i in range(r):
                for j in range(c):
                    pad_image[i+s_max//2][j+s_max//2] = self.image[i][j]
        else:
            pad_image = np.zeros((r+2*fz//2,c+2*fz//2))
            for i in range(r):
                for j in range(c):
                    pad_image[i+fz//2][j+fz//2] = self.image[i][j]


        out_image = self.image.copy()


        for i in range(r):
            for j in range(c):
                arr1 = []
                for y in range(fz):
                    for x in range(fz):
                        arr1.append(pad_image[y+i][x+j])

                if self.filter == self.get_adaptive_median:
                    out_image[i][j] = self.filter(pad_image, fz, i , j)
                else:
                    out_image[i][j] = self.filter(arr1)
        return out_image

