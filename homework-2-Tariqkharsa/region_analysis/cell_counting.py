from enum import unique
import numpy as np
import math
import cv2

class CellCounting:
    def __init__(self):
        pass

    def blob_coloring(self, image):
        """Implement the blob coloring algorithm
        takes a input:
        image: binary image
        return: a list/dict of regions"""
        regions = dict()

        r,c = image.shape
        new_image = np.zeros((r,c))
        def replace(r1,r2):
            for i in range(r):
                for j in range(c):
                    if new_image[i][j] == r1:
                        new_image[i][j] = r2
        k = 1
        for i in range(r):
            for j in range(c):
                if image[i][j] == 255 and j == 0 and i == 0:
                    new_image[i][j] = k 
                    k = k + 1
                elif i == 0:
                    if image[i][j] == 255 and image[i][j-1] == 0:
                        new_image[i][j] = k 
                        k = k + 1
                    if image[i][j] == 255 and image[i][j-1] == 255:
                        new_image[i][j] = new_image[i][j-1]
                elif j == 0:
                    if image[i][j] == 255 and image[i-1][j] == 0:
                        new_image[i][j] = k 
                        k = k + 1
                    if image[i][j] == 255 and image[i-1][j] == 255:
                        new_image[i][j] = new_image[i-1][j]
                else: #no edge cases
                    if image[i][j] == 255 and image[i][j-1] == 0 and image[i-1][j] == 0:
                        new_image[i][j] = k 
                        k = k + 1
                    if image[i][j] == 255 and image[i][j-1] == 0 and image[i-1][j] == 255:
                        new_image[i][j] = new_image[i-1][j]
                    if image[i][j] == 255 and image[i][j-1] == 255 and image[i-1][j] == 0:
                        new_image[i][j] = new_image[i][j-1]
                    if image[i][j] == 255 and image[i][j-1] == 255 and image[i-1][j] == 255:
                        if new_image[i][j-1] != new_image[i-1][j]:
                            replace(new_image[i][j-1], new_image[i-1][j])
                            new_image[i][j] = new_image[i-1][j]
                        else:
                            new_image[i][j] = new_image[i-1][j]
        list1 = []
        for i in range(r):
            for j in range(c):
                if new_image[i][j] > 0:
                    if new_image[i][j] not in list1:
                        regions[new_image[i][j]] = {(j,i)}
                        list1.append(new_image[i][j])
                    else:
                        regions[new_image[i][j]].add((j,i))
        result = dict()
        count = 0
        for x in regions:
            result[count] = regions[x]
            count+=1
        return result

    def compute_statistics(self, region):
        """Compute cell statistics area and location
        takes as input
        region: a list/dict of pixels in a region
        returns: region statistics"""

        # Please print your region statistics to stdout
        # <region number>: <location or center>, <area>
        # print(stats)
        stats = [{"Region":i+1,"Area":len(region[i]),"Centroid": 
        (math.floor(sum([x for x,y in region[i]])/len(region[i])), 
        math.floor(sum([y for x,y in region[i]])/len(region[i])))} 
        for i in range(len(region)) if len(region[i]) >= 15]

        for row in stats:
            print(row)

        return stats


    def mark_image_regions(self, image, stats):
        """Creates a new image with computed stats
        Make a copy of the image on which you can write text. 
        takes as input
        image: a list/dict of pixels in a region
        stats: stats regarding location and area
        returns: image marked with center and area"""
        res_image = image.copy()

        cv2.cvtColor(res_image, cv2.COLOR_GRAY2RGB)
        for row in stats:
             cv2.putText(img = res_image, text = str("*"+str(row["Region"])+", "+str(row["Area"])), fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.3, org=(row["Centroid"]), color=(125))

        return res_image

