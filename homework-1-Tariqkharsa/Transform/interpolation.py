class interpolation:

    def linear_interpolation(self, Pt1, Pt2, Pt3, IP1, IP2):
        """Computes the linear interpolation value at some iD location x between two 1D points (Pt1 and Pt2).
        
        There are no arguments defined in the function definition on purpose. It is left upto the student to define any requierd arguments.
        Please change the signature of the function and add the arguments based on your implementation.
        
        The function ideally takes two 1D points Pt1 and Pt2, and their intensitites I(Pt1), I(Pt2).
        return the interpolated intensity value (I(x)) at location x """

        # Write your code for linear interpolation here
        Intensity = (IP1)*((Pt2-Pt3)/(Pt2-Pt1)) + (IP2)*((Pt3-Pt1)/(Pt2-Pt1))
        return Intensity

    def bilinear_interpolation(self, x1, x2, x3, y1, y2, y3, IP1, IP2, IP3, IP4):

        """Computes the bi linear interpolation value at some 2D location x between four 2D points (Pt1, Pt2, Pt3, and Pt4).
        
        There are no arguments defined in the function definition on purpose. It is left upto the student to define any requierd arguments.
        Please change the signature of the function and add the arguments based on your implementation.
        
        The function ideally takes four 2D points Pt1, Pt2, Pt3, and Pt4, and their intensitites I(Pt1), I(Pt2), I(Pt3), and I(Pt4).
        return the interpolated intensity value (I(x)) at location x """

        # Write your code for bilinear interpolation here
        # Recall that bilinear interpolation performs linear interpolation three times
        # Please reuse or call linear interpolation method three times by passing the appropriate parameters to compute this task
        
        """Notes"""
        # I passed in x1,x2,y1,y2 instead of passing 4 points as it is much more efficient that way
        inter = interpolation()

        inten1 = inter.linear_interpolation(x1,x2,x3,IP1,IP2)
        inten2 = inter.linear_interpolation(x1,x2,x3,IP3,IP4)
        intensity = inter.linear_interpolation(y1,y2,y3,inten1,inten2)
        
        return intensity

