""" Deskews file after getting skew angle """
import optparse
import numpy as np
import matplotlib.pyplot as plt

from skew_detect import SkewDetect
from skimage import io,color
from skimage.transform import rotate


class Deskew:

    def __init__(self,input_img, input_file, output_file, display_image=None, r_angle=0):

        self.input_img=input_img
        self.input_file = input_file
        self.display_image = display_image
        self.output_file = output_file
        self.r_angle = r_angle
        self.skew_obj = SkewDetect(color.rgb2gray(input_img),self.input_file)
        print("Rotating")
    def deskew(self):

#        img = io.imread(self.input_file)
        img=self.input_img
        res = self.skew_obj.process_single_file()
        angle = res['Estimated Angle']

        if angle >= 0 and angle <= 90:
            rot_angle = angle - 90 + self.r_angle
        if angle >= -45 and angle < 0:
            rot_angle = angle - 90 + self.r_angle
        if angle >= -90 and angle < -45:
            rot_angle = 90 + angle + self.r_angle

        rotated = rotate(img, rot_angle, resize=True)

        if self.display_image:
            self.display(rotated)

        if self.output_file:
#            a=self.saveImage(rotated*255)
            a=rotated*255
            return a.astype(np.uint8)

    def saveImage(self, img):
        
        path = self.skew_obj.check_path(self.output_file)
        io.imsave(path, img.astype(np.uint8))
        a=img.astype(np.uint8)
        return a
    
    def display(self, img):

        plt.imshow(img)
        plt.show()

    def run(self):

        if self.input_file:
            a=self.deskew()
            return a


if __name__ == '__main__':
    img=io.imread("passport4.JPG")
    deskew_obj = Deskew(img,"a","b", r_angle=180)
    res=deskew_obj.run()
    io.imsave("cur.jpg", res)
