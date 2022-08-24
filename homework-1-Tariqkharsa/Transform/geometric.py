from .interpolation import interpolation
import math
import numpy as np
class Geometric:
    def __init__(self):
        pass

    def forward_rotate(self, image, theta):
        """Computes the forward rotated image by an angle theta
                image: input image
                theta: angle to rotate the image by (in radians)
                return the rotated image"""
        def mul(pointX, pointY, forward):

            x,y = 0,0

            x = math.floor(forward[0][0]*pointX + forward[0][1]*pointY)
            y = math.floor(forward[1][0]*pointX + forward[1][1]*pointY)

            return x,y
        minX, minY = 0, 0
        maxX, maxY = image.shape

        forward = [[math.cos(theta),math.sin(theta)],[-1*math.sin(theta),math.cos(theta)]]

        r1X, r1Y = mul(minX,minY, forward) # Point 1
        r2X, r2Y = mul(maxX,minY, forward) # Point 2
        r3X, r3Y = mul(minX,maxY, forward) # Point 3
        r4X, r4Y = mul(maxX,maxY, forward) # Point 4

        xVal = [r1X, r2X, r3X, r4X]
        yVal = [r1Y, r2Y, r3Y, r4Y]
        lowestX = min(xVal)
        highestX = max(xVal)

        lowestY = min(yVal)
        highestY = max(yVal)
        
        sizeX, sizeY = (highestX-lowestX), (highestY-lowestY)

        res_image = np.zeros((sizeY,sizeX))

        for i in range(maxY):
            for j in range(maxX):
                intensity = image[i][j]
                nX, nY = mul(j,i,forward)
                if nY-lowestY > 0 and nY-lowestY < sizeY and nX-lowestX > 0 and nX-lowestX < sizeX:
                    res_image[nY-lowestY][nX-lowestX] = intensity
        return res_image

    def reverse_rotation(self, rotated_image, theta, origin, original_shape):
        """Computes the reverse rotated image by an angle theta
                rotated_image: the rotated image from previous step
                theta: angle to rotate the image by (in radians)
                Origin: origin of the original image with respect to the rotated image
                Original shape: shape of the orginal image
                return the original image"""

        def mul2(pointX, pointY, inverse):

            x,y = 0,0

            x = math.floor(inverse[0][0]*pointX + inverse[0][1]*pointY)
            y = math.floor(inverse[1][0]*pointX + inverse[1][1]*pointY)

            return x,y
        reverse = [[math.cos(theta),-1*math.sin(theta)],[math.sin(theta),math.cos(theta)]]
        rr, rc = rotated_image.shape
        ofr, ofc = origin
        r,c = original_shape
        image = np.zeros((r,c))
        for i in range(rr):
            for j in range(rc):
                intensity = rotated_image[i][j]
                nX, nY = mul2(j-ofc,i-ofr,reverse)
                if 0 <= nY < r and 0 <= nX < c:
                    image[nY][nX] = intensity
        return image

    def rotate(self, image, theta, interpolation_type):
        """Computes the forward rotated image by an angle theta using interpolation
                image: the input image
                theta: angle to rotate the image by (in radians)
                interpolation_type: type of interpolation to use (nearest_neighbor, bilinear)
                return the original image"""
        geo = Geometric()
        inter = interpolation()
        fi = geo.forward_rotate(image,theta)
        forw_imag = fi.copy()

        def mul(pointX, pointY, forward):

            x,y = 0,0

            x = math.floor(forward[0][0]*pointX + forward[0][1]*pointY)
            y = math.floor(forward[1][0]*pointX + forward[1][1]*pointY)

            return x,y
        minX, minY = 0, 0
        maxX, maxY = image.shape

        forward = [[math.cos(theta),math.sin(theta)],[-1*math.sin(theta),math.cos(theta)]]

        r1X, r1Y = mul(minX,minY, forward) # Point 1
        r2X, r2Y = mul(maxX,minY, forward) # Point 2
        r3X, r3Y = mul(minX,maxY, forward) # Point 3
        r4X, r4Y = mul(maxX,maxY, forward) # Point 4

        xVal = [r1X, r2X, r3X, r4X]
        yVal = [r1Y, r2Y, r3Y, r4Y]

        lowestX = -1*min(xVal)
        lowestY = -1*min(yVal)

        print(lowestY, " ", lowestX)

        def mul2(pointX, pointY, inverse):

            x,y = 0,0

            x = math.floor(inverse[0][0]*pointX + inverse[0][1]*pointY)
            y = math.floor(inverse[1][0]*pointX + inverse[1][1]*pointY)

            return x,y

        def mul3(pointX, pointY, inverse):

            x,y = 0,0

            x = inverse[0][0]*pointX + inverse[0][1]*pointY
            y = inverse[1][0]*pointX + inverse[1][1]*pointY

            return x,y

        reverse = [[math.cos(theta),-1*math.sin(theta)],[math.sin(theta),math.cos(theta)]]
        rr, rc = forw_imag.shape
        ofr, ofc = lowestY, lowestX
        r,c = image.shape
        for i in range(rr):
            for j in range(rc):
                if interpolation_type == "nearest_neighbor":
                    mX, mY = mul2(j-ofc,i-ofr,reverse)
                    if 0 < mY < r and 0 < mX < c:
                        intensity = image[mY][mX]
                        forw_imag[i][j] = intensity
                if interpolation_type == "bilinear":
                    mX, mY = mul3(j-ofc, i-ofr, reverse)
                    if 0 < mY < r-1 and 0 < mX < c-1:
                        pt1X = math.floor(mX)
                        pt1Y = math.floor(mY)
                        pt2X = math.ceil(mX)
                        pt2Y = math.ceil(mY)
                        if pt1X == pt2X or pt1Y == pt2Y:
                            break 
                        In1 = image[pt1Y][pt1X]
                        In2 = image[pt2Y][pt2X]
                        In3 = image[pt1Y][pt2X]
                        In4 = image[pt2Y][pt1X]
                        intensity = inter.bilinear_interpolation(pt1X,pt2X,mX,pt1Y,pt2Y,mY,In1,In3,In2,In4)
                        forw_imag[i][j] = intensity

        return forw_imag


