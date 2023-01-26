import cv2
import numpy as np
from math import sqrt, pi


class Image:
    """ Main class of image """

    def __init__(self):
        """ Background color to be detected is dark blue
            others color to be added to detect all holes ...
        """
        self.boundaries = [([33, 0, 0], [179, 255, 255])]

    def find_contours(self, image, min_val, max_val):
        """ Converts original image to binary eroded image """

        M = np.ones(image.shape, dtype="uint8") * 6
        added_image = cv2.add(image, M)
        gray_img = cv2.cvtColor(added_image, cv2.COLOR_BGR2GRAY)
        blur_img = cv2.medianBlur(gray_img, 7)
        _, thresh = cv2.threshold(blur_img, min_val, max_val, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours


    def extract_new_picture(self, image, min_val, max_val):
        """ Gets the target contour and extracts it """

        contours = self.find_contours(image, min_val, max_val)
        contours_list = []
        for cnt in contours:
            contours_list.append(cv2.contourArea(cnt))
        max_selected_contour_index = contours_list.index(max(contours_list))
        selected_contour = contours[max_selected_contour_index]
        perimeter = cv2.arcLength(selected_contour, True)
        approx = cv2.approxPolyDP(selected_contour, 0.05 * perimeter, True)
        if len(approx) == 4:
            # Rearrange the 4 coordinates
            newCoords = np.zeros_like(approx)
            coords = approx.reshape((4, 2))
            addition = coords.sum(1)
            newCoords[0] = coords[np.argmin(addition)]
            newCoords[3] = coords[np.argmax(addition)]
            difference = np.diff(coords, axis=1)
            newCoords[1] = coords[np.argmin(difference)]
            newCoords[2] = coords[np.argmax(difference)]
            # Generate new target image
            width, height = 799, 799
            coords1 = np.float32(newCoords)
            coords2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
            matrix = cv2.getPerspectiveTransform(coords1, coords2)
            extractImg = cv2.warpPerspective(image, matrix, (width, height))
            return extractImg


    def find_biggest_circle_radius(self, image, blur_k, cThr, kernel):
        """ Gets infos on the biggest circle """

        grayImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurImg = cv2.GaussianBlur(grayImg, blur_k, 0)
        cannyImg = cv2.Canny(blurImg, cThr[0], cThr[1])
        dilateImg = cv2.dilate(cannyImg, kernel, iterations=1)
        erodeImg = cv2.erode(dilateImg, kernel, iterations=1)
        contours, hierarchy = cv2.findContours(erodeImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours_list = []
        for cnt in contours:
            contours_list.append(cv2.contourArea(cnt))
        max_selected_contour_index = contours_list.index(max(contours_list))
        selected_contour = contours[max_selected_contour_index]
        # Computes eccentricity
        a1 = (cv2.moments(selected_contour)['mu20'] + cv2.moments(selected_contour)['mu02']) / 2
        a2 = np.sqrt(4 * cv2.moments(selected_contour)['mu11'] ** 2 +
                     (cv2.moments(selected_contour)['mu20'] - cv2.moments(selected_contour)['mu02']) ** 2) / 2
        ecc = np.sqrt(1 - (a1 - a2) / (a1 + a2))
        x_centroid = round(cv2.moments(selected_contour)['m10'] / cv2.moments(selected_contour)['m00'])
        y_centroid = round(cv2.moments(selected_contour)['m01'] / cv2.moments(selected_contour)['m00'])
        length = cv2.arcLength(selected_contour, True)
        radius = length / (2 * pi)
        if radius > 369:
            radiusCircle = 369
        elif radius < 365:
            radiusCircle = 365
        else:
            radiusCircle = radius
        resp = {
            'x_center': x_centroid, 'y_center': y_centroid, 'radius': radiusCircle, 'excentricity': ecc
        }
        return resp


    def find_holes(self, image):
        """ Finds holes in the target """

        holes_in_img = image.copy()
        hsvImg = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        centerHolesList = []
        for (lower, upper) in self.boundaries:
            # Create numpy arrays from the boundaries
            lower = np.array(lower, dtype="uint8")
            upper = np.array(upper, dtype="uint8")
            # Find the colors within the specified boundaries and apply the mask
            mask = cv2.inRange(hsvImg, lower, upper)
            # Adding a black border to the image
            mask[0:20, 0:799] = 0
            mask[0:799, 0:20] = 0
            mask[0:799, 779:799] = 0
            mask[779:799, 0:799] = 0
            mask = cv2.medianBlur(mask, 7)
            # Detecting the 10 holes in the target
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                # Ne retenir que ce qui ressemble à un cercle
                length = cv2.arcLength(cnt, True)
                a = cv2.moments(cnt)['m00']
                if a > 0:
                    # k stands for Roundness
                    k = (length * length) / ((cv2.moments(cnt)['m00']) * 4 * np.pi)
                    if k < 1.32:
                        (x, y), radius = cv2.minEnclosingCircle(cnt)
                        if radius > 7.0:
                            cv2.drawContours(holes_in_img, [cnt], 0, (0, 255, 0), 1)
                            one_circle_coord = (round(x), round(y))
                            centerHolesList.append(one_circle_coord)
        return holes_in_img, centerHolesList


    def get_score(self, image, points_coord, x_center, y_center, radius):
        """ Counts points """

        print("raduis vaut:", radius)
        i = 0
        m = len(points_coord)
        center_to_hole_coords_array = np.zeros((m, 2), dtype=[('x', 'int'), ('y', 'int')])
        for hole in points_coord:
            center_to_hole_coords_array[i][0] = (x_center, y_center)
            center_to_hole_coords_array[i][1] = (hole[0], hole[1])
            i += 1
        # Creating list of distance for each hole found in center_to_hole_coords_array
        i = 0
        dist_center_hole = []
        for hole in center_to_hole_coords_array:
            a2 = pow((center_to_hole_coords_array[i][1][0] - center_to_hole_coords_array[i][0][0]), 2)
            b2 = pow((center_to_hole_coords_array[i][1][1] - center_to_hole_coords_array[i][0][1]), 2)
            dist_center_hole.append(round(sqrt(a2 + b2)))
            i += 1
        total_points = []
        i = 0
        new_score = 0
        for distance in dist_center_hole:
            if distance >= radius:
                score = 0
            elif distance >= 329 and distance < radius:
                score = 1
            elif distance >= 291 and distance < 329:
                score = 2
            elif distance >= 254 and distance < 291:
                score = 3
            elif distance >= 216 and distance < 254:
                score = 4
            elif distance >= 179 and distance < 216:
                score = 5
            elif distance >= 141 and distance < 179:
                score = 6
            elif distance >= 101 and distance < 141:
                score = 7
            elif distance >= 63 and distance < 101:
                score = 8
            elif distance >= 26 and distance < 63:
                score = 9
            elif distance >= 0 and distance < 26:
                score = 10
            # Writing points close to respective hole
            text_points_pos = (points_coord[i][0] + 10, points_coord[i][1] + 10)
            cv2.putText(image, str(score), text_points_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1)
            i += 1
            new_score += score
        print("Le score est:", new_score)
        cv2.putText(
            image, str(new_score) + ' pts (' + str(m) + ' impacts)',
            (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2
        )
        return image