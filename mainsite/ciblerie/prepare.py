from os import path, mkdir, listdir, remove
import numpy as np
import cv2


class Prepare:
    """ Preparation before processing with OpenCV """

    def __init__(self):

        self.base_path = path.dirname(path.abspath(__file__))
        self.media_dir = path.join(self.base_path, "media")
        self.in_dir = path.join(self.media_dir, "in")
        # out on static/ciblerie/out
        self.static = path.join(self.base_path, "static")
        self.stat_cib = path.join(self.static, "ciblerie")
        self.out_dir = path.join(self.stat_cib, "out")


    def create_folders(self):
        """ Creates empty directories or delete all files within in/ and out/ """

        try:
            mkdir(self.media_dir)
            mkdir(self.in_dir)
            # mkdir(self.out_dir)

        except FileExistsError:
            for directory in [self.in_dir, self.out_dir]:
                for file in listdir(directory):
                    file = path.join(directory, file)
                    remove(file)
        return self.in_dir, self.out_dir


    def check_picture(self, picture):
        """ Checks extension and size of the file """

        if (picture.name.rsplit('.', 1)[1].lower()) not in ['jpg', 'jpeg', 'png']:
            return "bad_extension"
        elif picture.size > 5000000:
            return "too_big"


    def save_to_disk(self, picture):
        """ Save picture to hard disk """

        with open(path.join(self.in_dir, picture.name), 'wb+') as file:
            for chunk in picture.chunks():
                file.write(chunk)
        return file.name


    def open_picture(self, img):
        """ Opens the file to work with """

        image = open(img, "rb").read()
        image = np.asarray(bytearray(image), dtype=np.uint8)
        img_opencv = cv2.imdecode(image, -1)
        return img_opencv


    def save_after_treatment(self, image):
        """ Saves the file after opencv treatment """

        final_picture = path.join(self.out_dir, 'temp.jpg')
        cv2.imwrite(final_picture, image)
        mainsite_dir = path.dirname(path.dirname(path.abspath(__file__)))
        mainsite_static_dir = path.join(mainsite_dir, "static")
        mainsite_static_cib_dir = path.join(mainsite_static_dir, "ciblerie")
        mainsite_static_cib_out_dir = path.join(mainsite_static_cib_dir, "out")
        static_picture = path.join(mainsite_static_cib_out_dir, 'temp.jpg')
        cv2.imwrite(static_picture, image)

























