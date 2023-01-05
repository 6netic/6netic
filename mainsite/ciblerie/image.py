import cv2
import numpy as np
from math import sqrt, pi


class Image:
    """ Main class of image """

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
        """  """

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
        # Computes excentricity
        a1 = (cv2.moments(selected_contour)['mu20'] + cv2.moments(selected_contour)['mu02']) / 2
        a2 = np.sqrt(4 * cv2.moments(selected_contour)['mu11'] ** 2 +
                     (cv2.moments(selected_contour)['mu20'] - cv2.moments(selected_contour)['mu02']) ** 2) / 2
        ecc = np.sqrt(1 - (a1 - a2) / (a1 + a2))
        print("excentricity vaut:", ecc)
        x_centroid = round(cv2.moments(selected_contour)['m10'] / cv2.moments(selected_contour)['m00'])
        y_centroid = round(cv2.moments(selected_contour)['m01'] / cv2.moments(selected_contour)['m00'])
        length = cv2.arcLength(selected_contour, True)
        radius = length / (2 * pi)
        # print("radius vaut:", radius)
        ############### On va de 385 à 394. A - de 380, on annule ###############
        if radius > 369:
            radiusCircle = 369
        elif radius < 365:
            radiusCircle = 365
        else:
            radiusCircle = radius

        # cv2.drawContours(image, [selected_contour], 0, (0, 255, 0), 1)
        resp = {
            'x_center': x_centroid, 'y_center': y_centroid, 'radius': radiusCircle, 'excentricity': ecc
        }
        return resp


    def find_holes(self, image, x_centroid, y_centroid, radiusCircle):
        """ Finds holes in the target """

        holesImg = image.copy()
        hsvImg = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # This is where to set the background color range to be detected
        boundaries = [
            ([0, 0, 0], [179, 255, 54]),
            ([23, 59, 0], [179, 255, 255]),
            ([30, 0, 0], [179, 255, 255])
        ]
        # Loop over the boundaries to find correct background color
        centerHolesList = []
        for (lower, upper) in boundaries:
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
                cv2.drawContours(image, [cnt], 0, (0, 255, 0), 1)

        return image

        #     if len(contours) == 10:
        #         radiusList = []
        #         for cnt in contours:
        #             (x, y), radius = cv2.minEnclosingCircle(cnt)
        #             if radius > 7.0 and radius <= 13.0:
        #                 radiusList.append(radius)
        #             else:
        #                 break
        #         if len(radiusList) == 10:
        #             i = 0
        #
        #             for contour in contours:
        #                 (x, y), radius = cv2.minEnclosingCircle(contour)
        #                 center = (int(x), int(y))
        #                 radius = int(radius)
        #                 cv2.circle(holesImg, center, radius, (0, 255, 0), 1)
        #                 i += 1
        #                 centerHolesList.append(center)
        # # Browsing centerHolesList and creating an array of vectors (centroid to holes)
        # i = 0
        # center2holeCoordsArray = np.zeros((10, 2), dtype=[('x', 'int'), ('y', 'int')])
        # for hole in centerHolesList:
        #     center2holeCoordsArray[i][0] = (x_centroid, y_centroid)
        #     center2holeCoordsArray[i][1] = (hole[0], hole[1])
        #     i += 1
        # # Creating list of distance for each hole found in center2holeCoordsArray
        # i = 0
        # distanceHoles = []
        # for hole in center2holeCoordsArray:
        #     a2 = pow((center2holeCoordsArray[i][1][0] - center2holeCoordsArray[i][0][0]), 2)
        #     b2 = pow((center2holeCoordsArray[i][1][1] - center2holeCoordsArray[i][0][1]), 2)
        #     distanceHoles.append(round(sqrt(a2 + b2)))
        #     i += 1
        # totalPoints = []
        # i = 0
        # for distanceHole in distanceHoles:
        #     if distanceHole >= radiusCircle:
        #         score = 0
        #     elif distanceHole >= 329 and distanceHole < radiusCircle:
        #         score = 1
        #     elif distanceHole >= 291 and distanceHole < 329:
        #         score = 2
        #     elif distanceHole >= 254 and distanceHole < 291:
        #         score = 3
        #     elif distanceHole >= 216 and distanceHole < 254:
        #         score = 4
        #     elif distanceHole >= 179 and distanceHole < 216:
        #         score = 5
        #     elif distanceHole >= 141 and distanceHole < 179:
        #         score = 6
        #     elif distanceHole >= 101 and distanceHole < 141:
        #         score = 7
        #     elif distanceHole >= 63 and distanceHole < 101:
        #         score = 8
        #     elif distanceHole >= 26 and distanceHole < 63:
        #         score = 9
        #     elif distanceHole >= 0 and distanceHole < 26:
        #         score = 10
        #     # Writing points close to respective hole
        #     position = (centerHolesList[i][0] + 10, centerHolesList[i][1] + 10)
        #     cv2.putText(holesImg, str(score), position, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1)
        #     i += 1
        #     totalPoints.append(score)
        # totalPointsSum = sum(totalPoints)
        # cv2.putText(holesImg, str(totalPointsSum) + ' points', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)
        #
        # return holesImg






























