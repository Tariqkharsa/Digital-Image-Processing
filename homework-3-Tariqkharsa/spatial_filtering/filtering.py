import numpy as np

class Filtering:

    def __init__(self, image):
        self.image = image

    def get_gaussian_filter(self):
        """Initialzes/Computes and returns a 5X5 Gaussian filter"""
        g_filter = np.zeros((5,5))
        sigma = 1
        row = 0
        column = 0
        for i in range(-2,3):
            for j in range(-2,3):
                g_filter[row][column] = (1/(2*np.pi*sigma**2))*np.exp(-1*(i**2 + j**2)/(2*sigma**2))
                column+=1
            column = 0
            row+=1
        return g_filter

    def get_laplacian_filter(self):
        """Initialzes and returns a 3X3 Laplacian filter"""
        arr = [[0,1,0],[1,-4,1],[0,1,0]]
        l_filter = np.array(arr)
        return l_filter

    def filter(self, filter_name):
        """Perform filtering on the image using the specified filter, and returns a filtered image
            takes as input:
            filter_name: a string, specifying the type of filter to use ["gaussian", laplacian"]
            return type: a 2d numpy array
                """
        r,c = self.image.shape
        input_image = (self.image).copy()
        res_image = np.zeros((r,c))
        if filter_name == "gaussian": 
            sum = 0
            gas_filter = Filtering.get_gaussian_filter(self)
            gr, gc = gas_filter.shape
            pad_image = np.zeros((r+2*(gr-1),c+2*(gc-1)))
            pad_r, pad_c = pad_image.shape
            for i in range((gr-1),pad_r-(gr-1)):
                for j in range((gc-1),pad_c-(gc-1)):
                    pad_image[i][j] = input_image[i-(gr-1)][j-(gc-1)]
            for i in range(pad_r-2*(gr-1)):
                for j in range(pad_c-2*(gc-1)):
                    for y in range(gr):
                        for x in range(gc):
                            sum = sum + gas_filter[y][x]*pad_image[i+y+(gr//2)][j+x+(gc//2)]
                    res_image[i][j] = sum
                    sum = 0                 
        if filter_name == "laplacian":
            sum = 0
            lap_filter = Filtering.get_laplacian_filter(self)
            lr, lc = lap_filter.shape
            pad_image = np.zeros((r+2*(lr-1),c+2*(lc-1)))
            pad_r, pad_c = pad_image.shape
            for i in range((lr-1),pad_r-(lr-1)):
                for j in range((lc-1),pad_c-(lc-1)):
                    pad_image[i][j] = input_image[i-(lr-1)][j-(lc-1)]
            for i in range(pad_r-2*(lr-1)):
                for j in range(pad_c-2*(lc-1)):
                    for y in range(lr):
                        for x in range(lc):
                            sum = sum + lap_filter[y][x]*pad_image[i+y+(lr//2)][j+x+(lc//2)]
                    res_image[i][j] = sum
                    sum = 0 
        return res_image

