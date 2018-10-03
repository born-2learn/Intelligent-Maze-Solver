
import numpy as np
import cv2
import bluetooth
import time



# Look for all Bluetooth devices
# the computer knows about.
print("Searching for devices...")
print("")

nearby_devices = bluetooth.discover_devices()#array of devices
# Run through all the devices found and list their name
num = 0
print("List of Devices: ")
for i in nearby_devices:
    num += 1
    print(num, ": ", bluetooth.lookup_name(i))
print("PIXELATION selected.")

port = 1#port for comm.
bd_addr="20:15:11:23:88:63"#MAC Address of PIXELATION


#sock not working without class, self required.
#1-forward,2-back,3-right,4-left
class application(object):

    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)#creating a socket for BT comm.

    '''def __del__(self):
        print('Deleted')'''#to delete object(only if required).

    def disconnect(self):
        # Close socket connection to device
        self.sock.close()
    def stop(self):
        data='0'
        self.sock.send(data)

    def forward(self):#sending data to bluetooth device
        data='1'
        self.sock.send(data)

    def right(self):
        data='2'
        self.sock.send(data)
    def left(self):
        data='3'
        self.sock.send(data)
    def back(self):
        data='4'
        self.sock.send(data)



    def __init__(self):
        # Connect to the bluetooth device

        self.sock.connect((bd_addr, port))



o1=application()# creation of object o1



# define the lower and upper boundaries of the colors in the HSV color space
lower = {'red': (166, 84, 141), 'green': (66, 122, 129), 'blue': (97, 100, 117), 'yellow': (23, 59, 119),
         'orange': (0, 50, 80)}  # assign new item lower['blue'] = (93, 10, 0)
upper = {'red': (186, 255, 255), 'green': (86, 255, 255), 'blue': (117, 255, 255), 'yellow': (54, 255, 255),
         'orange': (20, 255, 255)}

# define standard colors for circle around the object
colors = {'red': (0, 0, 255), 'green': (0, 255, 0), 'blue': (255, 0, 0), 'yellow': (0, 255, 217),
          'orange': (0, 140, 255)}

camera = cv2.VideoCapture(1)#capturing livestream


points=[[353, 230], [353, 105], [210, 105]]# vertices of the path (obtained via BFS) from another module

dir='q'#storing a non-direction value to direction variable
turn_state='noturn'# to store R/L turms
ran = 30# range, correction factor for timedelay in bluetooth connectivity.
timef = 0.005#time delay after each statement(eg.after forward)
timecorrectfactor = 30  # similar to value of range
for i in range(len(points)-1):# traversing the vertices array
    [x1, y1] = points[i ]# storing points
    [x2, y2] = points[i+1]



    #while loop starts to obtain center of yellow patch and center of blue patch and move the bot completely on 1 path
    while True:
        # grab the current frame
        def rescale(img, p=50):#rescaling for reducing load on processor
            width = int(img.shape[1] * p / 100)
            height = int(img.shape[0] * p / 100)
            dim = (width, height)
            return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        (grabbed, frame) = camera.read()

        frame = rescale(frame,p=25)

        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        # for each color in dictionary check object in frame
        yc, bc = [0, 0], [0, 0]#initializing centres of blue and yellow patch
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
                #print(box)
                xdash, ydash = 400, 300

                # only proceed if the radius meets a minimum size. Correct this value for your obect's size
                if radius > 0.5:
                    #drawing a rectangle around the blue and yellow patch

                    cv2.drawContours(frame, [box], 0, colors[key], 2)


                    cv2.putText(frame, key + " rectangle", (int(x - radius), int(y - radius)), cv2.FONT_HERSHEY_SIMPLEX,
                                0.6,
                                colors[key], 2)
                    if key == 'blue':
                        xdash = (box[1][0] + box[2][0]) / 2
                        ydash = (box[0][1] + box[1][1]) / 2
                        bc = [int(xdash), int(ydash)]
                        print(bc)


                    if key == 'yellow':
                        xdash = (box[1][0] + box[2][0]) / 2
                        ydash = (box[0][1] + box[1][1]) / 2
                        yc = [int(xdash), int(ydash)]

        #working case of only forward motion(north) and right(east) motion worked on
        if x1 == x2:


            if y1 - y2 > 0:
                if bc[1] <= (y2 + timecorrectfactor):
                    print('Path complete in going N')
                    break
                print("forward")

                dir = 'n'
                print('selected north x1=x2')
            else:

                print("backward")
                dir = 's'
        if y1 == y2:
            if x1 - x2 > 0:
                if bc[0] <= (x2 + timecorrectfactor):
                    print('Path complete in going W')
                    break
                print("left")

                dir = 'w'
            else:
                print("right")

                dir = 'e'

        if dir == 'n':
                if bc[1] > (y2 + timecorrectfactor):
                    print('entering north loop')
                    print('bc[1],y2', bc[1], y2)
                    o1.forward()
                    print('going north')
                    # time.sleep(timef)

                    '''if (bc[0] > (x1 + ran) or bc[0] < (x1 - ran)) or ((yc[0] > (x1 + ran) or yc[0] < (x1 - ran))):

                                if bc[0] > (x1 + ran):
                                    o1.right()
                                    print('Adjusting right blue')
                                    time.sleep(timef)

                                if bc[0] < (x1 - ran):
                                    o1.left()
                                    print('Adjusting left blue')
                                    time.sleep(timef)
                                if yc[0] > (x1 + ran):
                                    o1.left()
                                    print('Adjusting left yellow')
                                    time.sleep(timef)

                                if yc[0] < (x1 - ran):
                                    o1.right()
                                    print('Adjusting left yellow')
                                    time.sleep(timef)'''
                else:
                    o1.stop()
        if dir=='e':# for taking turns, requires correction.......................
            if abs(bc[1]-yc[1])<6 :
                dir='q'
                o1.stop()
            o1.right()
            if abs(bc[1]-yc[1])<6 and yc[0]<x2:
                o1.forward()
            else:
                o1.stop()



        # show the frame to our screen
        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1) & 0xFF
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break

camera.release()
cv2.destroyAllWindows()