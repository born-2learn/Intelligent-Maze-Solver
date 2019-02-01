import numpy as np
import cv2
import bluetooth
import time
import imutils

# Look for all Bluetooth devices
# the computer knows about.
print("Searching for devices...")
print("")

nearby_devices = bluetooth.discover_devices()  # array of devices
# Run through all the devices found and list their name
num = 0
print("List of Devices: ")
for i in nearby_devices:
    num += 1
    print(num, ": ", bluetooth.lookup_name(i))
print("PIXELATION selected.")

port = 1  # port for comm.
bd_addr = "20:15:11:23:88:63"  # MAC Address of PIXELATION


# sock not working without class, self required.
# 1-forward,2-back,3-right,4-left
class application(object):
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)  # creating a socket for BT comm.

    '''def __del__(self):
        print('Deleted')'''  # to delete object(only if required).

    def disconnect(self):
        # Close socket connection to device
        self.sock.close()

    def stop(self):
        data = '0'
        self.sock.send(data)

    def forward(self):  # sending data to bluetooth device
        data = '1'
        self.sock.send(data)

    def right(self):
        data = '2'
        self.sock.send(data)

    def left(self):
        data = '3'
        self.sock.send(data)

    def back(self):
        data = '4'
        self.sock.send(data)

    def __init__(self):
        # Connect to the bluetooth device

        self.sock.connect((bd_addr, port))


o1 = application()  # creation of object o1

# define the lower and upper boundaries of the colors in the HSV color space
lower = {'red': (166, 84, 141), 'green': (66, 122, 129), 'blue': (97, 100, 117), 'yellow': (23, 59, 119),
         'orange': (0, 50, 80)}  # assign new item lower['blue'] = (93, 10, 0)
upper = {'red': (186, 255, 255), 'green': (86, 255, 255), 'blue': (117, 255, 255), 'yellow': (54, 255, 255),
         'orange': (20, 255, 255)}

# define standard colors for circle around the object
colors = {'red': (0, 0, 255), 'green': (0, 255, 0), 'blue': (255, 0, 0), 'yellow': (0, 255, 217),
          'orange': (0, 140, 255)}

camera = cv2.VideoCapture(0)  # capturing livestream

points = [[390, 320], [390, 275], [274, 275], [273, 77], [273, 35], [379, 35], [379, 164], [462, 164]]

ran = 25  # pixel distance on each side of correct path
timef = 0.005  # time delay after each statement(eg.after forward)..usually not required.
timecorrectfactor = 20  # similar to value of range
turn=3

def centre():  # returns centre coordinates of yellow and blue patch.


        # grab the current frame


        (grabbed, frame) = camera.read()

        #frame = imutils.resize(frame, width=480, height=360)
        x1, x2 = 40, 520
        y1, y2 = 5, 520
        frame = frame[y1:y2, x1:x2]

        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        # for each color in dictionary check object in frame
        yc, bc = [0, 0], [0, 0]  # initializing centres of blue and yellow patch
        for key, value in upper.items():
            # construct a mask for the color from dictionary`1, then perform
            # a series of dilations and erosions to remove any small
            # blobs left in the mask
            kernel = np.ones((9, 9), np.uint8)
            mask = cv2.inRange(hsv, lower[key], upper[key])
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            # find contours in the mask and initialize the current
            # (x, y) center of the ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None

            # only proceed if at least one contour was found
            if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid

                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                # print(box)
                xdash, ydash = 400, 300

                # only proceed if the radius meets a minimum size. Correct this value for your obect's size
                if radius > 0.5:
                    # drawing a rectangle around the blue and yellow patch

                    cv2.drawContours(frame, [box], 0, colors[key], 2)

                    cv2.putText(frame, key + " rectangle", (int(x - radius), int(y - radius)), cv2.FONT_HERSHEY_SIMPLEX,
                                0.6,
                                colors[key], 2)
                    if key == 'blue':
                        xdash = (box[1][0] + box[2][0]) / 2
                        ydash = (box[0][1] + box[1][1]) / 2
                        bc = [int(xdash), int(ydash)]
                        #print(bc)

                    if key == 'orange':
                        xdash = (box[1][0] + box[2][0]) / 2
                        ydash = (box[0][1] + box[1][1]) / 2
                        yc = [int(xdash), int(ydash)]
        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1) & 0xFF
        # if the 'q' key is pressed, stop the loop

        return bc, yc

junction_deviation=5
initial_state='q'
for i in range(len(points) - 1):  # traversing the vertices array
    [x1, y1] = points[i]  # storing points
    [x2, y2] = points[i + 1]

    x, y = centre()
    [xb, yb] = x
    [xy, yy] = y

    if abs(x1-x2)<=junction_deviation and (y1 - y2) > 0:
        print("going north")
        print(initial_state)
        x, y = centre()
        print(x,y,'centres of blue and yellow')
        [xb, yb] = x
        [xy, yy] = y
        #while abs(x1 - xb) > 2*ran or abs(x1 - xy) > 2*ran:  # same construct(Ref1)
        if initial_state=='w':
            while abs(xy - xb) > turn:
                x, y = centre()
                [xb, yb] = x
                [xy, yy] = y
                o1.right()
                print('going right')
            else:
                while abs(y2 - ((yy + yb) / 2)) > timecorrectfactor:
                    print(((yy + yb) / 2))
                    print('moving up')
                    x, y = centre()
                    [xb, yb] = x
                    [xy, yy] = y
                    if xb < x1 and abs(xb - x1) > ran:
                        o1.left()
                        time.sleep(timef)
                        print('bl c')
                    elif xb > x1 and abs(xb - x1) > ran:
                        o1.right()
                        time.sleep(timef)
                        print('brc')
                    else:
                        o1.forward()
                    if yb > x1 and abs(xy - x1) > ran:
                        o1.left()
                        time.sleep(timef)
                        print('ylc')
                    elif yb < x1 and abs(xy - x1) > ran:
                        o1.right()
                        time.sleep(timef)
                        print('yrc')
                    else:
                        o1.forward()
        elif initial_state=='e':
            while abs(xy - xb) > turn:
                x, y = centre()
                [xb, yb] = x
                [xy, yy] = y
                o1.left()
            else:
                while abs(y2 - ((yy + yb) / 2)) > timecorrectfactor:
                    print(((yy + yb) / 2))
                    print('moving up')
                    x, y = centre()
                    [xb, yb] = x
                    [xy, yy] = y
                    if xb < x1 and abs(xb - x1) > ran:
                        o1.left()
                        time.sleep(timef)
                        print('bl c')
                    elif xb > x1 and abs(xb - x1) > ran:
                        o1.right()
                        time.sleep(timef)
                        print('brc')
                    else:
                        o1.forward()
                    if yb > x1 and abs(xy - x1) > ran:
                        o1.left()
                        time.sleep(timef)
                        print('ylc')
                    elif yb < x1 and abs(xy - x1) > ran:
                        o1.right()
                        time.sleep(timef)
                        print('yrc')
                    else:
                        o1.forward()
        else:
            while abs(y2 - ((yy + yb) / 2)) > timecorrectfactor:
                print(((yy + yb) / 2))
                print('moving up')
                x, y = centre()
                [xb, yb] = x
                [xy, yy] = y
                if xb < x1 and abs(xb - x1) > ran:
                    o1.left()
                    time.sleep(timef)
                    print('bl c')
                elif xb > x1 and abs(xb - x1) > ran:
                    o1.right()
                    time.sleep(timef)
                    print('brc')
                else:
                    o1.forward()
                if yb > x1 and abs(xy - x1) > ran:
                    o1.left()
                    time.sleep(timef)
                    print('ylc')
                elif yb < x1 and abs(xy - x1) > ran:
                    o1.right()
                    time.sleep(timef)
                    print('yrc')
                else:
                    o1.forward()

        initial_state = 'n'
        o1.stop()

    # case for going back yet to be written.
    elif abs(y1-y2)<junction_deviation and x1 - x2 > 0:
        print("going west")
        print(initial_state)
        if initial_state=='n':

         while abs(yy - yb) > turn:
            x, y = centre()
            [xb, yb] = x
            [xy, yy] = y
            o1.left()
            print('going left west ini n')
         else:  # add Ref1 here(experimental)
            while abs(x2 - ((xy+xb) / 2)) > timecorrectfactor:
                print(((xy + xb) / 2))
                print('moving straight')
                x, y = centre()
                [xb, yb] = x
                [xy, yy] = y
                if yb < y1 and abs(yb - y1) > ran:
                    o1.right()
                    time.sleep(timef)
                    print('bl c')
                elif yb > y1 and abs(yb - y1) > ran:
                    o1.left()
                    time.sleep(timef)
                    print('brc')
                else:
                    o1.forward()
                if yy > x1 and abs(yy - y1) > ran:
                    o1.right()
                    time.sleep(timef)
                    print('ylc')
                elif yb < y1 and abs(yy - y1) > ran:
                    o1.left()
                    time.sleep(timef)
                    print('yrc')
                else:
                    o1.forward()
            initial_state='w'
            o1.stop()
        elif initial_state=='s':
            while abs(yy - yb) > turn:
                x, y = centre()
                [xb, yb] = x
                [xy, yy] = y
                o1.right()
            else:  # add Ref1 here(experimental)
                while abs(x2 - ((xy + xb) / 2)) > timecorrectfactor:
                    print(((xy + xb) / 2))
                    print('moving straight')
                    x, y = centre()
                    [xb, yb] = x
                    [xy, yy] = y
                    if yb < y1 and abs(yb - y1) > ran:
                        o1.right()
                        time.sleep(timef)
                        print('bl c')
                    elif yb > y1 and abs(yb - y1) > ran:
                        o1.left()
                        time.sleep(timef)
                        print('brc')
                    else:
                        o1.forward()
                    if yy > x1 and abs(yy - y1) > ran:
                        o1.right()
                        time.sleep(timef)
                        print('ylc')
                    elif yb < y1 and abs(yy - y1) > ran:
                        o1.left()
                        time.sleep(timef)
                        print('yrc')
                    else:
                        o1.forward()
                initial_state = 'w'
                o1.stop()
        else:
                print('else of w')

                # add Ref1 here(experimental)
                while abs(x2 - ((xy + xb) / 2)) > timecorrectfactor:
                    print(((xy + xb) / 2))
                    print('moving straight')
                    x, y = centre()
                    [xb, yb] = x
                    [xy, yy] = y
                    if yb < y1 and abs(yb - y1) > ran:
                        o1.right()
                        time.sleep(timef)
                        print('bl c')
                    elif yb > y1 and abs(yb - y1) > ran:
                        o1.left()
                        time.sleep(timef)
                        print('brc')
                    else:
                        o1.forward()
                    if yy > x1 and abs(yy - y1) > ran:
                        o1.right()
                        time.sleep(timef)
                        print('ylc')
                    elif yb < y1 and abs(yy - y1) > ran:
                        o1.left()
                        time.sleep(timef)
                        print('yrc')
                    else:
                        o1.forward()
                initial_state = 'w'
                o1.stop()

    elif abs(y1-y2)<=junction_deviation and x2 - x1 > timecorrectfactor:
        print("going east")
        print(initial_state)
        if initial_state=='n':
         while abs(yy - yb) > turn:

            x, y = centre()
            [xb, yb] = x
            [xy, yy] = y
            print(x,y)
            print('taking right')
            o1.right()
            time.sleep(timef)
         else:  # add Ref1 here(experimental)
            print('east loop')
            while abs(x2 - ((xy+xb) / 2)) > timecorrectfactor:
                print(((xy + xb) / 2))
                print('moving straight')
                x, y = centre()
                [xb, yb] = x
                [xy, yy] = y
                if yb < y1 and abs(yb - y1) > ran:
                    o1.left()
                    time.sleep(timef)
                    print('bl c')
                elif yb > y1 and abs(yb - y1) > ran:
                    o1.right()
                    time.sleep(timef)
                    print('brc')
                else:
                    o1.forward()
                if yy > x1 and abs(yy - y1) > ran:
                    o1.left()
                    time.sleep(timef)
                    print('ylc')
                elif yb < y1 and abs(yy - y1) > ran:
                    o1.right()
                    time.sleep(timef)
                    print('yrc')
                else:
                    o1.forward()
            o1.stop()
            initial_state='e'
        elif initial_state=='s':
            while abs(yy - yb) > turn:

                x, y = centre()
                [xb, yb] = x
                [xy, yy] = y
                print(x, y)
                print('taking left')
                o1.left()
                time.sleep(timef)
            else:  # add Ref1 here(experimental)
                print('east loop')
                while abs(x2 - ((xy + xb) / 2)) > timecorrectfactor:
                    print(((xy + xb) / 2))
                    print('moving straight')
                    x, y = centre()
                    [xb, yb] = x
                    [xy, yy] = y
                    if yb < y1 and abs(yb - y1) > ran:
                        o1.left()
                        time.sleep(timef)
                        print('bl c')
                    elif yb > y1 and abs(yb - y1) > ran:
                        o1.right()
                        time.sleep(timef)
                        print('brc')
                    else:
                        o1.forward()
                    if yy > x1 and abs(yy - y1) > ran:
                        o1.left()
                        time.sleep(timef)
                        print('ylc')
                    elif yb < y1 and abs(yy - y1) > ran:
                        o1.right()
                        time.sleep(timef)
                        print('yrc')
                    else:
                        o1.forward()
        else:


                print('east loop')
                while abs(x2 - ((xy + xb) / 2)) > timecorrectfactor:
                    print(((xy + xb) / 2))
                    print('moving straight')
                    x, y = centre()
                    [xb, yb] = x
                    [xy, yy] = y
                    if yb < y1 and abs(yb - y1) > ran:
                        o1.left()
                        time.sleep(timef)
                        print('bl c')
                    elif yb > y1 and abs(yb - y1) > ran:
                        o1.right()
                        time.sleep(timef)
                        print('brc')
                    else:
                        o1.forward()
                    if yy > x1 and abs(yy - y1) > ran:
                        o1.left()
                        time.sleep(timef)
                        print('ylc')
                    elif yb < y1 and abs(yy - y1) > ran:
                        o1.right()
                        time.sleep(timef)
                        print('yrc')
                    else:
                        o1.forward()
                initial_state='e'
                o1.stop()

    elif abs(x1-x2)<=junction_deviation and (y2 - y1) > 0:
        print("going south")
        print(initial_state)
        x, y = centre()
        print(x,y,'centres of blue and yellow')
        [xb, yb] = x
        [xy, yy] = y
        if initial_state=='e':
            while abs(yy - yb) > turn:

                x, y = centre()
                [xb, yb] = x
                [xy, yy] = y
                print(x, y)
                print('taking right')
                o1.right()
                time.sleep(timef)
            else:  # add Ref1 here(experimental)
                print('south loop')
                while abs(y2 - ((yy + yb) / 2)) > timecorrectfactor:
                    print(((yy + yb) / 2))
                    print('moving down')
                    x, y = centre()
                    [xb, yb] = x
                    [xy, yy] = y
                    if xb < x1 and abs(xb - x1) > ran:
                        o1.right()
                        time.sleep(timef)
                        print('bl c')
                    elif xb > x1 and abs(xb - x1) > ran:
                        o1.left()
                        time.sleep(timef)
                        print('brc')
                    else:
                        o1.forward()
                    if yb > x1 and abs(xy - x1) > ran:
                        o1.right()
                        time.sleep(timef)
                        print('ylc')
                    elif yb < x1 and abs(xy - x1) > ran:
                        o1.left()
                        time.sleep(timef)
                        print('yrc')
                    else:
                        o1.forward()

        if initial_state == 'w':
                while abs(yy - yb) > turn:

                    x, y = centre()
                    [xb, yb] = x
                    [xy, yy] = y
                    print(x, y)
                    print('taking left')
                    o1.left()
                    time.sleep(timef)
                else:  # add Ref1 here(experimental)
                    print('south loop')
                    while abs(y2 - ((yy + yb) / 2)) > timecorrectfactor:
                        print(((yy + yb) / 2))
                        print('moving down')
                        x, y = centre()
                        [xb, yb] = x
                        [xy, yy] = y
                        if xb < x1 and abs(xb - x1) > ran:
                            o1.right()
                            time.sleep(timef)
                            print('bl c')
                        elif xb > x1 and abs(xb - x1) > ran:
                            o1.left()
                            time.sleep(timef)
                            print('brc')
                        else:
                            o1.forward()
                        if yb > x1 and abs(xy - x1) > ran:
                            o1.right()
                            time.sleep(timef)
                            print('ylc')
                        elif yb < x1 and abs(xy - x1) > ran:
                            o1.left()
                            time.sleep(timef)
                            print('yrc')
                        else:
                            o1.forward()
        else:
            print('south loop')
            while abs(y2 - ((yy + yb) / 2)) > timecorrectfactor:
                print(((yy + yb) / 2))
                print('moving down')
                x, y = centre()
                [xb, yb] = x
                [xy, yy] = y
                if xb < x1 and abs(xb - x1) > ran:
                    o1.right()
                    time.sleep(timef)
                    print('bl c')
                elif xb > x1 and abs(xb - x1) > ran:
                    o1.left()
                    time.sleep(timef)
                    print('brc')
                else:
                    o1.forward()
                if yb > x1 and abs(xy - x1) > ran:
                    o1.right()
                    time.sleep(timef)
                    print('ylc')
                elif yb < x1 and abs(xy - x1) > ran:
                    o1.left()
                    time.sleep(timef)
                    print('yrc')
                else:
                    o1.forward()
        initial_state='s'
        o1.stop()




            # while abs(x1 - xb) > 2*ran or abs(x1 - xy) > 2*ran:  # same construct(Ref1)

    else:
        o1.stop()#experimental



camera.release()
cv2.destroyAllWindows()

