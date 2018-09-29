#final under control BT program
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
l1=[0,1,2,3]#LIST to store motor state

o1.forward()
time.sleep(3)
o1.right()
time.sleep(2)
o1.forward()
time.sleep(3)
o1.left()
time.sleep(2)
o1.forward(3)
#o1.left()




#o1.disconnect()