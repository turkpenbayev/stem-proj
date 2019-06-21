#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, jsonify, request
from camera_opencv import Camera
import datetime
import random
import paho.mqtt.client as mqtt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


TOPIC = 'esp/prediction'


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.


def on_message(client, userdata, message):
    #socketio.emit('my variable')
    print("Received message")
    # socketio.emit('dht_temperature', {'data': message.payload.decode("utf-8")})


mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.username_pw_set("uwbfgkzz", "3rAA12jepUwD")
mqttc.connect("m24.cloudmqtt.com", 14281, 60)
# # mqttc.connect("localhost",1883,60)
mqttc.loop_start()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    return render_template('test.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame, label = camera.get_frame()
        mqttc.publish(TOPIC,label)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
