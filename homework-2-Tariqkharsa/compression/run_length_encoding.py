import numpy as np

class Rle:
    def __init__(self):
        pass

    def encode_image(self,binary_image):
        """
        Compress the image
        takes as input:
        image: binary_image
        returns run length code
        """
        k = 1
        encoded_img = [binary_image[0,0]]
        previous_number = binary_image[0,0]
        r,c = binary_image.shape
        for i in range(r):
            for j in range(c):
                if i != 0 or j != 0:
                    if binary_image[i,j] != previous_number:
                        encoded_img.append(k)
                        previous_number = binary_image[i,j]
                        k = 1
                    else:
                        k += 1
                        previous_number = binary_image[i,j]
        return encoded_img 

    def decode_image(self, rle_code, height , width):
        """
        Get original image from the rle_code
        takes as input:
        rle_code: the run length code to be decoded
        Height, width: height and width of the original image
        returns decoded binary image
        """
        decoded_img = np.zeros((height, width))
        cur_Color = rle_code.pop(0)
        for i in range(height):
            for j in range(width):
                try:
                    rle_code[0] = rle_code[0] - 1
                    if rle_code[0] == 0:
                        rle_code.pop(0)
                        if cur_Color == 0:
                            cur_Color = 255
                        else:
                            cur_Color = 0
                except IndexError:
                    break
                decoded_img[i,j] = cur_Color
        return decoded_img





        




