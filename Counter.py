import numpy as np
import cv2

cap = cv2.VideoCapture(0)

frames_count, fps, width, height = cap.get(cv2.CAP_PROP_FRAME_COUNT), cap.get(cv2.CAP_PROP_FPS), cap.get(
    cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = int(width)
height = int(height)
print(frames_count, fps, width, height)

count = 0

fgbg = cv2.createBackgroundSubtractorMOG2()

ret, frame = cap.read()
ratio = 1
image = frame

while True:
    countcontrol = True
    ret, frame = cap.read()

    if ret:

        image = cv2.resize(frame, (0, 0), None, ratio, ratio)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        fgmask = fgbg.apply(gray)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        closing = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
        opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
        dilation = cv2.dilate(opening, kernel)
        retvalbin, bins = cv2.threshold(dilation, 220, 255, cv2.THRESH_BINARY)

        im2, contours, hierarchy = cv2.findContours(bins, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        hull = [cv2.convexHull(c) for c in contours]

        # cv2.drawContours(image, hull, -1, (0, 255, 0), 3)

        lineypos = 150
        # cv2.line(image, (0, lineypos), (width, lineypos), (255, 255, 255), 2)

        lineypos2 = 200
        cv2.line(image, (0, lineypos2), (width, lineypos2), (255, 255, 255), 2)

        minarea = 300

        maxarea = 50000

        cxx = np.zeros(len(contours))
        cyy = np.zeros(len(contours))

        for i in range(len(contours)):

            if hierarchy[0, i, 3] == -1:

                area = cv2.contourArea(contours[i])

                if minarea < area < maxarea:

                    cnt = contours[i]
                    M = cv2.moments(cnt)
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])

                    # if cy < lineypos:

                    x, y, w, h = cv2.boundingRect(cnt)

                    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    cv2.putText(image, str(cx) + "," + str(cy), (cx + 10, cy + 10), cv2.FONT_HERSHEY_SIMPLEX,
                                .3, (0, 0, 255), 1)

                    # cv2.drawMarker(image, (cx, cy), (0, 0, 255), cv2.MARKER_STAR, markerSize=5, thickness=1,
                    #                line_type=cv2.LINE_AA)



                    countcontrol = True
                    if cy in range(lineypos, lineypos2):

                        for j in range(0, cxx.__len__()):
                            if abs(cx - cxx[j]) <= w and abs(cy - cyy[j]) <= h:
                                countcontrol = False


                        if countcontrol:
                            count += 1
                            cxx[i] = cx
                            cyy[i] = cy



        cxx = cxx[cxx != 0]
        cyy = cyy[cyy != 0]

        cv2.putText(image, "Count: " + str(count), (5, 25), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 2)


        cv2.imshow("Frame", image)
        cv2.moveWindow("Frame", 0, 0)

        # cv2.imshow("fgmask", fgmask)
        # cv2.moveWindow("fgmask", int(width * ratio), 0)
        #
        # cv2.imshow("closing", closing)
        # cv2.moveWindow("closing", width, 0)
        #
        # cv2.imshow("opening", opening)
        # cv2.moveWindow("opening", 0, int(height * ratio))
        #
        # cv2.imshow("dilation", dilation)
        # cv2.moveWindow("dilation", int(width * ratio), int(height * ratio))
        #
        # cv2.imshow("binary", bins)
        # cv2.moveWindow("binary", width, int(height * ratio))
        #


        k = cv2.waitKey(5) & 0xff
        if k == 27:
            break

    else:

        break

cap.release()
cv2.destroyAllWindows()