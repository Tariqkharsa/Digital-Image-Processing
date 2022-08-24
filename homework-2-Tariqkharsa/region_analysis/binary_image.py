class BinaryImage:
    def __init__(self):
        pass

    def compute_histogram(self, image):
        """Computes the histogram of the input image
        takes as input:
        image: a grey scale image
        returns a histogram as a list"""

        hist = [0]*256
        r,c = image.shape
        for i in range(r):
            for j in range(c):
                hist[image[i][j]]+=1
        return hist

    def find_otsu_threshold(self, hist):
        """analyses a histogram it to find the otsu's threshold assuming that the input hstogram is bimodal histogram
        takes as input
        hist: a bimodal histogram
        returns: an optimal threshold value (otsu's threshold)"""
        total = 0
        max = 0
        for i in range(len(hist)):
            total = total + hist[i]
        threshold = 0
        tmax = [0]*256
        for i in range(len(hist)):
            threshold = i
            wb = 0
            wf = 0
            u1 = 0
            u2 = 0
            sum1 = 0
            sum2 = 0
            for j in range(i):
                u1 = u1 + hist[j]*j
                sum1 = sum1 + hist[j]
            for k in range(i,256):
                u2 = u2 + hist[k]*k
                sum2 = sum2 + hist[k]
            wb = sum1/total
            wf = sum2/total
            if sum1 != 0:
                u1 = u1/sum1
            if sum2 != 0:    
                u2 = u2/sum2
            tmax[i] = wb*wf*(u1-u2)**2
        for i in range(len(tmax)):
            if tmax[i] > max:
                max = tmax[i]
                threshold = i
        return threshold

    def binarize(self, image):
        """Comptues the binary image of the the input image based on histogram analysis and thresholding
        take as input
        image: an grey scale image
        returns: a binary image"""

        bin_img = image.copy()
        hist = self.compute_histogram(image)
        threshold = self.find_otsu_threshold(hist)
        r,c = image.shape
        for i in range(r):
            for j in range(c):
                if bin_img[i][j] > threshold:
                    bin_img[i][j] = 0
                else:
                    bin_img[i][j] = 255
        return bin_img


