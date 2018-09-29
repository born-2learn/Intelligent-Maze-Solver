# only basic maze solver ...colors: black and white
import cv2
import bluetooth
import time
import numpy as np

import threading

import colorsys

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
        print('Deleted')'''#only to delete object(only if required).

    def disconnect(self):
        # Close socket connection to device
        self.sock.close()
    def stop(self):
        data='0'
        self.sock.send(data)

    def forward(self):
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


    '''def on(self):
        # Send '3' which the Arduino
        # detects as turning the light on
        data = "3"
        self.sock.send(data)

    def off(self):
        # Send '1' to turn off the light
        # attached to the Arduino
        data = "1"
        self.sock.send(data)'''



    def __init__(self):
        # Connect to the bluetooth device

        self.sock.connect((bd_addr, port))



o1=application()# use o1 always



class Point(object):



    def __init__(self, x=0, y=0):

        self.x = x

        self.y = y



    def __add__(self, other):

        return Point(self.x + other.x, self.y + other.y)



    def __eq__(self, other):

        return self.x == other.x and self.y == other.y





rw = 2

p = 0

start = Point()

end = Point()



dir4 = [Point(0, -1), Point(0, 1), Point(1, 0), Point(-1, 0)]





def BFS(s, e):



    global img, h, w

    const = 10000



    found = False

    q = []

    v = [[0 for j in range(w)] for i in range(h)]

    parent = [[Point() for j in range(w)] for i in range(h)]



    q.append(s)

    v[s.y][s.x] = 1

    while len(q) > 0:

        p = q.pop(0)

        for d in dir4:

            cell = p + d

            if (cell.x >= 0 and cell.x < w and cell.y >= 0 and cell.y < h and v[cell.y][cell.x] == 0 and

                    (img[cell.y][cell.x][0] != 0 or img[cell.y][cell.x][1] != 0 or img[cell.y][cell.x][2] != 0)):

                q.append(cell)

                v[cell.y][cell.x] = v[p.y][p.x] + 1  # Later



                img[cell.y][cell.x] = list(reversed(

                    [i * 255 for i in colorsys.hsv_to_rgb(v[cell.y][cell.x] / const, 1, 1)])

                )

                parent[cell.y][cell.x] = p

                if cell == e:

                    found = True

                    del q[:]

                    break



    path = []

    if found:

        p = e

        while p != s:

            path.append(p)

            p = parent[p.y][p.x]

        path.append(p)

        path.reverse()
        print(type(path))
        a1=[]
        a2=[]
        af=[]
        afinal=[]
        for i in path:# traversing path to get all points

            n=i.y
            m = i.x
            m=int(m)
            n=int(n)
            a1.append([m,n])
        #print (a1)
        xc=0
        yc=0
        #print(len(a1))
        print(a1[0][0],a1[0][1])
        for i in range(len(a1)-1):
            #print (i)
            c=0

            if a1[i][0]==a1[i+1][0] and a1[i][1]>a1[i+1][1]:
                a2.append('u')

            if a1[i][0]==a1[i+1][0] and a1[i][1]<a1[i+1][1]:
                a2.append('d')
            if a1[i][1]==a1[i+1][1] and a1[i][0]>a1[i+1][0]:
                a2.append('l')
            if a1[i][1]==a1[i+1][1] and a1[i][0]<a1[i+1][0]:
                a2.append('r')
        #print(a2)
        temp=[]
        tempv=''
        c=1
        fl=0
        for i in range(len(a2)-1):
            if(a2[i]=='u' and a2[i+1]=='u'):
                c+=1
            elif(a2[i]=='u' and a2[i+1]!='u'):
                #print(c,end=" kkk ")
                temp.append([c,a2[i]])
                c=1
                #print(c,temp,)
                continue
            if (a2[i] == 'r' and a2[i + 1] == 'r'):
                #print("ho")
                c += 1
            elif (a2[i] == 'r' and (a2[i + 1] != 'r' or i!=len(a2)-2) ):
                print(c, end=" kkk ")
                temp.append([c, a2[i]])
                c=1
                #print(c, temp, )
                continue
        templs=a2[-1]
        c=0
        for i in range(len(a2)-1,-1,-1):
            if a2[i]==templs :
                c+=1
            else:
                break
        temp.append([c,templs])

        afinal=temp
        print (afinal)








        for p in path:

            img[p.y][p.x] = [255, 255, 255]

        print("Path Found")

    else:

        print("Path Not Found")
    return(afinal)





def mouse_event(event, pX, pY, flags, param):



    global img, start, end, p



    if event == cv2.EVENT_LBUTTONUP:

        if p == 0:

            cv2.rectangle(img, (pX - rw, pY - rw),

                          (pX + rw, pY + rw), (0, 0, 255), -1)

            start = Point(pX, pY)

            print("start = ", start.x, start.y)

            p += 1

        elif p == 1:

            cv2.rectangle(img, (pX - rw, pY - rw),

                          (pX + rw, pY + rw), (0, 200, 50), -1)

            end = Point(pX, pY)

            print("end = ", end.x, end.y)

            p += 1





def disp():

    global img

    cv2.imshow("Image", img)

    cv2.setMouseCallback('Image', mouse_event)

    while True:

        cv2.imshow("Image", img)

        cv2.waitKey(1)





img = cv2.imread("maze.jpg", cv2.IMREAD_GRAYSCALE)
#img = cv2.resize(img, (0,0), fx=0.25, fy=0.25)

_, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY_INV)

img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

h, w = img.shape[:2]



print("Select start and end points : ")



t = threading.Thread(target=disp, args=())

t.daemon = True

t.start()



while p < 2:

    pass



arr=BFS(start, end)
for i in arr:
    if i[1]=='u':
        print (i[0])
        o1.forward()
        time.sleep(3)
    elif i[1]=='r':
        print(i[0])
        o1.right()
    elif i[1]=='l':
        print(i[0])
        o1.left()
print(arr)



cv2.waitKey(0)