
import cv2


cap = cv2.VideoCapture(0)
i=1
while(i==1):
    i+=1
    # Capture frame-by-frame
    ret, gray = cap.read()
    #gray = imutils.resize(gray,width=480,height=360)
    x1, x2 = 40, 520
    y1, y2 = 5, 520
    gray = gray[y1:y2, x1:x2]
    print(gray.shape)
    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    cv2.imwrite('frame.jpg',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()