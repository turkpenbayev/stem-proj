import cv2
import base64
import numpy as np
import math
import paho.mqtt.client as mqtt

TOPIC = 'esp/prediction'


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.


def on_message(client, userdata, message):
    #socketio.emit('my variable')
    print("Received message")
    socketio.emit('dht_temperature', {'data': message.payload.decode("utf-8")})


mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.username_pw_set("uwbfgkzz", "3rAA12jepUwD")
mqttc.connect("m24.cloudmqtt.com", 14281, 60)
# mqttc.connect("localhost",1883,60)
mqttc.loop_start()


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def frame_test(self):
        buffer = self.get_frame()

        # Convert to base64 encoding and show start of data
        jpg_as_text = base64.b64encode(buffer).decode()

        b64_src = 'data:image/png;base64,'
        img_src = b64_src + jpg_as_text

        return img_src

    def predict_frame(self):
        try:
            ret, frame = self.video.read()
            frame = cv2.flip(frame, 1)
            kernel = np.ones((3, 3), np.uint8)

            # define region of interest
            roi = frame[100:400, 100:400]

            cv2.rectangle(frame, (100, 100), (400, 400), (0, 255, 0), 0)
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

            # define range of skin color in HSV
            lower_skin = np.array([0, 20, 70], dtype=np.uint8)
            upper_skin = np.array([20, 255, 255], dtype=np.uint8)

            # extract skin colur imagw
            mask = cv2.inRange(hsv, lower_skin, upper_skin)

            # extrapolate the hand to fill dark spots within
            mask = cv2.dilate(mask, kernel, iterations=4)

            # blur the image
            mask = cv2.GaussianBlur(mask, (5, 5), 100)

            # find contours
            contours, hierarchy = cv2.findContours(
                mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # find contour of max area(hand)
            cnt = max(contours, key=lambda x: cv2.contourArea(x))

            # approx the contour a little
            epsilon = 0.0005*cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            # make convex hull around hand
            hull = cv2.convexHull(cnt)

            # define area of hull and area of hand
            areahull = cv2.contourArea(hull)
            areacnt = cv2.contourArea(cnt)

            # find the percentage of area not covered by hand in convex hull
            arearatio = ((areahull-areacnt)/areacnt)*100

            # find the defects in convex hull with respect to hand
            hull = cv2.convexHull(approx, returnPoints=False)
            defects = cv2.convexityDefects(approx, hull)

            # l = no. of defects
            l = 0

            # code for finding no. of defects due to fingers
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(approx[s][0])
                end = tuple(approx[e][0])
                far = tuple(approx[f][0])
                pt = (100, 180)

                # find length of all sides of triangle
                a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                s = (a+b+c)/2
                ar = math.sqrt(s*(s-a)*(s-b)*(s-c))

                # distance between point and convex hull
                d = (2*ar)/a

                # apply cosine rule here
                angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57

                # ignore angles > 90 and ignore points very close to convex hull(they generally come due to noise)
                if angle <= 90 and d > 30:
                    l += 1
                    cv2.circle(roi, far, 3, [255, 0, 0], -1)

                # draw lines around hand
                cv2.line(roi, start, end, [0, 255, 0], 2)

            l += 1

            # print corresponding gestures which are in their ranges
            if l == 1:
                if areacnt < 2000:
                    text = 'Put hand in the box'
                else:
                    if arearatio < 12:
                        text = '0'

                    elif arearatio < 17.5:
                        text = 'Best of luck'

                    else:
                        text = '1'

            elif l == 2:
                text = '2'

            elif l == 3:
                if arearatio < 27:
                    text = '3'
                else:
                    text = 'ok'

            elif l == 4:
                text = '4'

            elif l == 5:
                text = '5'

            elif l == 6:
                text = 'reposition'

            else:
                text = 'reposition'

            # show the windows

            return text

        except Exception as ex:
            pass


# if __name__ == "__main__":

#     camera = VideoCamera()
#     camera.frame_test()
